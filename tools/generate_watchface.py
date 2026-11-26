import math, os

C = 225
S = 450 / 400.0  # Scale from 400x400 SVG to 450x450 Wear OS WFF v3
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app", "src", "main", "res") + os.sep

def argb(hexrgb, a=255):
    return f"#{a:02X}{hexrgb.lstrip('#').upper()}"

f = lambda x: f"{x:.2f}".rstrip("0").rstrip(".")

# ---------------- Themes from Three Lens Watch Face HTML ----------------
# (id, label, face_bg, bezel, ink_txt, dim_txt, acc_sec, acc_dim)
THEMES = [
    ("mono",       "Mono",        "131313", "2B2B2B", "E6E6E6", "8A8A8A", "E6E6E6", "7A7A7A"),
    ("oled",       "OLED Black",  "000000", "1C1C1C", "F2F2F2", "7A7A7A", "F2F2F2", "7A7A7A"),
    ("metro",      "Metro",       "17171B", "2C2C33", "EBE7DC", "9D9A92", "FA6800", "B9632F"),
    ("catppuccin", "Catppuccin",  "1E1E2E", "313244", "CDD6F4", "7F849C", "CBA6F7", "7B6A9C"),
    ("gruvbox",    "Gruvbox",     "282828", "3C3836", "EBDBB2", "928374", "FE8019", "AF5F14"),
    ("nord",       "Nord",        "2E3440", "3B4252", "ECEFF4", "7B88A1", "88C0D0", "5E81AC"),
    ("tokyonight", "Tokyo Night", "1A1B26", "292E42", "C0CAF5", "565F89", "7AA2F7", "4D6AA8"),
    ("dracula",    "Dracula",     "282A36", "44475A", "F8F8F2", "6272A4", "FF79C6", "A14D82"),
    ("rosepine",   "Rose Pine",   "191724", "26233A", "E0DEF4", "6E6A86", "EB6F92", "9A475F"),
    ("everforest", "Everforest",  "2D353B", "3D484D", "D3C6AA", "859289", "A7C080", "5F7A4B"),
    ("solarized",  "Solarized",   "002B36", "073642", "93A1A1", "586E75", "B58900", "7A5E00"),
    ("m3purple",   "M3 Purple",   "141317", "2B2930", "E6E1E7", "948F9A", "D0BCFF", "7B6A9C"),
    ("m3blue",     "M3 Blue",     "121317", "282A30", "E3E2E7", "8E909A", "AAC7FF", "5E76A8"),
    ("m3teal",     "M3 Teal",     "0F1413", "252B2A", "DFE3E1", "889390", "6DD5C5", "3E8E82"),
    ("m3green",    "M3 Green",    "111410", "272B26", "E1E3DC", "8C9387", "86D993", "4E8F59"),
    ("m3rose",     "M3 Rose",     "181213", "312729", "EDDFE1", "9F8C90", "FFB1C8", "A16275"),
    ("m3amber",    "M3 Amber",    "18120D", "312820", "ECE0D7", "9D8E7F", "FFB95C", "A36E27"),
]

# ---------------- 6 Weights & 6 Widths (carefully chosen apt values) ----------------
# 6 Weight options: Thin (100), Extra Light (200), Light (300), Medium (500), Bold (700), Black (900 via bold+outline)
WEIGHTS = [
    ("gsr_thin",       0, "Thin",        None),
    ("gsr_extralight", 1, "Extra light", None),
    ("gsr_light",      2, "Light",       None),
    ("gsr_medium",     3, "Medium",      None),
    ("gsr_bold",       4, "Bold",        None),
    ("gsr_bold",       5, "Black",       "1.3"),
]

# 6 Width options: apt horizontal scale factors for radial & upright dial rings
WIDTH_VALS = [0.74, 0.86, 1.00, 1.13, 1.26, 1.40]
WIDTH_NAMES = [
    "Ultra condensed",
    "Condensed",
    "Normal",
    "Semi expanded",
    "Expanded",
    "Ultra expanded",
]

LISTS = [
    ("num_weight", "Font weight",       4, [w[2] for w in WEIGHTS]),
    ("num_width",  "Font width",        2, WIDTH_NAMES),
    ("hour_mode",  "Hours orientation", 0, ["Upright", "Radial", "Pointing"]),
    ("ring_mode",  "Min/Sec orientation", 0, ["Radial", "Pointing"]),
    ("bg_mode",    "Background",        0, ["Theme color", "Pure black"]),
    ("glass_str",  "Diopter refraction", 2, ["Subtle", "Balanced", "Strong"]),
    ("aod_style",  "Always-on style",   0, ["Three lenses", "Chunky stack", "Activity rings", "Minutes pie", "Minimal slit"]),
    ("aod_bright", "Always-on brightness", 0, ["Dim", "Normal"]),
]

strings = {
    "app_name": "Three Lens",
    "cfg_palette": "Theme",
}

