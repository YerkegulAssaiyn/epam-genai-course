"""
Build a relationship graph between vocabulary terms and their usage in research.md.

For every term in vocabulary.md the script counts:
  - explicit mentions: the term itself is written in the report (e.g. "RAG", "hallucinated")
  - implicit mentions: the idea is described in other words (e.g. "grounded in live account data" -> RAG)

Two terms are connected when they appear (explicitly or implicitly) in the same paragraph.
The edge weight is the number of shared paragraphs.

Outputs:
  terms_stats.json  - counts, matched phrases, and edges (the data behind the graph)
  terms_graph.png   - the graph plus an explicit vs implicit bar chart

Run: python build_graph.py
"""

import json
import re
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

HERE = Path(__file__).parent
REPORT = HERE / "research.md"

# term -> (group, explicit patterns, implicit patterns)
# Patterns are case-insensitive regular expressions.
TERMS = {
    "LLM": ("Core concepts",
            [r"\bLLMs?\b", r"\blarge language models?\b"],
            [r"\bGPT-4\b", r"\bGemini\b", r"\bgenerative model\b", r"\bmodels? (?:handled|did not handle)\b"]),
    "Token": ("Core concepts",
              [r"\btokens?\b"],
              [r"\bcosts? per (?:conversation|request)\b", r"\bcontrolling .{0,10}costs\b"]),
    "Tokenomics": ("Core concepts",
                   [r"\btokenomics\b"],
                   [r"\btoken costs?\b", r"\binfrastructure cost\b", r"\binitial cost\b", r"\bbusiness constraint\b"]),
    "Prompt": ("Core concepts",
               [r"\bprompts?\b(?!\s+injection)"],
               [r"\bpasted (?:a )?transcript\b", r"\binstructions?\b"]),
    "Hallucination": ("Core concepts",
                      [r"\bhallucinat\w*"],
                      [r"\binvent\w*\b", r"\bmislead\b", r"\bconfidently suggests wrong\b",
                       r"\bsubtly wrong\b", r"\bfactual or grammatical mistakes\b"]),
    "RAG": ("Working with data",
            [r"\bRAG\b"],
            [r"\bgrounded in\b", r"\bground it\b", r"\bsearch internal policies\b",
             r"\bknowledge base\b", r"\bsummarize policies\b"]),
    "Low-resource language": ("Working with data",
                              [r"\blow-resource languages?\b"],
                              [r"\bKazakh\b(?!stan)", r"\blocal languages\b", r"\bless high-quality training data\b"]),
    "Speech-to-text": ("Working with data",
                       [r"\bspeech-to-text\b"],
                       [r"\btranscripts?\b", r"\btranscription\b", r"\blisten(?:ed)? to\b", r"\bby voice\b",
                        r"\bvoice assistant\b"]),
    "AI agent": ("Agents and safety",
                 [r"\bagentic\b", r"\bAI agents?\b", r"\ban agent (?:that|which)\b", r"\bagents that\b"],
                 [r"\bperform operations\b", r"\bexecutes?\b", r"\bon the (?:customer's|user's) behalf\b",
                  r"\bcreate Jira work items\b", r"\bfrom answering to \*acting\*"]),
    "Human-in-the-loop": ("Agents and safety",
                          [r"\bhuman[- ]in[- ]the[- ]loop\b"],
                          [r"\bhuman review\w*\b", r"\bafter a human reviews\b", r"\bafter (?:user )?confirmation\b",
                           r"\bapprove before create\b", r"\bhuman oversight\b", r"\bmakes the final decision\b",
                           r"\bhuman remains responsible\b"]),
    "Guardrails": ("Agents and safety",
                   [r"\bguardrails?\b"],
                   [r"\bconstrained by\b", r"\bstrict permissions\b", r"\bacademic integrity\b",
                    r"\bage-appropriate\b"]),
    "Prompt injection": ("Agents and safety",
                         [r"\bprompt injection\b"],
                         [r"\bsocial engineering\b"]),
    "Copilot": ("Types of AI tools",
                [r"\bcopilot\b"],
                [r"\baugments?\b", r"\bagent assist\b", r"\bonly suggests\b"]),
    "AI-native": ("Types of AI tools",
                  [r"\bAI-native\b"],
                  [r"\brebuilt around AI\b"]),
    "Acceptance criteria": ("Process and education",
                            [r"\bacceptance criteria\b"],
                            [r"\bstructured specification\b", r"\bstandardized ticket quality\b"]),
    "Socratic approach": ("Process and education",
                          [r"\bsocratic\b"],
                          [r"\bguiding questions\b", r"\bguide, not write\b", r"\btoward answers\b",
                           r"\binstead of giving\b", r"\bwithout receiving ready-made solutions\b"]),
}

GROUP_COLORS = {  # validated categorical slots, fixed order
    "Core concepts": "#2a78d6",
    "Working with data": "#eb6834",
    "Agents and safety": "#1baf7a",
    "Types of AI tools": "#eda100",
    "Process and education": "#e87ba4",
}


