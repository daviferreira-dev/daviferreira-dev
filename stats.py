#!/usr/bin/env python3
"""Gera assets/registro.svg (Registro de aventura) com dados reais do GitHub, no estilo RPG do perfil.

Roda no GitHub Actions (variável GITHUB_TOKEN). Para testar localmente sem token: MOCK_FILE=dados.json python3 stats.py
"""
import os, json, datetime, urllib.request
from gen import W, ptext, txt, header, window, dash, svg, save, tw, robot, ROBOT_CSS

USER = os.environ.get("GH_USER", "daviferreira-dev")

QUERY = """query($login:String!){ user(login:$login){
  createdAt
  contributionsCollection{
    totalCommitContributions totalPullRequestContributions totalIssueContributions restrictedContributionsCount
    contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } }
  repositories(first:100, ownerAffiliations:OWNER, isFork:false){ totalCount nodes{ stargazerCount
    languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name } } } } }
}}"""


def fetch():
    if os.environ.get("MOCK_FILE"):
        return json.load(open(os.environ["MOCK_FILE"], encoding="utf-8"))
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": "bearer " + os.environ["GITHUB_TOKEN"], "Content-Type": "application/json",
                 "User-Agent": "registro-de-aventura"})
    d = json.load(urllib.request.urlopen(req))
    if "errors" in d:
        raise SystemExit(json.dumps(d["errors"]))
    return d["data"]["user"]


def streaks(days):
    """Sequência atual (tolerando hoje ainda sem contribuição) e maior sequência do período."""
    best = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        best = max(best, run)
    cur = 0
    seq = list(days)
    if seq and seq[-1][1] == 0:
        seq = seq[:-1]
    for _, c in reversed(seq):
        if c == 0: break
        cur += 1
    return cur, best


def fmt(n):
    return f"{n:,}".replace(",", ".")


