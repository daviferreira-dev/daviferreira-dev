#!/usr/bin/env python3
"""Gera os SVGs animados (estilo RPG retrô, preto e branco) do perfil de Davi Ferreira."""
import os, textwrap

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)
W = 800
MONO = "Consolas, 'DejaVu Sans Mono', 'Courier New', monospace"
CW = 15 * 0.55  # largura aproximada de um caractere monoespaçado em 15px

# ---------------------------------------------------------------- fonte pixel 5x7
G = {
 "A":"01110 10001 10001 11111 10001 10001 10001", "B":"11110 10001 10001 11110 10001 10001 11110",
 "C":"01110 10001 10000 10000 10000 10001 01110", "D":"11110 10001 10001 10001 10001 10001 11110",
 "E":"11111 10000 10000 11110 10000 10000 11111", "F":"11111 10000 10000 11110 10000 10000 10000",
 "G":"01110 10001 10000 10111 10001 10001 01111", "H":"10001 10001 10001 11111 10001 10001 10001",
 "I":"01110 00100 00100 00100 00100 00100 01110", "J":"00111 00010 00010 00010 00010 10010 01100",
 "K":"10001 10010 10100 11000 10100 10010 10001", "L":"10000 10000 10000 10000 10000 10000 11111",
 "M":"10001 11011 10101 10101 10001 10001 10001", "N":"10001 10001 11001 10101 10011 10001 10001",
 "O":"01110 10001 10001 10001 10001 10001 01110", "P":"11110 10001 10001 11110 10000 10000 10000",
 "Q":"01110 10001 10001 10001 10101 10010 01101", "R":"11110 10001 10001 11110 10100 10010 10001",
 "S":"01111 10000 10000 01110 00001 00001 11110", "T":"11111 00100 00100 00100 00100 00100 00100",
 "U":"10001 10001 10001 10001 10001 10001 01110", "V":"10001 10001 10001 10001 10001 01010 00100",
 "W":"10001 10001 10001 10101 10101 10101 01010", "X":"10001 10001 01010 00100 01010 10001 10001",
 "Y":"10001 10001 01010 00100 00100 00100 00100", "Z":"11111 00001 00010 00100 01000 10000 11111",
 "0":"01110 10001 10011 10101 11001 10001 01110", "1":"00100 01100 00100 00100 00100 00100 01110",
 "2":"01110 10001 00001 00010 00100 01000 11111", "3":"11110 00001 00001 01110 00001 00001 11110",
 "4":"00010 00110 01010 10010 11111 00010 00010", "5":"11111 10000 11110 00001 00001 10001 01110",
 "6":"00110 01000 10000 11110 10001 10001 01110", "7":"11111 00001 00010 00100 01000 01000 01000",
 "8":"01110 10001 10001 01110 10001 10001 01110", "9":"01110 10001 10001 01111 00001 00010 01100",
 " ":"00000 00000 00000 00000 00000 00000 00000", "·":"00000 00000 00000 00100 00000 00000 00000",
 ":":"00000 00100 00100 00000 00100 00100 00000", "!":"00100 00100 00100 00100 00100 00000 00100",
 "?":"01110 10001 00001 00010 00100 00000 00100", "-":"00000 00000 00000 11111 00000 00000 00000",
 ".":"00000 00000 00000 00000 00000 00000 00100", "/":"00001 00001 00010 00100 01000 10000 10000",
 "+":"00000 00100 00100 11111 00100 00100 00000", "&":"01100 10010 10100 01000 10101 10010 01101",
 "▶":"10000 11000 11100 11110 11100 11000 10000", "★":"00100 00100 11111 01110 01010 10001 00000",
 "✓":"00000 00001 00010 10100 01000 00000 00000", "(":"00010 00100 01000 01000 01000 00100 00010",
 ")":"01000 00100 00010 00010 00010 00100 01000", "º":"01100 10010 01100 00000 00000 00000 00000",
}
G = {k: [int(r, 2) for r in v.split()] for k, v in G.items()}
ACC = {"Á": ("A", "acute"), "É": ("E", "acute"), "Í": ("I", "acute"), "Ó": ("O", "acute"), "Ú": ("U", "acute"),
       "Ã": ("A", "tilde"), "Õ": ("O", "tilde"), "Â": ("A", "circ"), "Ê": ("E", "circ"), "Ô": ("O", "circ"), "Ç": ("C", "ced")}
MARK = {"acute": {-2: 0b00010, -1: 0b00100}, "tilde": {-2: 0b01101, -1: 0b10110},
        "circ": {-2: 0b00100, -1: 0b01010}, "ced": {7: 0b00100, 8: 0b01100}}


def tw(s, px):
    return (len(s) * 6 - 1) * px


def glyph_path(ch, x, y, px):
    base, mark = (ACC[ch] if ch in ACC else (ch, None))
    rows = {r: b for r, b in enumerate(G.get(base, G[" "]))}
    if mark: rows.update(MARK[mark])
    d = []
    for r, bits in rows.items():
        c = 0
        while c < 5:
            if bits >> (4 - c) & 1:
                a = c
                while c < 5 and bits >> (4 - c) & 1: c += 1
                d.append(f"M{x + a * px:g} {y + r * px:g}h{(c - a) * px:g}v{px:g}h-{(c - a) * px:g}z")
            else:
                c += 1
    return "".join(d)