uc = []
# Each ColorOption has max 5 colors in WFF v3:
# 0: face_bg, 1: bezel, 2: ink_txt, 3: dim_txt, 4: acc_sec
uc.append('    <ColorConfiguration id="palette" displayName="cfg_palette" defaultValue="0">')
for i, (k, label, face, bezel, ink, dim, acc, accd) in enumerate(THEMES):
    strings["pal_" + k] = label
    cols = " ".join([argb(face), argb(bezel), argb(ink), argb(dim), argb(acc)])
    uc.append(f'      <ColorOption id="{i}" displayName="pal_{k}" colors="{cols}"/>')
uc.append("    </ColorConfiguration>")

for cid, label, dflt, opts in LISTS:
    strings["cfg_" + cid] = label
    uc.append(f'    <ListConfiguration id="{cid}" displayName="cfg_{cid}" defaultValue="{dflt}">')
    for j, o in enumerate(opts):
        strings[f"{cid}_{j}"] = o
        uc.append(f'      <ListOption id="{j}" displayName="{cid}_{j}"/>')
    uc.append("    </ListConfiguration>")

FL = [
    ("f_lenses",  0),
    ("f_stack",   1),
    ("f_rings",   2),
    ("f_pie",     3),
    ("f_minimal", 4),
]
FLAVORS = '    <Flavors defaultValue="f_lenses">\n' + "\n".join(
    f'      <Flavor id="{fid}" displayName="aod_style_{ak}"><Configuration id="aod_style" optionId="{ak}"/></Flavor>'
    for fid, ak in FL
) + "\n    </Flavors>"
uc.append(FLAVORS)
USERCFG = "  <UserConfigurations>\n" + "\n".join(uc) + "\n  </UserConfigurations>"

# Color references
BG    = "[CONFIGURATION.palette.0]"
BEZEL = "[CONFIGURATION.palette.1]"
TXT   = "[CONFIGURATION.palette.2]"
DIMT  = "[CONFIGURATION.palette.3]"
ACC   = "[CONFIGURATION.palette.4]"

def cfg(i): return f"[CONFIGURATION.{i}]"
def sel(i, k, on=255): return f'{cfg(i)} == "{k}" ? {on} : 0'
def tern(i, vals):
    s = str(vals[-1])
    for k in range(len(vals) - 2, -1, -1):
        s = f'({cfg(i)} == "{k}" ? {vals[k]} : {s})'
    return s

WIDTH_EXPR = tern("num_width", WIDTH_VALS)

# Dial radii scaled from 400x400 HTML (RH=58, RM=118, RS=165) to 450x450
RH = 58 * S     # 65.25
RM = 118 * S    # 132.75
RS = 165 * S    # 185.625

# Smooth time angle expressions matching Three Lens Watch Face HTML
ANG_H = "(([HOUR_0_11]%12)*30)"
ANG_M = "(([MINUTE]+[SECOND_MILLISECOND]/60)*6)"
E_S   = "clamp(fract([SECOND_MILLISECOND])/0.35,0,1)"
ANG_S = f"(([SECOND]-pow(1-{E_S},3))*6)"

n = [0]
def nm(p):
    n[0] += 1
    return f"{p}{n[0]}"

def pt(deg, r):
    a = math.radians(deg)
    return C + math.sin(a) * r, C - math.cos(a) * r

def radial_rot(deg):
    d = deg % 360
    return d + 90 if (180 < d < 360) else d - 90

# ---------------- Multi-weight & multi-width text helpers ----------------
def weight_font_nodes(prefix, w, h, size, col, text_body, minor_fast=False):
    """Generates font-weight PartText layers inside a local numeral Group."""
    nodes = []
    if minor_fast:
        tiers = [
            ("gsr_extralight", f'({cfg("num_weight")} == "0" || {cfg("num_weight")} == "1") ? 255 : 0'),
            ("gsr_medium",     f'({cfg("num_weight")} == "2" || {cfg("num_weight")} == "3") ? 255 : 0'),
            ("gsr_bold",       f'({cfg("num_weight")} == "4" || {cfg("num_weight")} == "5") ? 255 : 0'),
        ]
        for fam, a_expr in tiers:
            nodes.append(
                f'          <PartText name="{nm(prefix)}" x="0" y="0" width="{w}" height="{h}">'
                f"<Transform target=\"alpha\" value='{a_expr}'/>"
                f'<Text align="CENTER"><Font family="{fam}" size="{size}" color="{col}">{text_body}</Font></Text></PartText>'
            )
        return "\n".join(nodes)
    for fam, wk, _, out_w in WEIGHTS:
        a_expr = sel("num_weight", wk)
        inner = f'<Outline color="{col}" width="{out_w}">{text_body}</Outline>' if out_w else text_body
        nodes.append(
            f'          <PartText name="{nm(prefix)}" x="0" y="0" width="{w}" height="{h}">'
            f"<Transform target=\"alpha\" value='{a_expr}'/>"
            f'<Text align="CENTER"><Font family="{fam}" size="{size}" color="{col}">{inner}</Font></Text></PartText>'
        )
    return "\n".join(nodes)