def registro(u):
    cc = u["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    cur, best = streaks(days)
    repos = u["repositories"]
    stars = sum(r["stargazerCount"] for r in repos["nodes"])
    langs = {}
    for r in repos["nodes"]:
        for e in r["languages"]["edges"]:
            if e["node"]["name"] in ("Jupyter Notebook",): continue             langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]

    css = ["@keyframes on{to{opacity:1}}", ".s{opacity:0;animation:on .01s forwards}",
           "@keyframes bl{50%{opacity:0}}.bl{animation:bl 1s steps(1) infinite}",
           "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}",
           ".g{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:grow .8s steps(10) forwards}",
           ROBOT_CSS]
    b = [header("REGISTRO DE AVENTURA")]

    # ---- janela 1: status + sequência
    h1 = 200
    b.append(window(0, 30, W, h1))
    b.append(ptext("STATUS · ÚLTIMOS 12 MESES", 28, 52, 2, fill="#888"))
    stats = [("CONTRIBUIÇÕES", cal["totalContributions"]), ("COMMITS", cc["totalCommitContributions"]),
             ("PULL REQUESTS", cc["totalPullRequestContributions"]), ("ISSUES", cc["totalIssueContributions"]),
             ("REPOSITÓRIOS", repos["totalCount"]), ("ESTRELAS", stars)]
    for i, (k, v) in enumerate(stats):
        col, row = i % 2, i // 2
        x, y = 28 + col * 230, 84 + row * 40
        b.append(f'<g class="s" style="animation-delay:{.2 + i * .15:.2f}s">{ptext(k, x, y, 1, fill="#aaa")}'
                 f'{txt(x + 210, y + 8, fmt(v), fill="#fff", size=16, anchor="end", extra=chr(32) + "font-weight=" + chr(34) + "bold" + chr(34))}</g>')
        b.append(dash(x, x + 210, y + 20))
    # sequência (lado direito)
    sx = 520
    b.append(f'<rect x="{sx}" y="50" width="250" height="160" fill="#000" stroke="#555" stroke-width="2"/>')
    b.append(ptext("SEQUÊNCIA", sx + 125, 62, 2, fill="#888", anchor="middle"))
    # chama pixel
    flame = ["...#...", "..##...", "..###..", ".#####.", ".##.##.", "##...##", ".#####."]
    fd = "".join(f"M{sx + 104 + c * 6} {84 + r * 6}h6v6h-6z" for r, l in enumerate(flame) for c, ch in enumerate(l) if ch == "#")
    b.append(f'<path class="bl" fill="#fff" d="{fd}"/>')
    b.append(txt(sx + 125, 158, f"{cur} {'dia' if cur == 1 else 'dias'}", fill="#fff", size=22, anchor="middle", extra='font-weight="bold"'))
    b.append(ptext("ATUAL", sx + 125, 168, 1, fill="#aaa", anchor="middle"))
    b.append(txt(sx + 125, 196, f"maior sequência: {best} {'dia' if best == 1 else 'dias'}", fill="#888", size=12, anchor="middle"))

    # ---- janela 2: linguagens
    y2 = 30 + h1 + 10
    h2 = 60 + len(top) * 26 + 10
    b.append(window(0, y2, W, h2))
    b.append(ptext("LINGUAGENS MAIS USADAS", 28, y2 + 22, 2, fill="#888"))
    for i, (name, size) in enumerate(top):
        y = y2 + 56 + i * 26
        pct = size / total
        bw = max(4, round(pct * 470 / 10) * 10)
        b.append(txt(28, y + 12, name, fill="#fff", size=14))
        b.append(f'<rect x="200" y="{y}" width="480" height="14" fill="#1a1a1a"/>')
        b.append(f'<rect class="g" x="200" y="{y}" width="{bw}" height="14" fill="#fff" style="animation-delay:{.3 + i * .15:.2f}s"/>')
        b.append(txt(W - 28, y + 12, f"{pct * 100:.1f}%", fill="#aaa", size=13, anchor="end"))

    # ---- janela 3: mapa de contribuições (heatmap) com robô percorrendo
    y3 = y2 + h2 + 10
    weeks = cal["weeks"][-53:]
    cell = 13
    gx = (W - len(weeks) * cell) / 2
    h3 = 40 + 7 * cell + 40
    b.append(window(0, y3, W, h3))
    b.append(ptext("MAPA DE CONTRIBUIÇÕES", 28, y3 + 22, 2, fill="#888"))
    mx = max([c for _, c in days] + [1])
    shades = ["#161616", "#444", "#777", "#aaa", "#fff"]
    for wi, w in enumerate(weeks):
        g = []
        for d in w["contributionDays"]:
            c = d["contributionCount"]
            lvl = 0 if c == 0 else min(4, 1 + int(3 * c / mx + 0.5))
            dow = datetime.date.fromisoformat(d["date"]).isoweekday() % 7
            g.append(f'<rect x="{gx + wi * cell:g}" y="{y3 + 44 + dow * cell}" width="{cell - 3}" height="{cell - 3}" fill="{shades[lvl]}"/>')
        b.append(f'<g class="s" style="animation-delay:{.2 + wi * .03:.2f}s">{"".join(g)}</g>')
    legend_y = y3 + 44 + 7 * cell + 10
    b.append(txt(28, legend_y + 10, f"Atualizado em {datetime.date.today().strftime('%d/%m/%Y')}", fill="#666", size=11))
    lx = W - 28 - 5 * cell - 70
    b.append(txt(lx - 6, legend_y + 10, "menos", fill="#666", size=11, anchor="end"))
    for i, s in enumerate(shades):
        b.append(f'<rect x="{lx + i * cell}" y="{legend_y}" width="{cell - 3}" height="{cell - 3}" fill="{s}"/>')
    b.append(txt(lx + 5 * cell + 4, legend_y + 10, "mais", fill="#666", size=11))

    h = y3 + h3
    save("registro.svg", svg(h, "".join(b), "".join(css),
                             f"Registro de aventura: {cal['totalContributions']} contribuições no último ano, sequência atual de {cur} dias"))


if __name__ == "__main__":
    registro(fetch())
    print("registro.svg gerado")