def ptext(s, x, y, px, fill="#fff", anchor="start", cls="", per_char_cls=None):
    """Texto em pixel. per_char_cls(i) devolve uma classe por letra (para animações letra a letra)."""
    s = s.upper()
    if anchor == "middle": x -= tw(s, px) / 2
    elif anchor == "end": x -= tw(s, px)
    if per_char_cls:
        out = []
        for i, ch in enumerate(s):
            if ch == " ": continue
            out.append(f'<path class="{per_char_cls(i)}" fill="{fill}" d="{glyph_path(ch, x + i * 6 * px, y, px)}"/>')
        return "".join(out)
    d = "".join(glyph_path(ch, x + i * 6 * px, y, px) for i, ch in enumerate(s))
    c = f' class="{cls}"' if cls else ""
    return f'<path{c} fill="{fill}" d="{d}"/>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, fill="#aaa", size=15, anchor="start", extra=""):
    return (f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" fill="{fill}" font-family="{MONO}" '
            f'font-size="{size}" {extra}>{esc(s)}</text>')


def svg(h, body, css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
            f'shape-rendering="crispEdges" role="img"><title>{esc(title)}</title>'
            f'<style>{css}</style><rect width="{W}" height="{h}" fill="#000"/>{body}</svg>')


def header(title):
    lx = 46 + tw(title.upper(), 2)
    return (f'<rect x="8" y="7" width="8" height="8" fill="#fff" transform="rotate(45 12 11)"/>'
            f'{ptext(title, 30, 4, 2)}'
            f'<rect x="{lx}" y="9" width="{W - 4 - lx}" height="2" fill="#fff"/>'
            f'<rect x="{lx}" y="13" width="{W - 4 - lx}" height="2" fill="#555"/>')


def window(x, y, w, h):
    return (f'<rect x="{x + 1.5:g}" y="{y + 1.5:g}" width="{w - 3:g}" height="{h - 3:g}" fill="#000" stroke="#fff" stroke-width="3"/>'
            f'<rect x="{x + 7:g}" y="{y + 7:g}" width="{w - 14:g}" height="{h - 14:g}" fill="none" stroke="#555" stroke-width="1.5"/>')


def dash(x1, x2, y):
    return f'<line x1="{x1:g}" y1="{y}" x2="{x2:g}" y2="{y}" stroke="#333" stroke-width="1.5" stroke-dasharray="3 4"/>'


def tag(x, y, label, px=2, solid=True, cls=""):
    """Caixinha com texto pixel (alinhada pela direita em x)."""
    w = tw(label.upper(), px) + 14
    h = 7 * px + 12
    c = f' class="{cls}"' if cls else ""
    col = "#fff" if solid else "#666"
    return (f'<g{c}><rect x="{x - w + 1:g}" y="{y + 1:g}" width="{w - 2:g}" height="{h - 2:g}" fill="#000" stroke="{col}" stroke-width="2"/>'
            f'{ptext(label, x - w + 7, y + 6, px, fill=col)}</g>')


def ttag(x, y, label, size=12):
    w = len(label) * size * 0.6 + 16
    return (f'<rect x="{x - w + 1:g}" y="{y + 1:g}" width="{w - 2:g}" height="22" fill="#000" stroke="#fff" stroke-width="2"/>'
            f'{txt(x - w / 2, y + 16, label, fill="#fff", size=size, anchor="middle")}')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- sprite do robô
ROBOT = """
.......#.......
......###......
.......#.......
..###########..
..#.........#..
..#..EE.EE..#..
..#..EE.EE..#..
..#.........#..
..#...MMM...#..
..###########..
.....#...#.....
.#############.
.#.#.......#.#.
.#.#..LLL..#.#.
.#.#.......#.#.
...#########...
....##...##....
...###...###...
"""


def robot(x, y, px):
    rows = [r for r in ROBOT.strip("\n").split("\n")]
    body, eyes, mouth, light, ant = [], [], [], [], []
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch == ".": continue
            rect = f"M{x + c * px:g} {y + r * px:g}h{px:g}v{px:g}h-{px:g}z"
            if r < 3: ant.append(rect)
            elif ch == "E": eyes.append(rect)
            elif ch == "M": mouth.append(rect)
            elif ch == "L": light.append(rect)
            else: body.append(rect)
    w, h = len(rows[0]) * px, len(rows) * px
    return (f'<g class="bob">'
            f'<path class="ant" fill="#fff" d="{"".join(ant)}"/>'
            f'<path fill="#fff" d="{"".join(body)}"/>'
            f'<rect x="{x + 3 * px:g}" y="{y + 4 * px:g}" width="{9 * px:g}" height="{5 * px:g}" fill="#000"/>'
            f'<path class="eye" fill="#fff" d="{"".join(eyes)}"/>'
            f'<path fill="#aaa" d="{"".join(mouth)}"/>'
            f'<path class="core" fill="#fff" d="{"".join(light)}"/>'
            f'</g>'), w, h


ROBOT_CSS = (
    "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}"
    ".bob{animation:bob 1.6s steps(2) infinite}"
    "@keyframes eye{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}"
    ".eye{transform-box:fill-box;transform-origin:center;animation:eye 4s infinite}"
    "@keyframes ant{0%,100%{opacity:1}50%{opacity:.25}}.ant{animation:ant 1s steps(1) infinite}"
    "@keyframes core{0%,100%{fill:#fff}50%{fill:#555}}.core{animation:core 2s steps(1) infinite}"
)