def dial_numeral(deg, r, text_str, size, box_w, box_h, col, angle_expr=None, static_angle=0, minor_fast=False):
    cx, cy = pt(deg, r)
    x = round(cx - box_w / 2)
    y = round(cy - box_h / 2)
    px = f"{(cx - x) / box_w:.4f}"
    py = f"{(cy - y) / box_h:.4f}"
    ang_attr = f' angle="{f(static_angle)}"' if (angle_expr is None and static_angle != 0) else ""
    ang_tf = f'\n          <Transform target="angle" value=\'{angle_expr}\'/>' if angle_expr else ""
    return (
        f'        <Group name="{nm("ng")}" x="{x}" y="{y}" width="{box_w}" height="{box_h}" pivotX="{px}" pivotY="{py}"{ang_attr}>{ang_tf}\n'
        f"          <Transform target=\"scaleX\" value='{WIDTH_EXPR}'/>\n"
        f'{weight_font_nodes("nt", box_w, box_h, size, col, text_str, minor_fast=minor_fast)}\n'
        f'        </Group>'
    )

# ---------------- Batched fixed index rings (Hour, Minute, Second) ----------------
def build_fixed_rings():
    out = []
    # Subtle concentric track bands (matching HTML band(gH,RH,56,.05), band(gM,RM,46,.04), band(gS,RS,38,.05))
    out.append(
        f'      <PartDraw name="ring_bands" x="0" y="0" width="450" height="450">'
        f'<Ellipse x="{f(C-RH)}" y="{f(C-RH)}" width="{f(2*RH)}" height="{f(2*RH)}"><Stroke color="#10FFFFFF" thickness="{f(56*S)}"/></Ellipse>'
        f'<Ellipse x="{f(C-RM)}" y="{f(C-RM)}" width="{f(2*RM)}" height="{f(2*RM)}"><Stroke color="#0CFFFFFF" thickness="{f(46*S)}"/></Ellipse>'
        f'<Ellipse x="{f(C-RS)}" y="{f(C-RS)}" width="{f(2*RS)}" height="{f(2*RS)}"><Stroke color="#10FFFFFF" thickness="{f(38*S)}"/></Ellipse>'
        f'</PartDraw>'
    )

    # 1. Hour ring (1..12) with dynamic hour_mode (0: Upright, 1: Radial, 2: Pointing)
    h_nodes = []
    for h in range(1, 13):
        deg = h * 30
        r_rot = radial_rot(deg)
        ang_expr = f'({cfg("hour_mode")} == "0" ? 0 : ({cfg("hour_mode")} == "1" ? {r_rot} : {deg}))'
        h_nodes.append(dial_numeral(deg, RH, str(h), 17, 36, 26, TXT, angle_expr=ang_expr))
    out.append('      <Group name="ringH" x="0" y="0" width="450" height="450">\n' + "\n".join(h_nodes) + "\n      </Group>")

    # 2. Minute ring (00..59 numerals + batched outer ticks)
    m_nodes = []
    m_maj_ticks = []
    m_min_ticks = []
    for m in range(60):
        deg = m * 6
        five = (m % 5 == 0)
        r_rot = radial_rot(deg)
        ang_expr = f'({cfg("ring_mode")} == "0" ? {r_rot} : {deg})'
        col = TXT if five else DIMT
        m_nodes.append(dial_numeral(deg, RM, f"{m:02d}", 10.5, 26, 18, col, angle_expr=ang_expr, minor_fast=not five))
        # Outer minute ticks (HTML: 134..141 major, 136..141 minor)
        x1, y1 = pt(deg, (134 if five else 136) * S)
        x2, y2 = pt(deg, 141 * S)
        line = f'<Line startX="{f(x1)}" startY="{f(y1)}" endX="{f(x2)}" endY="{f(y2)}"><Stroke color="{TXT}" thickness="{f((1.6 if five else 1.0)*S)}" cap="BUTT"/></Line>'
        (m_maj_ticks if five else m_min_ticks).append(line)
    out.append(
        '      <Group name="ringM" x="0" y="0" width="450" height="450">\n'
        + "\n".join(m_nodes) + "\n"
        + f'        <PartDraw name="ringM_tmin" x="0" y="0" width="450" height="450" alpha="95">{"".join(m_min_ticks)}</PartDraw>\n'
        + f'        <PartDraw name="ringM_tmaj" x="0" y="0" width="450" height="450" alpha="205">{"".join(m_maj_ticks)}</PartDraw>\n'
        + "      </Group>"
    )

    # 3. Second ring (00..59 numerals + batched outer ticks)
    s_nodes = []
    s_maj_ticks = []
    s_min_ticks = []
    for s_idx in range(60):
        deg = s_idx * 6
        five = (s_idx % 5 == 0)
        r_rot = radial_rot(deg)
        ang_expr = f'({cfg("ring_mode")} == "0" ? {r_rot} : {deg})'
        col = ACC if five else DIMT
        s_nodes.append(dial_numeral(deg, RS, f"{s_idx:02d}", 11, 26, 18, col, angle_expr=ang_expr, minor_fast=not five))
        # Outer second ticks (HTML: 176..184 major, 178..184 minor)
        x1, y1 = pt(deg, (176 if five else 178) * S)
        x2, y2 = pt(deg, 184 * S)
        line = f'<Line startX="{f(x1)}" startY="{f(y1)}" endX="{f(x2)}" endY="{f(y2)}"><Stroke color="{ACC}" thickness="{f((2.0 if five else 1.1)*S)}" cap="BUTT"/></Line>'
        (s_maj_ticks if five else s_min_ticks).append(line)
    out.append(
        '      <Group name="ringS" x="0" y="0" width="450" height="450">\n'
        + "\n".join(s_nodes) + "\n"
        + f'        <PartDraw name="ringS_tmin" x="0" y="0" width="450" height="450" alpha="115">{"".join(s_min_ticks)}</PartDraw>\n'
        + f'        <PartDraw name="ringS_tmaj" x="0" y="0" width="450" height="450" alpha="240">{"".join(s_maj_ticks)}</PartDraw>\n'
        + "      </Group>"
    )
    return "\n".join(out)