def paragraphs(text):
    """Split the report into paragraphs, skipping headings, links lists and the mermaid block."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    out = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block or block.startswith("#") or block == "---":
            continue
        out.append(block)
    return out


def find(patterns, text):
    spans = []
    for p in patterns:
        for m in re.finditer(p, text, flags=re.I):
            spans.append((m.start(), m.end(), m.group(0)))
    return spans


def overlaps(span, others):
    return any(span[0] < o[1] and o[0] < span[1] for o in others)


def main():
    paras = paragraphs(REPORT.read_text(encoding="utf-8"))
    stats = {t: {"group": g, "explicit": 0, "implicit": 0,
                 "explicit_matches": [], "implicit_matches": []} for t, (g, _, _) in TERMS.items()}
    presence = {t: set() for t in TERMS}

    for i, para in enumerate(paras):
        for term, (_, exp, imp) in TERMS.items():
            e = find(exp, para)
            im = [s for s in find(imp, para) if not overlaps(s, e)]
            stats[term]["explicit"] += len(e)
            stats[term]["implicit"] += len(im)
            stats[term]["explicit_matches"] += [s[2] for s in e]
            stats[term]["implicit_matches"] += [s[2] for s in im]
            if e or im:
                presence[term].add(i)

    edges = []
    for a, b in combinations(TERMS, 2):
        w = len(presence[a] & presence[b])
        if w:
            edges.append({"source": a, "target": b, "weight": w})

    (HERE / "terms_stats.json").write_text(
        json.dumps({"terms": stats, "edges": edges}, indent=2, ensure_ascii=False), encoding="utf-8")

    draw(stats, edges)
    for t, s in stats.items():
        print(f"{t:24} explicit={s['explicit']:3} implicit={s['implicit']:3}")
    print(f"edges: {len(edges)}")


def draw(stats, edges):
    ink, muted, grid = "#0b0b0b", "#52514e", "#d9d8d4"
    fig = plt.figure(figsize=(12, 17), facecolor="#fcfcfb")
    ax1 = fig.add_axes([0.03, 0.40, 0.94, 0.55])
    ax2 = fig.add_axes([0.24, 0.04, 0.72, 0.27])

    G = nx.Graph()
    for t, s in stats.items():
        G.add_node(t, total=s["explicit"] + s["implicit"])
    for e in edges:
        if e["weight"] >= 2:  # draw only links shared in 2+ paragraphs; all links are in terms_stats.json
            G.add_edge(e["source"], e["target"], weight=e["weight"])

    full = nx.Graph()
    full.add_nodes_from(G.nodes())
    full.add_edges_from((e["source"], e["target"]) for e in edges)
    pos = nx.kamada_kawai_layout(full)  # layout uses all links, drawing shows the strong ones
    maxw = max(d["weight"] for _, _, d in G.edges(data=True))
    nx.draw_networkx_edges(G, pos, ax=ax1, edge_color="#a3a29d",
                           width=[0.6 + 3.4 * G[u][v]["weight"] / maxw for u, v in G.edges()],
                           alpha=0.45)
    sizes = [300 + 90 * G.nodes[n]["total"] for n in G.nodes()]
    colors = [GROUP_COLORS[stats[n]["group"]] for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=sizes, node_color=colors,
                           edgecolors="#fcfcfb", linewidths=2)
    for n, (x, y) in pos.items():
        s = stats[n]
        ax1.annotate(f"{n}\nE {s['explicit']} · I {s['implicit']}", (x, y),
                     xytext=(0, -13 - (300 + 90 * G.nodes[n]['total']) ** 0.5 / 2),
                     textcoords="offset points", ha="center", va="top", fontsize=10, color=ink,
                     bbox=dict(boxstyle="round,pad=0.2", fc="#fcfcfb", ec="none", alpha=0.9), zorder=5)
    ax1.set_title("GenAI vocabulary: how terms connect in my report",
                  fontsize=17, color=ink, loc="left", pad=40, fontweight="bold")
    ax1.text(0, 1.01, "Node size = total mentions (E = explicit, I = implicit).\n"
             "Line = terms used together in 2+ paragraphs; thicker = more shared paragraphs.",
             transform=ax1.transAxes, fontsize=10.5, color=muted, va="bottom")
    handles = [plt.Line2D([], [], marker="o", ls="", ms=11, mfc=c, mec="none", label=g)
               for g, c in GROUP_COLORS.items()]
    ax1.legend(handles=handles, loc="upper left", bbox_to_anchor=(0, -0.02), frameon=False, fontsize=10, ncol=3)
    ax1.margins(0.12)
    ax1.axis("off")

    order = sorted(stats, key=lambda t: stats[t]["explicit"] + stats[t]["implicit"])
    exp = [stats[t]["explicit"] for t in order]
    imp = [stats[t]["implicit"] for t in order]
    y = range(len(order))
    h = 0.38
    ax2.barh([i + h / 2 + 0.02 for i in y], exp, height=h, color="#2a78d6", label="Explicit")
    ax2.barh([i - h / 2 - 0.02 for i in y], imp, height=h, color="#eb6834", label="Implicit")
    for i, (a, b) in enumerate(zip(exp, imp)):
        ax2.text(a + 0.3, i + h / 2 + 0.02, str(a), va="center", fontsize=8.5, color=muted)
        ax2.text(b + 0.3, i - h / 2 - 0.02, str(b), va="center", fontsize=8.5, color=muted)
    ax2.set_yticks(list(y))
    ax2.set_yticklabels(order, fontsize=10, color=ink)
    ax2.set_title("Explicit vs implicit mentions per term", fontsize=13, color=ink, loc="left", pad=10)
    ax2.legend(frameon=False, loc="lower right", fontsize=10)
    ax2.xaxis.grid(True, color=grid, lw=0.8)
    ax2.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax2.spines[side].set_visible(False)
    ax2.spines["bottom"].set_color(grid)
    ax2.tick_params(axis="x", colors=muted)
    ax2.tick_params(axis="y", length=0)

    fig.savefig(HERE / "terms_graph.png", dpi=150, facecolor=fig.get_facecolor())


if __name__ == "__main__":
    main()