# ---------------------------------------------------------------- 1. banner
def banner():
    h = 230
    css = [ROBOT_CSS,
           "@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}",
           "@keyframes pop{0%{opacity:0;transform:translateY(-12px)}60%{opacity:1;transform:translateY(2px)}100%{opacity:1;transform:translateY(0)}}",
           "@keyframes bl{50%{opacity:0}}.blink{animation:bl 1s steps(1) infinite}",
           "@keyframes up{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(-140px);opacity:0}}",
           "@keyframes spin{to{transform:rotate(360deg)}}",
           "@keyframes xp{0%{width:0}100%{width:260px}}.xp{animation:xp 3s 1.6s steps(26) forwards;width:0}",
           "@keyframes fade{from{opacity:0}to{opacity:1}}.sub{opacity:0;animation:fade .01s 1.4s forwards}",
           ".ch{opacity:0;animation:pop .35s forwards}"]
    b = []
    # moldura
    b.append(f'<rect x="3" y="3" width="{W - 6}" height="{h - 6}" fill="none" stroke="#fff" stroke-width="3"/>')
    b.append(f'<rect x="9" y="9" width="{W - 18}" height="{h - 18}" fill="none" stroke="#555" stroke-width="1.5"/>')
    # estrelas
    stars = [(40, 30), (120, 60), (210, 25), (300, 190), (380, 40), (470, 195), (560, 28), (640, 70), (720, 35),
             (760, 180), (690, 200), (250, 120), (150, 190), (520, 120), (330, 80), (610, 150), (430, 160), (95, 120)]
    for i, (sx, sy) in enumerate(stars):
        s = 3 if i % 3 else 4
        b.append(f'<rect x="{sx}" y="{sy}" width="{s}" height="{s}" fill="#fff" style="animation:tw {1.6 + (i % 5) * .5:.1f}s {(i % 7) * .3:.1f}s steps(2) infinite"/>')
    # engrenagens / chips subindo (tema robótica)
    for i, gx in enumerate([215, 255, 735, 770, 235]):
        dur, delay = 5 + i % 3, i * 1.1
        b.append(f'<g style="animation:up {dur}s {delay:.1f}s linear infinite;opacity:0">'
                 f'<g style="transform-box:fill-box;transform-origin:center;animation:spin 3s steps(8) infinite">'
                 f'<rect x="{gx}" y="200" width="10" height="10" fill="none" stroke="#666" stroke-width="2"/>'
                 f'<rect x="{gx + 4}" y="196" width="2" height="4" fill="#666"/><rect x="{gx + 4}" y="210" width="2" height="4" fill="#666"/>'
                 f'<rect x="{gx - 4}" y="204" width="4" height="2" fill="#666"/><rect x="{gx + 10}" y="204" width="4" height="2" fill="#666"/>'
                 f'</g></g>')
    # chão + robô
    b.append('<rect x="40" y="186" width="150" height="4" fill="#fff"/><rect x="40" y="192" width="150" height="2" fill="#555"/>')
    r, rw, rh = robot(60, 186 - 18 * 6, 6)
    b.append(r)
    # balão
    b.append('<g class="sub"><rect x="140" y="40" width="96" height="26" fill="#000" stroke="#fff" stroke-width="2"/>'
             '<rect x="146" y="64" width="6" height="6" fill="#fff"/>'
             f'{ptext("OLÁ!", 152, 46, 2)}<rect x="210" y="48" width="12" height="10" fill="#fff" class="blink"/></g>')
    # título
    cx = 500
    b.append(ptext("PLAYER 1 · ESTÁGIO NA SOLUCX", cx, 30, 2, fill="#aaa", anchor="middle"))
    name = "DAVI FERREIRA"
    b.append(ptext(name, cx, 64, 5, anchor="middle", per_char_cls=lambda i: f"ch c{i}"))
    css += [f".c{i}{{animation-delay:{.15 + i * .08:.2f}s}}" for i in range(len(name))]
    b.append(f'<g class="sub">{ptext("FULL STACK DEVELOPER", cx, 118, 2, anchor="middle")}'
             f'{ptext("REACT · TYPESCRIPT · PHP · PYTHON", cx, 140, 2, fill="#888", anchor="middle")}</g>')
    # barra EXP
    b.append(f'<g class="sub">{ptext("EXP", 300, 172, 2, fill="#aaa")}'
             f'<rect x="340" y="168" width="264" height="18" fill="#000" stroke="#fff" stroke-width="2"/>'
             f'<rect class="xp" x="342" y="170" height="14" fill="#fff"/>'
             f'{ptext("PRESS START", 622, 172, 2, cls="blink")}</g>')
    save("banner.svg", svg(h, "".join(b), "".join(css), "Davi Ferreira — Full Stack Developer"))


# ---------------------------------------------------------------- 2. botões
def button(name, label, icon):
    w = tw(label, 2) + 52
    h = 30
    body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="#000" stroke="#fff" stroke-width="2"/>'
            f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" fill="none" stroke="#555" stroke-width="1"/>'
            f'{icon}{ptext(label, 36, 8, 2)}')
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" shape-rendering="crispEdges" role="img">'
           f'<title>{label}</title><style>@keyframes bl{{50%{{opacity:0}}}}.bl{{animation:bl 1.2s steps(1) infinite}}</style>'
           f'<rect width="{w}" height="{h}" fill="#000"/>{body}</svg>')
    save(name, out)


def buttons():
    ln = ('<rect x="12" y="8" width="14" height="14" fill="#fff"/>'
          '<rect x="15" y="14" width="2" height="6" fill="#000"/><rect x="15" y="10" width="2" height="2" fill="#000"/>'
          '<rect x="19" y="14" width="2" height="6" fill="#000"/><rect x="21" y="14" width="2" height="2" fill="#000"/><rect x="23" y="16" width="2" height="4" fill="#000"/>')
    mail = ('<rect x="11" y="9" width="16" height="12" fill="none" stroke="#fff" stroke-width="2"/>'
            '<path d="M12 10l7 6l7-6" fill="none" stroke="#fff" stroke-width="2"/>'
            '<rect class="bl" x="24" y="6" width="4" height="4" fill="#fff"/>')
    pin = ('<rect x="14" y="6" width="10" height="2" fill="#fff"/><rect x="12" y="8" width="14" height="8" fill="#fff"/>'
           '<rect x="17" y="10" width="4" height="4" fill="#000"/><rect x="14" y="16" width="10" height="2" fill="#fff"/>'
           '<rect x="16" y="18" width="6" height="2" fill="#fff"/><rect class="bl" x="18" y="20" width="2" height="4" fill="#fff"/>')
    button("btn-linkedin.svg", "LINKEDIN", ln)
    button("btn-email.svg", "E-MAIL", mail)
    button("btn-local.svg", "TAUBATÉ · SP", pin)