# ---------------- Frameless Light-Bending Glass Diopter Slits ----------------
def make_glass_slit(lid, R, hw, hl, ang_expr, zoomed_inner_xml):
    """
    Pure frameless glass diopter slit that orbits at radius R with angle ang_expr.
    Uses renderMode="MASK" to clip the magnified index and applies only optical glass
    refraction layers (edge vignette, radial caustic dome bend, meniscus sheen, and
    translucent specular rim) with zero opaque colored borders.
    """
    lx = f(C - hw)
    ly = f(C - R - hl)
    lw = f(2 * hw)
    lh = f(2 * hl)
    cr = f(hw)
    cy = f(C - R)
    glass_alpha = tern("glass_str", [145, 210, 255])
    return f'''      <Group name="lens_{lid}_orbit" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">
        <Transform target="angle" value='{ang_expr}'/>
        <PartDraw name="lens_{lid}_shadow" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(C-hw+2)}" y="{f(C-R-hl+4)}" width="{lw}" height="{lh}" cornerRadiusX="{cr}" cornerRadiusY="{cr}"><Fill color="#48000000"/></RoundRectangle></PartDraw>
        <Group name="lens_{lid}_clip" x="0" y="0" width="450" height="450">
          <PartDraw name="lens_{lid}_mask" x="0" y="0" width="450" height="450" renderMode="MASK"><RoundRectangle x="{lx}" y="{ly}" width="{lw}" height="{lh}" cornerRadiusX="{cr}" cornerRadiusY="{cr}"><Fill color="#FFFFFFFF"/></RoundRectangle></PartDraw>
          <PartDraw name="lens_{lid}_bg_theme" x="0" y="0" width="450" height="450" renderMode="SOURCE"><Rectangle x="{f(C-hw-2)}" y="{f(C-R-hl-2)}" width="{f(2*hw+4)}" height="{f(2*hl+4)}"><Fill color="{BG}"/></Rectangle></PartDraw>
          <PartDraw name="lens_{lid}_bg_black" x="0" y="0" width="450" height="450" renderMode="SOURCE"><Transform target="alpha" value='{sel("bg_mode", 1)}'/><Rectangle x="{f(C-hw-2)}" y="{f(C-R-hl-2)}" width="{f(2*hw+4)}" height="{f(2*hl+4)}"><Fill color="#FF000000"/></Rectangle></PartDraw>
          <PartDraw name="lens_{lid}_band" x="0" y="0" width="450" height="450" renderMode="SOURCE"><Rectangle x="{f(C-hw-2)}" y="{f(C-R-hl-2)}" width="{f(2*hw+4)}" height="{f(2*hl+4)}"><Fill color="#12FFFFFF"/></Rectangle></PartDraw>
          <Group name="lens_{lid}_mag" x="0" y="0" width="450" height="450" renderMode="SOURCE">
{zoomed_inner_xml}
          </Group>
          <Group name="lens_{lid}_optics" x="0" y="0" width="450" height="450" renderMode="SOURCE">
            <Transform target="alpha" value='{glass_alpha}'/>
            <PartDraw name="lens_{lid}_caustic" x="0" y="0" width="450" height="450"><RoundRectangle x="{lx}" y="{ly}" width="{lw}" height="{lh}" cornerRadiusX="{cr}" cornerRadiusY="{cr}"><Fill color="#00FFFFFF"><RadialGradient centerX="{f(C-hw*0.18)}" centerY="{f(C-R-hl*0.22)}" radius="{f(hl*1.12)}" colors="#04FFFFFF #16FFFFFF #3CFFFFFF" positions="0 0.68 1"/></Fill></RoundRectangle></PartDraw>
            <PartDraw name="lens_{lid}_vignette" x="0" y="0" width="450" height="450"><RoundRectangle x="{lx}" y="{ly}" width="{lw}" height="{lh}" cornerRadiusX="{cr}" cornerRadiusY="{cr}"><Stroke color="#78000000" thickness="4.5"/></RoundRectangle></PartDraw>
            <PartDraw name="lens_{lid}_meniscus" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(C-hw+2.5)}" y="{f(C-R-hl+2)}" width="{f(2*hw-5)}" height="{f(hl*0.85)}" cornerRadiusX="{f(hw-2.5)}" cornerRadiusY="{f(hw*0.55)}"><Fill color="#00FFFFFF"><LinearGradient startX="225" startY="{f(C-R-hl+2)}" endX="225" endY="{cy}" colors="#38FFFFFF #10FFFFFF #00FFFFFF" positions="0 0.55 1"/></Fill></RoundRectangle></PartDraw>
            <PartDraw name="lens_{lid}_spec" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(C-hw+0.8)}" y="{f(C-R-hl+0.8)}" width="{f(2*hw-1.6)}" height="{f(2*hl-1.6)}" cornerRadiusX="{f(hw-0.8)}" cornerRadiusY="{f(hw-0.8)}"><Stroke color="#FFFFFFFF" thickness="1.5"><LinearGradient startX="{lx}" startY="{ly}" endX="{f(C+hw)}" endY="{f(C-R+hl)}" colors="#99FFFFFF #22FFFFFF #08FFFFFF #55FFFFFF" positions="0 0.3 0.7 1"/></Stroke></RoundRectangle></PartDraw>
          </Group>
        </Group>
      </Group>'''

