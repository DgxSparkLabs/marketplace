# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Generate an interactive HTML dashboard analyzing skill usage from the
Devin CLI sessions database.

Reads ~/.local/share/devin/cli/sessions.db, extracts actual skill
invocations (tool_calls with name="skill", command="invoke"), and
produces a self-contained HTML file with Chart.js visualizations.
"""

import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DEFAULT_DB = Path.home() / ".local" / "share" / "devin" / "cli" / "sessions.db"


def get_db(db_path: str | None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else DEFAULT_DB
    if not path.exists():
        print(f"Error: database not found at {path}", file=sys.stderr)
        print("Is Devin CLI installed? Expected sessions.db here.", file=sys.stderr)
        sys.exit(1)
    return sqlite3.connect(str(path))


def extract_usage(conn: sqlite3.Connection, skills_dir: Path | None = None) -> dict:
    """Parse all sessions and extract skill invocation data."""
    cur = conn.cursor()

    cur.execute("SELECT id, title, created_at FROM sessions ORDER BY created_at")
    sessions = cur.fetchall()

    cur.execute("SELECT count(*) FROM message_nodes")
    n_messages = cur.fetchone()[0]

    # Discover installed skills from the skills directory
    if skills_dir is None:
        skills_dir = Path.home() / ".config" / "devin" / "skills"
    installed = set()
    if skills_dir.is_dir():
        installed = {d.name for d in skills_dir.iterdir() if d.is_dir()}

    skill_inv = defaultdict(int)
    skill_sess = defaultdict(set)
    skill_timeline = defaultdict(list)
    session_skills = defaultdict(dict)

    for idx, (sid, title, created_at) in enumerate(sessions):
        cur.execute(
            "SELECT chat_message FROM message_nodes "
            "WHERE session_id=? AND chat_message LIKE '%\"skill\"%'",
            (sid,),
        )
        for (raw,) in cur.fetchall():
            try:
                msg = json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                continue
            if msg.get("role") != "assistant":
                continue
            for tc in msg.get("tool_calls", []):
                if tc.get("name") != "skill":
                    continue
                args = tc.get("arguments", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except (json.JSONDecodeError, TypeError):
                        continue
                if args.get("command") == "invoke" and args.get("skill"):
                    sk = args["skill"]
                    skill_inv[sk] += 1
                    skill_sess[sk].add(sid)
                    session_skills[sid][sk] = session_skills[sid].get(sk, 0) + 1

        for sk, cnt in session_skills.get(sid, {}).items():
            skill_timeline[sk].append((idx, cnt))

    # Count sessions with any skill use
    sessions_with_skills = set()
    for sids in skill_sess.values():
        sessions_with_skills |= sids

    # Measure SKILL.md sizes for installed skills
    skill_sizes = {}
    for name in installed:
        skill_md = skills_dir / name / "SKILL.md"
        if skill_md.exists():
            text = skill_md.read_text(errors="replace")
            lines = len(text.splitlines())
            tokens_est = len(text) // 4
            skill_sizes[name] = {"lines": lines, "tokens": tokens_est}

    return {
        "n_sessions": len(sessions),
        "n_messages": n_messages,
        "sessions": sessions,
        "installed_skills": sorted(installed),
        "skill_sizes": skill_sizes,
        "skill_inv": dict(skill_inv),
        "skill_sess": {k: len(v) for k, v in skill_sess.items()},
        "skill_timeline": {k: v for k, v in skill_timeline.items()},
        "n_with_skills": len(sessions_with_skills),
    }


def compute_rolling(data: dict, window: int) -> dict:
    """Compute rolling usage rate per skill."""
    sessions = data["sessions"]
    skill_sess_sets = defaultdict(set)
    # Rebuild sets from timeline
    for sk, entries in data["skill_timeline"].items():
        for idx, cnt in entries:
            skill_sess_sets[sk].add(sessions[idx][0])

    rolling = {}
    for sk in data["skill_inv"]:
        ss = skill_sess_sets[sk]
        rates = []
        for i in range(len(sessions)):
            w = max(0, i - window + 1)
            wids = [sessions[j][0] for j in range(w, i + 1)]
            rates.append(round(sum(1 for sid in wids if sid in ss) / len(wids), 3))
        rolling[sk] = rates
    return rolling


def build_json_output(data: dict, window: int) -> dict:
    """Build structured JSON output."""
    rolling = compute_rolling(data, window)
    return {
        "summary": {
            "total_sessions": data["n_sessions"],
            "total_messages": data["n_messages"],
            "sessions_with_skill_use": data["n_with_skills"],
            "installed_skills": data["installed_skills"],
            "skills_ever_invoked": len(data["skill_inv"]),
        },
        "per_skill": {
            sk: {
                "invocations": data["skill_inv"].get(sk, 0),
                "sessions": data["skill_sess"].get(sk, 0),
                "installed": sk in data["installed_skills"],
                "size": data["skill_sizes"].get(sk),
                "rolling_rate": rolling.get(sk, []),
            }
            for sk in sorted(
                set(data["installed_skills"]) | set(data["skill_inv"].keys())
            )
        },
    }


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

PAL = {
    "green": "#4ade80", "red": "#f87171", "accent": "#6c8cff",
    "orange": "#fb923c", "yellow": "#facc15", "purple": "#c084fc",
    "cyan": "#22d3ee", "pink": "#f472b6",
}
SKILL_COLORS = [
    PAL["green"], PAL["accent"], PAL["purple"], PAL["pink"],
    PAL["cyan"], PAL["orange"], PAL["yellow"], PAL["red"],
]


def build_html(data: dict, window: int) -> str:
    """Generate a self-contained HTML dashboard."""
    n_sessions = data["n_sessions"]
    n_messages = data["n_messages"]
    n_installed = len(data["installed_skills"])
    n_with_skills = data["n_with_skills"]

    # Skills sorted by session count
    all_invoked = sorted(
        data["skill_inv"].keys(), key=lambda s: -data["skill_sess"].get(s, 0)
    )
    n_invoked = len(all_invoked)
    n_multi = sum(1 for s in all_invoked if data["skill_sess"].get(s, 0) >= 2)
    n_consistent = sum(1 for s in all_invoked if data["skill_sess"].get(s, 0) >= 5)

    sess_labels = json.dumps(all_invoked)
    sess_values = json.dumps([data["skill_sess"].get(s, 0) for s in all_invoked])
    sess_colors = json.dumps([
        PAL["green"] if data["skill_sess"].get(s, 0) >= 5
        else PAL["accent"] if data["skill_sess"].get(s, 0) >= 2
        else PAL["orange"]
        for s in all_invoked
    ])

    inv_sorted = sorted(all_invoked, key=lambda s: -data["skill_inv"].get(s, 0))
    inv_labels = json.dumps(inv_sorted)
    inv_values = json.dumps([data["skill_inv"][s] for s in inv_sorted])
    inv_colors = json.dumps([
        PAL["green"] if data["skill_inv"][s] >= 50
        else PAL["accent"] if data["skill_inv"][s] >= 5
        else PAL["orange"]
        for s in inv_sorted
    ])

    # Timeline bubbles
    color_map = {s: SKILL_COLORS[i % len(SKILL_COLORS)] for i, s in enumerate(all_invoked)}
    bubbles, bub_bg, bub_bd = [], [], []
    for si, sk in enumerate(all_invoked):
        for idx, cnt in data["skill_timeline"].get(sk, []):
            r = min(3 + cnt**0.4 * 3, 22)
            bubbles.append({"x": idx, "y": si, "r": round(r, 1)})
            bub_bg.append(color_map[sk] + "aa")
            bub_bd.append(color_map[sk])

    # Rolling window
    rolling = compute_rolling(data, window)
    roll_datasets = []
    for sk in all_invoked:
        if sk not in rolling:
            continue
        c = color_map.get(sk, PAL["accent"])
        roll_datasets.append({
            "label": sk, "data": rolling[sk],
            "borderColor": c, "backgroundColor": c + "22",
            "borderWidth": 2, "pointRadius": 0,
            "fill": False, "tension": 0.3,
        })

    # Installed skills table
    installed_table_rows = ""
    for sk in sorted(data["installed_skills"]):
        inv = data["skill_inv"].get(sk, 0)
        sess = data["skill_sess"].get(sk, 0)
        sz = data["skill_sizes"].get(sk, {})
        lines = sz.get("lines", "?")
        tokens = sz.get("tokens", "?")
        tok_str = f"{tokens:,}" if isinstance(tokens, int) else tokens
        installed_table_rows += (
            f"<tr><td>{sk}</td>"
            f"<td class='n'>{lines}</td>"
            f"<td class='n'>{tok_str}</td>"
            f"<td class='n'>{sess}</td>"
            f"<td class='n'>{inv}</td></tr>\n"
        )

    # Never-invoked installed skills
    never_used = [s for s in data["installed_skills"] if data["skill_inv"].get(s, 0) == 0]
    n_never = len(never_used)
    never_list = ", ".join(never_used) if never_used else "(none)"

    # Context budget
    listing_tokens = n_installed * 30
    total_skill_tokens = sum(
        data["skill_sizes"].get(s, {}).get("tokens", 0)
        for s in data["installed_skills"]
    )

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skill Analytics Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{{--bg:#0f1117;--sf:#1a1d27;--sf2:#232733;--bd:#2d3140;--tx:#e1e4eb;--tx2:#8b90a0;--ac:#6c8cff;--gn:#4ade80;--rd:#f87171;--or:#fb923c;--yl:#facc15}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6;padding:0 0 4rem}}
.hdr{{padding:3rem 2rem 2rem;max-width:1200px;margin:0 auto;border-bottom:1px solid var(--bd)}}
.hdr h1{{font-size:2rem;font-weight:700;margin-bottom:.5rem}}
.hdr .sub{{color:var(--tx2);font-size:.95rem}} .hdr .date{{color:var(--tx2);font-size:.85rem;margin-top:.25rem}}
.kr{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;max-width:1200px;margin:2rem auto;padding:0 2rem}}
.k{{background:var(--sf);border:1px solid var(--bd);border-radius:12px;padding:1.25rem 1.5rem}}
.k .n{{font-size:2.2rem;font-weight:700;line-height:1.1}}
.k .n.g{{color:var(--gn)}}.k .n.r{{color:var(--rd)}}.k .n.a{{color:var(--ac)}}.k .n.o{{color:var(--or)}}
.k .l{{color:var(--tx2);font-size:.85rem;margin-top:.25rem}}
.k .e{{color:var(--tx2);font-size:.78rem;margin-top:.5rem;border-top:1px solid var(--bd);padding-top:.5rem}}
.sec{{max-width:1200px;margin:3rem auto 0;padding:0 2rem}}
.sec h2{{font-size:1.35rem;font-weight:600;margin-bottom:.25rem}}
.sec .ld{{color:var(--tx2);font-size:.92rem;margin-bottom:1.5rem;max-width:720px}}
.cg{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}}
@media(max-width:800px){{.cg{{grid-template-columns:1fr}}}}
.cc{{background:var(--sf);border:1px solid var(--bd);border-radius:12px;padding:1.5rem}}
.cc.f{{grid-column:1/-1}} .cc h3{{font-size:1rem;font-weight:600;margin-bottom:.15rem}}
.cc .ce{{color:var(--tx2);font-size:.82rem;margin-bottom:1rem}}
.cw{{position:relative;width:100%}} .cw.h3{{height:300px}}.cw.h35{{height:350px}}
.ins{{background:var(--sf2);border-left:3px solid var(--ac);border-radius:0 8px 8px 0;padding:.85rem 1.1rem;margin-top:1rem;font-size:.88rem}}
.ins strong{{color:var(--ac)}}
.tw{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:.88rem}}
th,td{{padding:.6rem .8rem;text-align:left;border-bottom:1px solid var(--bd)}}
th{{color:var(--tx2);font-weight:500;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
.fr{{display:flex;align-items:center;gap:1rem;margin:1.5rem 0;flex-wrap:wrap;justify-content:center}}
.fb{{background:var(--sf2);border:1px solid var(--bd);border-radius:10px;padding:1rem 1.5rem;text-align:center;min-width:140px}}
.fb .fn{{font-size:2rem;font-weight:700}} .fb .fl{{font-size:.8rem;color:var(--tx2)}}
.fa{{font-size:1.5rem;color:var(--tx2)}}
.ft{{max-width:1200px;margin:4rem auto 0;padding:2rem;border-top:1px solid var(--bd);color:var(--tx2);font-size:.82rem}}
</style>
</head>
<body>
<div class="hdr">
  <h1>Skill Analytics Dashboard</h1>
  <div class="sub">Your personal skill usage analysis &mdash; {n_installed} installed skills across {n_sessions} sessions.</div>
  <div class="date">{now_str} &middot; {n_messages:,} message nodes analyzed</div>
</div>

<div class="kr">
  <div class="k"><div class="n a">{n_installed}</div><div class="l">Installed Skills</div><div class="e">Currently in your skills directory.</div></div>
  <div class="k"><div class="n g">{n_invoked}</div><div class="l">Ever Invoked</div><div class="e">Skills that were actually called via <code>skill invoke</code> at least once.</div></div>
  <div class="k"><div class="n {'r' if n_never > 0 else 'g'}">{n_never}</div><div class="l">Never Used</div><div class="e">{never_list if n_never <= 5 else f'{n_never} installed skills have zero invocations.'}</div></div>
  <div class="k"><div class="n o">{round(n_with_skills/n_sessions*100) if n_sessions else 0}%</div><div class="l">Sessions Using Skills</div><div class="e">{n_with_skills} of {n_sessions} sessions invoked any skill at all.</div></div>
</div>

<div class="sec">
  <h2>Usage Funnel</h2>
  <p class="ld">How skills narrow from &ldquo;installed&rdquo; to &ldquo;consistently used.&rdquo;</p>
  <div class="fr">
    <div class="fb"><div class="fn">{n_installed}</div><div class="fl">Installed</div></div>
    <div class="fa">&rarr;</div>
    <div class="fb"><div class="fn">{n_invoked}</div><div class="fl">Ever Invoked</div></div>
    <div class="fa">&rarr;</div>
    <div class="fb"><div class="fn">{n_multi}</div><div class="fl">2+ Sessions</div></div>
    <div class="fa">&rarr;</div>
    <div class="fb"><div class="fn" style="color:var(--gn)">{n_consistent}</div><div class="fl">5+ Sessions</div></div>
  </div>
</div>

<div class="sec">
  <h2>Session Spread vs Invocation Count</h2>
  <p class="ld">Session spread is a better quality signal than raw count. A skill used across many sessions is more broadly useful than one invoked hundreds of times in a single marathon session.</p>
  <div class="cg">
    <div class="cc"><h3>Sessions per Skill</h3><div class="ce">Distinct sessions where each skill was invoked.</div><div class="cw h35"><canvas id="cSess"></canvas></div></div>
    <div class="cc"><h3>Invocations (log scale)</h3><div class="ce">Total invocation count. High numbers in few sessions may indicate branching conversations, not broad adoption.</div><div class="cw h35"><canvas id="cInv"></canvas></div></div>
  </div>
</div>

<div class="sec">
  <h2>Usage Timeline</h2>
  <p class="ld">Each bubble is a session where a skill was invoked. Size reflects invocation count.</p>
  <div class="cg"><div class="cc f"><h3>Skill Invocations Over Time</h3><div class="ce">X-axis is session index (chronological). Hover for details.</div><div class="cw h3"><canvas id="cTime"></canvas></div></div></div>
</div>

<div class="sec">
  <h2>Rolling Usage Rate</h2>
  <p class="ld">For each session, what fraction of the last {window} sessions used that skill. Reveals sustained adoption vs one-off spikes.</p>
  <div class="cg"><div class="cc f"><h3>{window}-Session Rolling Window</h3><div class="ce">A skill at 0.3 means it was used in {window*3//10} of the last {window} sessions. Hover to see the skill name and rate.</div><div class="cw h3"><canvas id="cRoll"></canvas></div></div></div>
</div>

<div class="sec">
  <h2>Installed Skills</h2>
  <p class="ld">All skills currently in your skills directory with their size and usage data.</p>
  <div class="cc f" style="padding:.75rem"><div class="tw"><table>
    <thead><tr><th>Skill</th><th class="n">Lines</th><th class="n">~Tokens</th><th class="n">Sessions</th><th class="n">Invocations</th></tr></thead>
    <tbody>{installed_table_rows}</tbody>
  </table></div></div>
</div>

<div class="sec">
  <h2>Context Budget</h2>
  <p class="ld">Every installed skill costs ~30 tokens in the system prompt listing, plus its full SKILL.md content when invoked.</p>
  <div class="cg">
    <div class="cc">
      <h3>Always-On Cost</h3>
      <div class="ce">Tokens consumed every session just by having skills installed.</div>
      <div style="font-size:2rem;font-weight:700;color:var(--ac);margin:.5rem 0">~{listing_tokens:,} tokens</div>
      <div style="color:var(--tx2);font-size:.85rem">{n_installed} skills &times; ~30 tokens per listing</div>
    </div>
    <div class="cc">
      <h3>On-Demand Cost (when invoked)</h3>
      <div class="ce">Total SKILL.md content across all installed skills.</div>
      <div style="font-size:2rem;font-weight:700;color:var(--or);margin:.5rem 0">~{total_skill_tokens:,} tokens</div>
      <div style="color:var(--tx2);font-size:.85rem">Sum of all SKILL.md files. Only one is loaded at a time.</div>
    </div>
  </div>
</div>

<div class="ft">
  Generated from <code>sessions.db</code> &middot; {n_sessions} sessions &middot; {n_messages:,} messages &middot; {now_str}
</div>

<script>
const C={{ac:'#6c8cff',gn:'#4ade80',rd:'#f87171',or:'#fb923c',yl:'#facc15',pu:'#c084fc',cy:'#22d3ee',pk:'#f472b6'}};
Chart.defaults.color='#8b90a0';Chart.defaults.borderColor='#2d3140';
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif";

new Chart(document.getElementById('cSess'),{{type:'bar',data:{{labels:{sess_labels},datasets:[{{data:{sess_values},backgroundColor:{sess_colors},borderRadius:6,barPercentage:.7}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>c.raw+' session'+(c.raw!==1?'s':'')}}}}}},scales:{{x:{{title:{{display:true,text:'Sessions',color:'#8b90a0'}},grid:{{color:'#2d314040'}}}},y:{{grid:{{display:false}}}}}}}}}});

new Chart(document.getElementById('cInv'),{{type:'bar',data:{{labels:{inv_labels},datasets:[{{data:{inv_values},backgroundColor:{inv_colors},borderRadius:6,barPercentage:.7}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>c.raw.toLocaleString()+' invocations'}}}}}},scales:{{x:{{type:'logarithmic',title:{{display:true,text:'Invocations (log)',color:'#8b90a0'}},grid:{{color:'#2d314040'}}}},y:{{grid:{{display:false}}}}}}}}}});

new Chart(document.getElementById('cTime'),{{type:'bubble',data:{{datasets:[{{data:{json.dumps(bubbles)},backgroundColor:{json.dumps(bub_bg)},borderColor:{json.dumps(bub_bd)},borderWidth:1}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>{{const n={sess_labels};return n[c.raw.y]+' (session '+c.raw.x+')'}}}}}}}},scales:{{x:{{title:{{display:true,text:'Session index',color:'#8b90a0'}},min:0,max:{n_sessions},grid:{{color:'#2d314040'}}}},y:{{ticks:{{callback:v=>{{const n={sess_labels};return n[v]||''}},stepSize:1}},min:-.5,max:{len(all_invoked)-.5},grid:{{color:'#2d314040'}}}}}}}}}});

new Chart(document.getElementById('cRoll'),{{type:'line',data:{{labels:Array.from({{length:{n_sessions}}},(_,i)=>i),datasets:{json.dumps(roll_datasets)}}},options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'nearest',intersect:false,axis:'x'}},plugins:{{legend:{{position:'bottom',labels:{{boxWidth:12,padding:10}}}},tooltip:{{callbacks:{{title:c=>c.length?'Session '+c[0].label:'',label:c=>c.dataset.label+': '+(c.raw*100).toFixed(0)+'% of last {window} sessions'}}}}}},scales:{{x:{{title:{{display:true,text:'Session index',color:'#8b90a0'}},grid:{{color:'#2d314020'}}}},y:{{title:{{display:true,text:'Fraction of last {window} sessions',color:'#8b90a0'}},min:0,max:1,grid:{{color:'#2d314040'}}}}}}}}}});
</script>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(
        description="Analyze skill usage and generate an interactive dashboard.",
    )
    parser.add_argument(
        "--output", default="./skill_audit.html",
        help="Output HTML file path (default: ./skill_audit.html)",
    )
    parser.add_argument(
        "--db", default=None,
        help=f"Path to sessions database (default: {DEFAULT_DB})",
    )
    parser.add_argument(
        "--window", type=int, default=10,
        help="Rolling window size in sessions (default: 10)",
    )
    parser.add_argument(
        "--skills-dir", default=None,
        help="Path to installed skills directory (default: ~/.config/devin/skills)",
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output raw analysis data as JSON instead of HTML",
    )
    args = parser.parse_args()

    conn = get_db(args.db)
    skills_path = Path(os.path.expanduser(args.skills_dir)) if args.skills_dir else None
    data = extract_usage(conn, skills_dir=skills_path)
    conn.close()

    if args.json_output:
        out = build_json_output(data, args.window)
        print(json.dumps(out, indent=2))
        return

    html = build_html(data, args.window)
    out_path = os.path.expanduser(args.output)
    with open(out_path, "w") as f:
        f.write(html)
    print(f"Dashboard written to {out_path}")
    print(f"  {data['n_sessions']} sessions, {data['n_messages']:,} messages analyzed")
    print(f"  {len(data['installed_skills'])} installed skills, "
          f"{len(data['skill_inv'])} ever invoked")


if __name__ == "__main__":
    main()