# ---------------------------------------------------------------- typing helper
def typed_lines(lines, x, y0, lh, start=0.4, speed=0.011, fill="#ccc", size=15):
    """Revela linhas em sequência, como diálogo de RPG (cobertura preta que desliza em steps)."""
    out, css, t = [], [], start
    for i, (s, col) in enumerate(lines):
        y = y0 + i * lh
        n = max(len(s), 1)
        dur = n * speed
        wpx = n * size * 0.6 + 12
        out.append(txt(x, y, s, fill=col or fill, size=size))
        out.append(f'<rect x="{x - 2:g}" y="{y - size:g}" width="{wpx:g}" height="{size + 6}" fill="#000" '
                   f'style="transform-box:fill-box;transform-origin:right;animation:rev {dur:.2f}s {t:.2f}s steps({n}) forwards"/>')
        t += dur + 0.1
    css.append("@keyframes rev{to{transform:scaleX(0)}}")
    return "".join(out), "".join(css), t


# ---------------------------------------------------------------- 3. sobre mim
def sobre():
    paras = [
        ("Olá, eu sou o Davi Ferreira!", "#fff"),
        None,
        ("Minha jornada na tecnologia não começou apenas digitando código em uma tela, mas projetando lógicas complexas em competições de robótica. Hoje, aplico esse mesmo pensamento sistêmico e capacidade de resolução de problemas no desenvolvimento de software full stack.", None),
        None,
        ("Foram 2 anos como Jovem Aprendiz de TI na cpi | Tegus, com escopo ampliado: suporte técnico, infraestrutura e desenvolvimento de software. Isso me deu uma visão holística que vai da infraestrutura até a experiência final do usuário.", None),
        None,
        ("Hoje sou Estagiário em Suporte Técnico na SoluCX, no time de Employee Experience, e curso Análise e Desenvolvimento de Sistemas no SENAI São Paulo. Busco oportunidades como Desenvolvedor Júnior para aplicar e expandir minhas habilidades full stack.", None),
    ]
    lines = []
    for p in paras:
        if p is None: lines.append(("", None)); continue
        for l in textwrap.wrap(p[0], 80): lines.append((l, p[1]))
    lh = 22
    h = 30 + 30 + len(lines) * lh + 30
    body, css, t = typed_lines(lines, 28, 82, lh)
    last_y = 82 + (len(lines) - 1) * lh
    cur = (f'<rect class="cur" x="760" y="{last_y + 6}" width="12" height="8" fill="#fff"/>')
    css += ("@keyframes bl{50%{opacity:0}}@keyframes on{to{opacity:1}}"
            f".cur{{opacity:0;animation:on .01s {t:.2f}s forwards,bl 1s {t:.2f}s steps(1) infinite}}")
    b = header("SOBRE MIM") + window(0, 30, W, h - 30) + body + cur
    save("sobre-mim.svg", svg(h, b, css, "Sobre mim"))