def build_three_lenses():
    # 1. Hour lens (RH=65.25, hw=18.5, hl=35.5, mag=1.65x -> font size 28)
    bw_h, bh_h = 54, 42
    xh = round(C - bw_h / 2)
    yh = round(C - RH - bh_h / 2)
    # In lens_H_orbit local frame (already rotated by ANG_H):
    # - Upright (hour_mode==0): counter-rotate by -ANG_H so numeral stays upright on screen
    # - Radial (hour_mode==1): +90 on left half (180..360), -90 on right half (0..180)
    # - Pointing (hour_mode==2): 0 (points radially outward along lens axis)
    h_rot_local = f'({cfg("hour_mode")} == "0" ? -({ANG_H}) : ({cfg("hour_mode")} == "1" ? (({ANG_H}) &gt; 180 &amp;&amp; ({ANG_H}) &lt; 360 ? 90 : -90) : 0))'
    h_body = '<Template>%d<Parameter expression="[HOUR_1_12]"/></Template>'
    zoom_h = (
        f'            <Group name="z_h_grp" x="{xh}" y="{yh}" width="{bw_h}" height="{bh_h}" pivotX="0.5" pivotY="0.5">\n'
        f"              <Transform target=\"angle\" value='{h_rot_local}'/>\n"
        f"              <Transform target=\"scaleX\" value='{WIDTH_EXPR}'/>\n"
        f'{weight_font_nodes("zh", bw_h, bh_h, 28, TXT, h_body)}\n'
        f'            </Group>'
    )
    lens_h = make_glass_slit("H", RH, 18.5, 35.5, ANG_H, zoom_h)

    # 2. Minute lens (RM=132.75, hw=14.5, hl=31, mag=2.15x -> font size 23)
    bw_m, bh_m = 48, 36
    xm = round(C - bw_m / 2)
    ym = round(C - RM - bh_m / 2)
    m_rot_local = f'({cfg("ring_mode")} == "0" ? (([MINUTE] &gt; 30) ? 90 : -90) : 0)'
    m_body = '<Template>%s<Parameter expression="[MINUTE_Z]"/></Template>'
    # Magnified outer minute tick at top of minute lens (r = 150.75..158.6 scaled around RM)
    mt_y1 = f(C - RM - (134 * S - RM) * 1.45)
    mt_y2 = f(C - RM - (141 * S - RM) * 1.45)
    zoom_m = (
        f'            <PartDraw name="z_m_tick" x="0" y="0" width="450" height="450"><Line startX="225" startY="{mt_y1}" endX="225" endY="{mt_y2}"><Stroke color="{TXT}" thickness="2.6" cap="ROUND"/></Line></PartDraw>\n'
        f'            <Group name="z_m_grp" x="{xm}" y="{ym}" width="{bw_m}" height="{bh_m}" pivotX="0.5" pivotY="0.5">\n'
        f"              <Transform target=\"angle\" value='{m_rot_local}'/>\n"
        f"              <Transform target=\"scaleX\" value='{WIDTH_EXPR}'/>\n"
        f'{weight_font_nodes("zm", bw_m, bh_m, 23, TXT, m_body)}\n'
        f'            </Group>'
    )
    lens_m = make_glass_slit("M", RM, 14.5, 31.0, ANG_M, zoom_m)

    # 3. Second lens (RS=185.625, hw=12, hl=23.5, mag=1.90x -> font size 21)
    bw_s, bh_s = 44, 34
    xs = round(C - bw_s / 2)
    ys = round(C - RS - bh_s / 2)
    s_rot_local = f'({cfg("ring_mode")} == "0" ? (([SECOND] &gt; 30) ? 90 : -90) : 0)'
    s_body = '<Template>%s<Parameter expression="[SECOND_Z]"/></Template>'
    st_y1 = f(C - RS - (176 * S - RS) * 1.35)
    st_y2 = f(C - RS - (184 * S - RS) * 1.35)
    zoom_s = (
        f'            <PartDraw name="z_s_tick" x="0" y="0" width="450" height="450"><Line startX="225" startY="{st_y1}" endX="225" endY="{st_y2}"><Stroke color="{ACC}" thickness="3" cap="ROUND"/></Line></PartDraw>\n'
        f'            <Group name="z_s_grp" x="{xs}" y="{ys}" width="{bw_s}" height="{bh_s}" pivotX="0.5" pivotY="0.5">\n'
        f"              <Transform target=\"angle\" value='{s_rot_local}'/>\n"
        f"              <Transform target=\"scaleX\" value='{WIDTH_EXPR}'/>\n"
        f'{weight_font_nodes("zs", bw_s, bh_s, 21, ACC, s_body)}\n'
        f'            </Group>'
    )
    lens_s = make_glass_slit("S", RS, 12.0, 23.5, ANG_S, zoom_s)

    # Center glass hub (HTML lines 160-165: r=13*1.125=14.6, inner accent pin r=3.6*1.125=4.05)
    hub = (
        f'      <PartDraw name="center_hub" x="0" y="0" width="450" height="450">'
        f'<Ellipse x="210.4" y="210.4" width="29.2" height="29.2"><Fill color="#FF08080A"/></Ellipse>'
        f'<Ellipse x="210.4" y="210.4" width="29.2" height="29.2"><Fill color="#00FFFFFF"><RadialGradient centerX="222" centerY="221" radius="16" colors="#08FFFFFF #1EFFFFFF #42FFFFFF" positions="0 0.7 1"/></Fill></Ellipse>'
        f'<Ellipse x="211.5" y="211.5" width="27" height="27"><Stroke color="#66FFFFFF" thickness="1.3"/></Ellipse>'
        f'<Ellipse x="221" y="221" width="8" height="8"><Fill color="{ACC}"/></Ellipse>'
        f'</PartDraw>'
    )
    return "\n".join([lens_h, lens_m, lens_s, hub])

# ---------------- Background ----------------
BGL = f'''    <PartDraw name="bg_theme" x="0" y="0" width="450" height="450">
      <Variant mode="AMBIENT" target="alpha" value="0"/>
      <Ellipse x="4.5" y="4.5" width="441" height="441"><Fill color="#FF060608"/></Ellipse>
      <Ellipse x="11.25" y="11.25" width="427.5" height="427.5"><Fill color="{BG}"/><Stroke color="{BEZEL}" thickness="2.2"/></Ellipse>
    </PartDraw>
    <PartDraw name="bg_black" x="0" y="0" width="450" height="450">
      <Transform target="alpha" value='{sel("bg_mode", 1)}'/>
      <Rectangle x="0" y="0" width="450" height="450"><Fill color="#FF000000"/></Rectangle>
    </PartDraw>'''

ACTIVE_ROOT = (
    '    <Group name="active_root" x="0" y="0" width="450" height="450">\n'
    '      <Variant mode="AMBIENT" target="alpha" value="0"/>\n'
    + build_fixed_rings() + "\n"
    + build_three_lenses()
    + "\n    </Group>"
)

# ---------------- Always-On Display (AOD) Styles (5 styles, burn-in protected, zero lag) ----------------
SHIFT_X = "(([MINUTE]%5)-2)*2"
SHIFT_Y = "((floor([MINUTE]/5)%5)-2)*2"
DAYP = ["[DAY_OF_WEEK_S]", "[DAY]"]

def hollow(name, x, y, w, h, size, fam, tmpl, params, col, width="3.5", align="CENTER"):
    ps = "".join(f'<Parameter expression="{p}"/>' for p in params)
    return f'        <PartText name="{name}" x="{x}" y="{y}" width="{w}" height="{h}"><Text align="{align}"><Font family="{fam}" size="{size}" color="#00000000"><Outline color="{col}" width="{width}"><Template>{tmpl}{ps}</Template></Outline></Font></Text></PartText>'

def solid(name, x, y, w, h, size, fam, tmpl, params, col, upper=False, ls=None, align="CENTER"):
    if params:
        ps = "".join(f'<Parameter expression="{p}"/>' for p in params)
        t = f"<Template>{tmpl}{ps}</Template>"
    else:
        t = tmpl
    if upper:
        t = f"<Upper>{t}</Upper>"
    l = f' letterSpacing="{ls}"' if ls else ""
    return f'        <PartText name="{name}" x="{x}" y="{y}" width="{w}" height="{h}"><Text align="{align}"><Font family="{fam}" size="{size}" color="{col}"{l}>{t}</Font></Text></PartText>'

def aod_style_group(k, body):
    s_aod = sel("aod_style", k)
    return (
        f'        <Group name="aod_style{k}" x="0" y="0" width="450" height="450">\n'
        f"          <Transform target=\"alpha\" value='{s_aod}'/>\n"
        + body + "\n        </Group>"
    )

# AOD 0: Three lenses AOD (sparse 12-hour + 5-minute index with moving Hour & Minute glass diopter slits)
aod0_idx = []
for h in range(1, 13):
    cx, cy = pt(h * 30, RH)
    aod0_idx.append(f'        <PartText name="aod0_h{h}" x="{round(cx-16)}" y="{round(cy-12)}" width="32" height="24"><Text align="CENTER"><Font family="gsr_bold" size="14" color="{DIMT}">{h}</Font></Text></PartText>')