# ---------------------------------------------------------------- 4. ficha
def ficha():
    cells = [("CLASSE", "Desenvolvedor Full Stack"), ("ESPECIALIDADE", "Criador de Produtos Digitais"),
             ("QUEST ATUAL", "Estagiário em Suporte Técnico · SoluCX"), ("BASE", "Taubaté · SP"),
             ("GUILDA", "ADS (Superior) · SENAI SP · até 2027"), ("ORIGEM", "STEM · Robótica (FLL, TBR, OBR)")]
    rows = (len(cells) + 1) // 2
    by = 56 + rows * 60
    h = by + 86
    b = [header("FICHA DO PERSONAGEM"), window(0, 30, W, h - 30)]
    for i, (k, v) in enumerate(cells):
        x = 28 if i % 2 == 0 else 440
        y = 56 + (i // 2) * 60
        b.append(ptext(k, x, y, 2, fill="#888"))
        b.append(txt(x, y + 38, v, fill="#fff"))
    b.append(ptext("VISÃO HOLÍSTICA", 28, by, 2))
    stages = ["INFRA", "SUPORTE", "ARQUITETURA", "PRODUTO", "UX"]
    seg = (W - 56 - 4 * 6) / 5
    css = ["@keyframes fill{from{opacity:0}to{opacity:1}}", "@keyframes bl{50%{opacity:0}}"]
    for i, s in enumerate(stages):
        x = 28 + i * (seg + 6)
        b.append(f'<rect x="{x:g}" y="{by + 24}" width="{seg:g}" height="16" fill="#222"/>')
        b.append(f'<rect x="{x:g}" y="{by + 24}" width="{seg:g}" height="16" fill="#fff" style="opacity:0;animation:fill .01s {0.6 + i * .45:.2f}s forwards"/>')
        b.append(txt(x + seg / 2, by + 58, s, fill="#888", size=12, anchor="middle"))
    b.append(ptext("▶", W - 28 - 10, by, 2, fill="#fff", cls="cur"))
    css.append(".cur{animation:bl 1s steps(1) infinite}")
    save("ficha.svg", svg(h, "".join(b), "".join(css), "Ficha do personagem"))


# ---------------------------------------------------------------- 5. habilidades
def habilidades():
    skills = [
        ("VISÃO DE PRODUTO", "Não escrevo apenas código; eu traduzo regras de negócios complexas em interfaces acessíveis e eficientes."),
        ("TROUBLESHOOTING", "Anos de competições STEM e robótica me treinaram para debugar sistemas sob pressão e encontrar soluções otimizadas."),
        ("MENTALIDADE DE ENGENHARIA", "Entendo a stack inteira. Seja projetando um banco de dados relacional ou construindo um frontend reativo, foco em performance e manutenibilidade."),
    ]
    b, y = [], 54
    rows_y = []
    for i, (name, desc) in enumerate(skills):
        rows_y.append(y)
        b.append(ptext(name, 56, y, 2))
        for j, l in enumerate(textwrap.wrap(desc, 78)):
            b.append(txt(56, y + 38 + j * 20, l))
        y += 38 + len(textwrap.wrap(desc, 78)) * 20 + 14
        if i < len(skills) - 1:
            b.append(dash(28, W - 28, y - 6))
            y += 10
    h = y + 10
    # cursor que percorre as habilidades
    n = len(rows_y)
    kf = []
    for i, ry in enumerate(rows_y):
        a, z = i * 100 / n, (i + 1) * 100 / n - 0.01
        kf.append(f"{a:.2f}%,{z:.2f}%{{transform:translateY({ry - rows_y[0]}px)}}")
    css = (f"@keyframes sel{{{''.join(kf)}}}.sel{{animation:sel 6s steps(1) infinite}}"
           "@keyframes bl{50%{opacity:0}}.bl{animation:bl .5s steps(1) infinite}")
    cursor = f'<g class="sel"><g class="bl">{ptext("▶", 30, rows_y[0], 2)}</g></g>'
    b = header("HABILIDADES ESPECIAIS") + window(0, 30, W, h - 30) + "".join(b) + cursor
    save("habilidades.svg", svg(h, b, css, "Habilidades especiais: visão de produto, troubleshooting, mentalidade de engenharia"))


# ---------------------------------------------------------------- 6. inventário
def inventario():
    groups = [
        ("FRONTEND & MOBILE", ["React", "TypeScript", "JavaScript", "React Flow", "Tailwind CSS", "React Native", "Framer Motion", "HTML5 / CSS3"],
         "SPAs dinâmicas, interfaces baseadas em grafos e apps multiplataforma"),
        ("BACKEND & APIS", ["Node.js", "PHP", "Laravel", "Python", "API REST"],
         "APIs RESTful, processamento assíncrono e regras de negócio"),
        ("DADOS & INFRA", ["MySQL", "MongoDB", "Supabase", "Docker", "Firebase", "AWS", "Linux"],
         "Modelagem relacional/não-relacional, conteinerização, cloud e deploy ágil"),
        ("IA · DADOS · HARDWARE", ["Machine Learning", "Power BI", "Gemini", "Arduino", "C++", "Redes LAN/WAN"],
         "Modelos preditivos, análise de dados, LLMs, robótica e redes (CCNA)"),
        ("WORKFLOW & QUALIDADE", ["Git", "GitHub", "Vitest", "Scrum", "Kanban"],
         "Versionamento rigoroso, testes e entregas iterativas alinhadas ao produto"),
    ]
    b, css = [], ["@keyframes pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:scale(1)}}",
                  ".it{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .3s forwards}"]
    y, k = 52, 0
    for gi, (name, items, ctx) in enumerate(groups):
        b.append(ptext(name, 28, y, 2, fill="#888"))
        x, ry = 28, y + 24
        for it in items:
            w = len(it) * 8.3 + 22
            if x + w > W - 28:
                x, ry = 28, ry + 36
            b.append(f'<g class="it" style="animation-delay:{.3 + k * .08:.2f}s">'
                     f'<rect x="{x + 1:g}" y="{ry:g}" width="{w - 2:g}" height="28" fill="#000" stroke="#fff" stroke-width="2"/>'
                     f'{txt(x + w / 2, ry + 19, it, fill="#fff", size=14, anchor="middle")}</g>')
            x += w + 8
            k += 1
        b.append(txt(28, ry + 50, ctx, fill="#777", size=13))
        y = ry + 72
        if gi < len(groups) - 1: b.append(dash(28, W - 28, y - 12))
    h = y + 4
    b = header("INVENTÁRIO") + window(0, 30, W, h - 30) + "".join(b)
    save("inventario.svg", svg(h, b, "".join(css), "Inventário de tecnologias"))


# ---------------------------------------------------------------- 7. missão principal
def missao():
    b = []
    b.append(ptext("AUTO ABOUT", 28, 56, 4))
    b.append(txt(28, 112, "Motor de Automação No-Code (WhatsApp + IA)", fill="#fff"))
    b.append(tag(W - 28, 52, "★ DESTAQUE", cls="bl"))
    b.append(txt(28, 136, "Líder de desenvolvimento · chatbot personalizável para fluxos de mensagem no WhatsApp,", fill="#888", size=14))
    b.append(txt(28, 156, "voltado para pequenas e médias empresas, com programação visual (no-code) e IA.", fill="#888", size=14))
    rows = [
        ("DESAFIO", "Desenvolver uma interface onde usuários sem conhecimento técnico pudessem orquestrar automações de alta complexidade."),
        ("SOLUÇÃO", "Interface drag-and-drop fluida com React Flow. No backend, um motor em Node.js que lê e processa os nós visuais, traduzindo-os em árvores de decisão executáveis. Integra a API do Gemini para respostas dinâmicas."),
        ("IMPACTO", "Redução drástica na curva de aprendizado para criação de bots, democratizando o acesso à automação inteligente."),
    ]
    y = 180
    css = ["@keyframes bl{50%{opacity:0}}.bl{animation:bl 1.2s steps(1) infinite}",
           "@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}",
           ".row{opacity:0;animation:in .4s forwards}"]
    for i, (k, v) in enumerate(rows):
        b.append(dash(28, W - 28, y))
        wl = textwrap.wrap(v, 66)
        g = [ptext(k, 28, y + 16, 2, fill="#aaa")]
        for j, l in enumerate(wl):
            g.append(txt(170, y + 29 + j * 20, l, fill="#ddd"))
        b.append(f'<g class="row" style="animation-delay:{.4 + i * .5:.1f}s">{"".join(g)}</g>')
        y += 22 + len(wl) * 20 + 8
    b.append(dash(28, W - 28, y))
    y += 14
    x = 28
    for t in ["REACT FLOW", "NODE.JS", "GEMINI API", "WHATSAPP"]:
        w = tw(t, 2) + 14
        b.append(tag(x + w, y, t, solid=False))
        x += w + 8
    h = y + 26 + 24
    out = header("MISSÃO PRINCIPAL") + window(0, 30, W, h - 30) + "".join(b)
    save("missao.svg", svg(h, out, "".join(css), "Missão principal: Auto About — motor de automação no-code"))


# ---------------------------------------------------------------- 7b. diário de missões
def missoes():
    quests = [
        ("Kash · controle financeiro a partir do extrato", "SIDE PROJECT",
         "Importa extratos CSV sem duplicar lançamentos, categoriza gastos e aprende com novas categorias, detecta gastos recorrentes e avisa quando um orçamento está perto do limite.",
         ["REACT", "TYPESCRIPT", "TAILWIND", "FRAMER MOTION", "VITEST"]),
        ("Modelo de risco de FPD · Science Hackathon by TMB", "3º LUGAR",
         "Machine Learning para prever o risco de não pagamento da primeira parcela ainda no checkout, com 90 mil+ registros reais: feature engineering, desbalanceamento, validação temporal e segmentação de risco.",
         ["PYTHON", "MACHINE LEARNING", "DADOS"]),
        ("Monitoramento automatizado de preços na web · Workshop", "PALESTRANTE",
         "Workshop na Semana Tecnológica do SENAI Taubaté sobre web scraping, automação, armazenamento e análise de dados. 2º melhor workshop e 2º melhor projeto.",
         ["PYTHON", "WEB SCRAPING", "AUTOMAÇÃO"]),
        ("Site interativo sobre a norma ISA-101 · Automação Industrial", "SENAI",
         "Vídeo e site sobre design de interfaces homem-máquina: comparador antes/depois arrastável, painel HMI por nível de cor, gráfico de tempo de resposta a falhas e quiz.",
         ["WEB", "IHM / HMI", "UX"]),
    ]
    css = ["@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}",
           ".q{opacity:0;animation:in .4s forwards}",
           "@keyframes bl{50%{opacity:0}}.bl{animation:bl 1s steps(1) infinite}"]
    b, y = [], 50
    for i, (title, badge, desc, tags) in enumerate(quests):
        g = [ptext("▶", 28, y + 4, 2, cls="bl") if i == 0 else ptext("◇" if False else "-", 28, y + 4, 2, fill="#666"),
             txt(52, y + 16, title, fill="#fff"), ttag(W - 28, y, badge)]
        wl = textwrap.wrap(desc, 84)
        for j, l in enumerate(wl):
            g.append(txt(52, y + 40 + j * 19, l, fill="#999", size=13))
        ty = y + 40 + len(wl) * 19 - 6
        x = 52
        for t in tags:
            w = tw(t, 1) + 14
            g.append(f'<rect x="{x + 1}" y="{ty + 1}" width="{w - 2}" height="17" fill="#000" stroke="#555" stroke-width="2"/>{ptext(t, x + 7, ty + 5, 1, fill="#888")}')
            x += w + 6
        b.append(f'<g class="q" style="animation-delay:{.3 + i * .4:.1f}s">{"".join(g)}</g>')
        y = ty + 34
        if i < len(quests) - 1:
            b.append(dash(28, W - 28, y - 10))
            y += 6
    h = y + 6
    out = header("DIÁRIO DE MISSÕES") + window(0, 30, W, h - 30) + "".join(b)
    save("missoes.svg", svg(h, out, "".join(css), "Diário de missões: Kash, modelo de risco de FPD, workshop de monitoramento de preços e site ISA-101"))


# ---------------------------------------------------------------- 8. conquistas
TROPHY = ["#######", "#######", ".#####.", "..###..", "...#...", "..###..", ".#####."]


def trophy(x, y, px):
    d = "".join(f"M{x + c * px} {y + r * px}h{px}v{px}h-{px}z"
                for r, line in enumerate(TROPHY) for c, ch in enumerate(line) if ch == "#")
    return f'<path fill="#fff" d="{d}"/>'


def conquistas():
    items = [
        ("TBR · Torneio Brasil de Robótica", "AVALIADOR · 2022-2023",
         "2 temporadas avaliando o desempenho técnico dos robôs e a lógica de programação."),
        ("FIRST LEGO League", "MENTOR 2023 · COMPETIDOR 2022",
         "Design mecânico e lógica de missões autônomas (SuperPowered e Masterpiece)."),
        ("OBR 2023 · Olimpíada Brasileira de Robótica", "COMPETIDOR · PRÁTICA",
         "Etapa regional de São José dos Campos: robótica móvel e algoritmos sob pressão."),
        ("XVII MOBFOG · Mostra Brasileira de Foguetes", "BRONZE + MENÇÃO HONROSA",
         "Construção e lançamento de foguetes com alta performance de alcance (OBA, 2023)."),
        ("4º Science Hackathon by TMB", "3º LUGAR",
         "Modelo de ML para prever risco de FPD com 90 mil+ registros reais (2026)."),
        ("Semana Tecnológica · SENAI Taubaté", "2º WORKSHOP · 2º PROJETO",
         "Palestrante no workshop de monitoramento automatizado de preços na web."),
        ("Grand Prix SENAI de Inovação", "PARTICIPANTE · BRASÍLIA",
         "Soluções colaborativas para desafios reais da indústria (abril de 2026)."),
    ]
    b = [txt(28, 62, "Base analítica forjada em desafios práticos e competições nacionais de alto nível.", fill="#888", size=14)]
    css = ["@keyframes un{0%{opacity:0}40%{opacity:1}55%{opacity:.3}70%,100%{opacity:1}}",
           ".u{opacity:0;animation:un .7s forwards}",
           "@keyframes fl{0%{opacity:0}30%{opacity:1}100%{opacity:0}}",
           ".fl{opacity:0;animation:fl .6s forwards}"]
    y = 82
    for i, (name, role, desc) in enumerate(items):
        d = .4 + i * .45
        b.append(f'<g class="u" style="animation-delay:{d:.2f}s">'
                 f'<rect x="28" y="{y}" width="44" height="44" fill="#000" stroke="#fff" stroke-width="2"/>{trophy(32 + 4, y + 8, 4)}'
                 f'{txt(88, y + 16, name, fill="#fff")}'
                 f'{txt(88, y + 36, desc, fill="#888", size=13)}</g>')
        b.append(f'<g class="u" style="animation-delay:{d + .2:.2f}s">{ttag(W - 28, y - 4, role)}</g>')
        b.append(f'<rect class="fl" x="28" y="{y}" width="{W - 56}" height="44" fill="#fff" style="animation-delay:{d:.2f}s"/>')
        y += 60
    h = y + 10
    out = header("CONQUISTAS DESBLOQUEADAS") + window(0, 30, W, h - 30) + "".join(b)
    save("conquistas.svg", svg(h, out, "".join(css), "Conquistas: TBR, FIRST LEGO League, OBR 2023, MOBFOG bronze, 3º lugar Science Hackathon by TMB, 2º lugar workshop SENAI, Grand Prix SENAI"))


# ---------------------------------------------------------------- 8b. certificados
SCROLL = ["######.", "#....#.", "#.##.#.", "#....#.", "#.##.#.", "#....##", "######."]


def certificados():
    certs = [
        ("Gemini Academy 2026 · IA no Workspace", "Google · 2026"),
        ("AWS Academy Cloud Foundations", "Amazon Web Services · 2026"),
        ("JavaScript Essentials 1", "Cisco · 2026"),
        ("Introduction to Modern AI", "Cisco · 2026"),
        ("Data Analytics Essentials", "Cisco · 2026"),
        ("Linux Unhatched", "Cisco · 2026"),
        ("Load Balancing on Compute Engine", "Google · skill badge · 2026"),
        ("CCNA v7 Introduction to Networks", "SENAI São Paulo"),
        ("Fundamentos do Python", "SENAI São Paulo · 2025"),
        ("Power BI", "SENAI São Paulo · 2024"),
        ("Arduino", "SENAI São Paulo"),
        ("Pacote Office", "SENAI São Paulo · 2021"),
    ]
    css = ["@keyframes pop{0%{opacity:0;transform:translateY(6px)}100%{opacity:1;transform:none}}",
           ".c{opacity:0;animation:pop .35s forwards}"]
    icon = lambda x, y: '<path fill="#fff" d="' + "".join(
        f"M{x + c * 3} {y + r * 3}h3v3h-3z" for r, l in enumerate(SCROLL) for c, ch in enumerate(l) if ch == "#") + '"/>'
    b = [txt(28, 62, f"{len(certs)} itens raros coletados em cursos e trilhas oficiais.", fill="#888", size=14)]
    y0 = 82
    for i, (name, who) in enumerate(certs):
        col, row = i % 2, i // 2
        x, y = 28 + col * 380, y0 + row * 50
        b.append(f'<g class="c" style="animation-delay:{.3 + i * .12:.2f}s">{icon(x, y + 4)}'
                 f'{txt(x + 32, y + 16, name, fill="#fff", size=14)}{txt(x + 32, y + 34, who, fill="#777", size=12)}</g>')
    h = y0 + ((len(certs) + 1) // 2) * 50 + 8
    out = header("GRIMÓRIO DE CERTIFICADOS") + window(0, 30, W, h - 30) + "".join(b)
    save("certificados.svg", svg(h, out, "".join(css), "Certificados: Google, AWS, Cisco e SENAI São Paulo"))


# ---------------------------------------------------------------- 9. mapa da jornada
def mapa():
    nodes = [("ROBÓTICA", "STEM", "2022-23", "done"), ("TÉCNICO", "ADS", "SENAI · 2024-25", "done"),
             ("JOVEM", "APRENDIZ", "TI · 2024-26", "done"), ("ESTÁGIO", "SOLUCX", "ATUAL", "now"),
             ("SYSTEM", "DESIGN", "", "next"), ("ENGENHARIA", "DE IA", "", "next")]
    xs = [82 + i * 127 for i in range(len(nodes))]
    cur = 3
    py = 110
    h = 320
    b = [f'<line x1="{xs[0]}" y1="{py}" x2="{xs[cur]}" y2="{py}" stroke="#fff" stroke-width="4"/>',
         f'<line x1="{xs[cur]}" y1="{py}" x2="{xs[-1]}" y2="{py}" stroke="#555" stroke-width="4" stroke-dasharray="8 8"/>']
    dist = xs[cur] - xs[0]
    css = ["@keyframes bl{50%{opacity:0}}.bl{animation:bl 1s steps(1) infinite}",
           f"@keyframes walk{{0%{{transform:translateX(0)}}100%{{transform:translateX({dist}px)}}}}",
           f".walk{{animation:walk 3.5s .3s steps({dist // 10}) forwards}}",
           "@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.25)}}",
           ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 1s steps(2) infinite}"]
    for (a, c, yr, st), x in zip(nodes, xs):
        if st == "done":
            b.append(f'<rect x="{x - 14}" y="{py - 14}" width="28" height="28" fill="#fff"/>{ptext("✓", x - 5, py - 6, 2, fill="#000")}')
        elif st == "now":
            b.append(f'<rect class="pulse" x="{x - 16}" y="{py - 16}" width="32" height="32" fill="#000" stroke="#fff" stroke-width="4"/>')
            b.append(f'<rect x="{x - 6}" y="{py - 6}" width="12" height="12" fill="#fff" class="bl"/>')
        else:
            b.append(f'<rect x="{x - 14}" y="{py - 14}" width="28" height="28" fill="#000" stroke="#666" stroke-width="2"/>{ptext("?", x - 5, py - 7, 2, fill="#666")}')
        col = "#fff" if st != "next" else "#888"
        b.append(ptext(a, x, py + 30, 2, fill=col, anchor="middle"))
        b.append(ptext(c, x, py + 50, 2, fill=col, anchor="middle"))
        if yr:
            b.append(txt(x, py + 86, yr, fill=("#fff" if st == "now" else "#777"), size=12, anchor="middle"))
    mini, _, _ = robot(xs[0] - 15, py - 70, 2)
    b.append(f'<g class="walk">{mini}</g>')
    b.append(dash(28, W - 28, 216))
    b.append(ptext("PRÓXIMAS FASES", 28, 230, 2, fill="#888"))
    b.append(txt(28, 268, "System Design & Arquitetura: de monólitos para integrações robustas e microsserviços.", fill="#ddd", size=14))
    b.append(txt(28, 292, "Engenharia de IA: integração de LLMs (como o Gemini) em aplicações AI-first.", fill="#ddd", size=14))
    out = header("MAPA DA JORNADA") + window(0, 30, W, h - 30) + "".join(b)
    save("mapa.svg", svg(h, out, ROBOT_CSS + "".join(css), "Mapa da jornada: Robótica STEM, Técnico em ADS no SENAI, Jovem Aprendiz de TI, Estágio na SoluCX (atual), System Design e Engenharia de IA"))


# ---------------------------------------------------------------- 10. continue
def cont():
    h = 240
    css = ["@keyframes bl{50%{opacity:0}}.bl{animation:bl 1s steps(1) infinite}"]
    b = [ptext("CONTINUE?", W / 2, 48, 6, anchor="middle", cls="bl")]
    for n in range(10):
        a, z = n * 10, n * 10 + 10
        css.append(f"@keyframes n{n}{{0%,{a}%{{opacity:0}}{a + .01}%,{z}%{{opacity:1}}{z + .01}%,100%{{opacity:0}}}}")
        b.append(f'<g style="opacity:0;animation:n{n} 10s steps(1) infinite">{ptext(str(9 - n), W / 2, 106, 3, fill="#888", anchor="middle")}</g>')
    b.append(txt(W / 2, 160, "Vamos construir algo juntos?", fill="#fff", size=16, anchor="middle"))
    b.append(txt(W / 2, 184, "Buscando oportunidades como Desenvolvedor Júnior.", fill="#ccc", size=13, anchor="middle"))
    b.append(txt(W / 2, 204, "Arquitetura de software, automação ou uma nova oportunidade profissional:", fill="#888", size=13, anchor="middle"))
    b.append(txt(W / 2, 222, "minha caixa de entrada está aberta.", fill="#888", size=13, anchor="middle"))
    save("continue.svg", svg(h, "".join(b), "".join(css), "Continue? Vamos construir algo juntos? Buscando oportunidades como Desenvolvedor Júnior"))


# ---------------------------------------------------------------- 11. rodapé
def rodape():
    h = 140
    quote = "“Engenharia de software não é apenas sobre escrever código,"
    quote2 = "é sobre traduzir problemas complexos em soluções elegantes.”"
    b = [f'<rect x="3" y="3" width="{W - 6}" height="{h - 6}" fill="none" stroke="#fff" stroke-width="3"/>',
         f'<rect x="9" y="9" width="{W - 18}" height="{h - 18}" fill="none" stroke="#555" stroke-width="1.5"/>',
         txt(W / 2, 40, quote, fill="#ccc", size=14, anchor="middle", extra='font-style="italic"'),
         txt(W / 2, 60, quote2, fill="#ccc", size=14, anchor="middle", extra='font-style="italic"'),
         ptext("SALVANDO JOGO", 220, 88, 2, fill="#aaa"),
         '<rect x="400" y="84" width="180" height="18" fill="#000" stroke="#fff" stroke-width="2"/>',
         '<rect class="sv" x="402" y="86" height="14" fill="#fff"/>',
         f'<g class="ok">{ptext("✓ SALVO", 596, 88, 2)}</g>',
         txt(W / 2, 124, "OBRIGADO POR VISITAR · DAVI FERREIRA", fill="#666", size=12, anchor="middle")]
    css = ("@keyframes sv{0%{width:0}60%,100%{width:176px}}.sv{animation:sv 5s steps(16) infinite}"
           "@keyframes ok{0%,59%{opacity:0}60%,100%{opacity:1}}.ok{animation:ok 5s steps(1) infinite}")
    save("rodape.svg", svg(h, "".join(b), css, "Obrigado por visitar — jogo salvo"))


def registro_titulo():
    save("registro.svg", svg(22, header("REGISTRO DE AVENTURA"), "", "Registro de aventura: estatísticas do GitHub"))


if __name__ == "__main__":
    for f in (banner, buttons, sobre, ficha, habilidades, inventario, missao, missoes, conquistas, certificados, mapa, cont, rodape):
        f()
    print("ok:", sorted(os.listdir(OUT)))