for m in range(0, 60, 5):
    deg = m * 6
    cx, cy = pt(deg, RM)
    aod0_idx.append(f'        <PartText name="aod0_m{m}" x="{round(cx-15)}" y="{round(cy-11)}" width="30" height="22" pivotX="0.5" pivotY="0.5" angle="{f(radial_rot(deg))}"><Text align="CENTER"><Font family="gsr_bold" size="11" color="{DIMT}">{m:02d}</Font></Text></PartText>')

aod0_lens_h = make_glass_slit(
    "aodH", RH, 18.5, 35.5, ANG_H,
    f'            <Group name="aod_zh_g" x="{round(C-27)}" y="{round(C-RH-21)}" width="54" height="42" pivotX="0.5" pivotY="0.5">\n'
    f"              <Transform target=\"angle\" value='-({ANG_H})'/>\n"
    f'              <PartText name="aod_zh_t" x="0" y="0" width="54" height="42"><Text align="CENTER"><Font family="gsr_bold" size="27" color="{TXT}"><Template>%d<Parameter expression="[HOUR_1_12]"/></Template></Font></Text></PartText>\n'
    f'            </Group>'
)
aod0_lens_m = make_glass_slit(
    "aodM", RM, 14.5, 31.0, "[MINUTE]*6",
    f'            <Group name="aod_zm_g" x="{round(C-24)}" y="{round(C-RM-18)}" width="48" height="36" pivotX="0.5" pivotY="0.5">\n'
    f"              <Transform target=\"angle\" value='([MINUTE] &gt; 30 ? 90 : -90)'/>\n"
    f'              <PartText name="aod_zm_t" x="0" y="0" width="48" height="36"><Text align="CENTER"><Font family="gsr_bold" size="23" color="{ACC}"><Template>%s<Parameter expression="[MINUTE_Z]"/></Template></Font></Text></PartText>\n'
    f'            </Group>'
)
s0 = "\n".join(aod0_idx + [aod0_lens_h, aod0_lens_m])

# AOD 1: Chunky stack (smaller filled bold Hour + huge chunky outline bold Minute + date)
s1 = "\n".join([
    solid("aod1_h", 100, 82, 250, 74, 66, "gsr_bold", "%s", ["[HOUR_1_12_Z]"], TXT),
    hollow("aod1_m", 45, 152, 360, 148, 126, "gsr_bold", "%s", ["[MINUTE_Z]"], ACC, "3.5"),
    solid("aod1_d", 100, 318, 250, 30, 18, "gsr_bold", "%s %d", DAYP, DIMT, True, "0.12"),
])

# AOD 2: Activity rings (3 full-360° bold concentric rings + smaller filled Hour + larger outline Minute)
RING_R = [198, 174, 150]
RING_COLS = ["#FFFA114F", "#FF92E82A", "#FF00E5FF"]
RING_TRK = ["#26FA114F", "#2692E82A", "#2600E5FF"]
RING_EXPRS = [
    "clamp([STEP_PERCENT]/100,0.02,1)",
    "clamp([STEP_COUNT]/7800,0.02,1)",
    "clamp([STEP_COUNT]/6000,0.02,1)",
]
aod2_rings = []
for i, (r, col, tcol, expr) in enumerate(zip(RING_R, RING_COLS, RING_TRK, RING_EXPRS)):
    aod2_rings.append(f'        <PartDraw name="aod2_trk{i}" x="0" y="0" width="450" height="450"><Ellipse x="{C-r}" y="{C-r}" width="{2*r}" height="{2*r}"><Stroke color="{tcol}" thickness="3"/></Ellipse></PartDraw>')
    aod2_rings.append(f'        <PartDraw name="aod2_rng{i}" x="0" y="0" width="450" height="450"><Arc centerX="225" centerY="225" width="{2*r}" height="{2*r}" startAngle="0" endAngle="0" direction="CLOCKWISE"><Transform target="endAngle" value="359.9*({expr})"/><Stroke color="{col}" thickness="13" cap="ROUND"/></Arc></PartDraw>')
s2 = "\n".join(aod2_rings + [
    solid("aod2_h", 125, 118, 200, 62, 54, "gsr_bold", "%s", ["[HOUR_1_12_Z]"], TXT),
    hollow("aod2_m", 95, 174, 260, 108, 94, "gsr_bold", "%s", ["[MINUTE_Z]"], TXT, "3.5"),
    solid("aod2_d", 135, 286, 180, 26, 18, "gsr_bold", "%s %d", DAYP, DIMT, False),
])

# AOD 3: Minutes pie (9 streamlined concentric arcs + chunky filled Hour + large outline Minute + centered step count)
aod3_arcs = []
for r in range(22, 212, 22):
    aod3_arcs.append(f'        <PartDraw name="aod3_a{r}" x="0" y="0" width="450" height="450" alpha="115"><Arc centerX="225" centerY="225" width="{2*r}" height="{2*r}" startAngle="0" endAngle="0" direction="CLOCKWISE"><Transform target="endAngle" value="[MINUTE]*6"/><Stroke color="{ACC}" thickness="2" cap="BUTT"/></Arc></PartDraw>')
aod3_edge = (
    '        <Group name="aod3_edge" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">\n'
    "          <Transform target=\"angle\" value='[MINUTE]*6'/>\n"
    f'          <PartDraw name="aod3_edged" x="0" y="0" width="450" height="450"><Rectangle x="{f(C-1.3)}" y="{C-215}" width="2.6" height="215"><Fill color="{ACC}"/></Rectangle></PartDraw>\n'
    '        </Group>'
)
aod3_start = f'        <PartDraw name="aod3_start" x="0" y="0" width="450" height="450" alpha="115"><Rectangle x="{f(C-1)}" y="{C-215}" width="2" height="215"><Fill color="{ACC}"/></Rectangle></PartDraw>'
s3 = "\n".join(aod3_arcs + [
    aod3_start, aod3_edge,
    solid("aod3_h", 16, 66, 200, 72, 64, "gsr_bold", "%s", ["[HOUR_1_12_Z]"], TXT),
    hollow("aod3_m", 8, 132, 230, 126, 108, "gsr_bold", "%s", ["[MINUTE_Z]"], ACC, "3.5"),
    solid("aod3_steps", 125, 346, 200, 44, 30, "gsr_bold", "%d", ["[STEP_COUNT]"], TXT),
])

# AOD 4: Minimal glass slit (smaller filled bold Hour + larger outline bold Minute framed by a frameless glass slit)
s4_slit = (
    '        <PartDraw name="aod4_slit_caustic" x="0" y="0" width="450" height="450"><RoundRectangle x="115" y="135" width="220" height="150" cornerRadiusX="75" cornerRadiusY="75"><Fill color="#00FFFFFF"><RadialGradient centerX="210" centerY="190" radius="140" colors="#04FFFFFF #12FFFFFF #2CFFFFFF" positions="0 0.7 1"/></Fill></RoundRectangle></PartDraw>\n'
    '        <PartDraw name="aod4_slit_spec" x="0" y="0" width="450" height="450"><RoundRectangle x="115" y="135" width="220" height="150" cornerRadiusX="75" cornerRadiusY="75"><Stroke color="#FFFFFFFF" thickness="1.5"><LinearGradient startX="115" startY="135" endX="335" endY="285" colors="#88FFFFFF #18FFFFFF #06FFFFFF #48FFFFFF" positions="0 0.35 0.7 1"/></Stroke></RoundRectangle></PartDraw>'
)
s4 = "\n".join([
    s4_slit,
    solid("aod4_h", 105, 148, 105, 86, 58, "gsr_bold", "%s", ["[HOUR_1_12_Z]"], TXT, align="END"),
    hollow("aod4_m", 220, 136, 130, 108, 86, "gsr_bold", "%s", ["[MINUTE_Z]"], ACC, "3.2", align="START"),
    solid("aod4_d", 125, 306, 200, 28, 17, "gsr_bold", "%s %d %s", DAYP + ["[MONTH_S]"], DIMT, True, "0.14"),
])

_aod_br_expr = cfg("aod_bright") + ' == "0" ? 140 : 205'
AOD = (
    '    <Group name="aod_root" x="0" y="0" width="450" height="450" alpha="0">\n'
    '      <Variant mode="AMBIENT" target="alpha" value="255"/>\n'
    f'      <Transform target="x" value="{SHIFT_X}"/>\n'
    f'      <Transform target="y" value="{SHIFT_Y}"/>\n'
    '      <Group name="aod_bright" x="0" y="0" width="450" height="450">\n'
    f"        <Transform target=\"alpha\" value='{_aod_br_expr}'/>\n"
    + "\n".join(aod_style_group(k, b) for k, b in enumerate([s0, s1, s2, s3, s4]))
    + "\n      </Group>\n    </Group>"
)

xml = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- Three Lens Watch Face for Wear OS (WFF v3).
     Three concentric fixed numeral/tick rings with orbiting frameless light-bending glass diopter slits.
     Font: Google Sans Flex Rounded (SIL OFL 1.1) - see FONT_LICENSE.txt -->
<WatchFace width="450" height="450">
{USERCFG}
  <Scene backgroundColor="#FF000000">
{BGL}
{ACTIVE_ROOT}
{AOD}
  </Scene>
</WatchFace>
'''

with open(OUT + "raw/watchface.xml", "w", encoding="utf-8") as fh:
    fh.write(xml)

esc = lambda t: t.replace("&", "&amp;").replace("'", "\\'")
with open(OUT + "values/strings.xml", "w", encoding="utf-8") as fh:
    fh.write(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        + "\n".join(f'    <string name="{k}">{esc(v)}</string>' for k, v in strings.items())
        + "\n</resources>\n"
    )

with open(OUT + "xml/watch_face_info.xml", "w", encoding="utf-8") as fh:
    fh.write(
        '<?xml version="1.0" encoding="utf-8"?>\n<WatchFaceInfo>\n'
        '    <Preview value="@drawable/preview" />\n'
        '    <Editable value="true" />\n'
        '    <FlavorsSupported value="true" />\n'
        '    <MultipleInstancesAllowed value="true" />\n'
        '</WatchFaceInfo>\n'
    )

print("watchface.xml", len(xml), "bytes")
