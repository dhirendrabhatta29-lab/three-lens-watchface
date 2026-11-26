import math, os

C = 225
S = 450 / 400.0  # Scale from 400x400 SVG to 450x450 Wear OS WFF v3
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app", "src", "main", "res") + os.sep

def argb(hexrgb, a=255):
    return f"#{a:02X}{hexrgb.lstrip('#').upper()}"

f = lambda x: f"{x:.2f}".rstrip("0").rstrip(".")

# ---------------- 17 Themes from Three Lens Watch Face HTML + M3 ----------------
# (id, label, face_bg, bezel, ink_txt, dim_txt, acc_sec)
THEMES = [
    ("mono",       "Mono",        "131313", "2B2B2B", "E6E6E6", "8A8A8A", "E6E6E6"),
    ("oled",       "OLED Black",  "000000", "1C1C1C", "F2F2F2", "7A7A7A", "F2F2F2"),
    ("metro",      "Metro",       "17171B", "2C2C33", "EBE7DC", "9D9A92", "FA6800"),
    ("catppuccin", "Catppuccin",  "1E1E2E", "313244", "CDD6F4", "7F849C", "CBA6F7"),
    ("gruvbox",    "Gruvbox",     "282828", "3C3836", "EBDBB2", "928374", "FE8019"),
    ("nord",       "Nord",        "2E3440", "3B4252", "ECEFF4", "7B88A1", "88C0D0"),
    ("tokyonight", "Tokyo Night", "1A1B26", "292E42", "C0CAF5", "565F89", "7AA2F7"),
    ("dracula",    "Dracula",     "282A36", "44475A", "F8F8F2", "6272A4", "FF79C6"),
    ("rosepine",   "Rose Pine",   "191724", "26233A", "E0DEF4", "6E6A86", "EB6F92"),
    ("everforest", "Everforest",  "2D353B", "3D484D", "D3C6AA", "859289", "A7C080"),
    ("solarized",  "Solarized",   "002B36", "073642", "93A1A1", "586E75", "B58900"),
    ("m3purple",   "M3 Purple",   "141317", "2B2930", "E6E1E7", "948F9A", "D0BCFF"),
    ("m3blue",     "M3 Blue",     "121317", "282A30", "E3E2E7", "8E909A", "AAC7FF"),
    ("m3teal",     "M3 Teal",     "0F1413", "252B2A", "DFE3E1", "889390", "6DD5C5"),
    ("m3green",    "M3 Green",    "111410", "272B26", "E1E3DC", "8C9387", "86D993"),
    ("m3rose",     "M3 Rose",     "181213", "312729", "EDDFE1", "9F8C90", "FFB1C8"),
    ("m3amber",    "M3 Amber",    "18120D", "312820", "ECE0D7", "9D8E7F", "FFB95C"),
]

# ---------------- 6 Weights & 6 Widths (per-ring individual configurations) ----------------
WEIGHTS = [
    ("gsr_thin",       0, "Thin",        None),
    ("gsr_extralight", 1, "Extra light", None),
    ("gsr_light",      2, "Light",       None),
    ("gsr_medium",     3, "Medium",      None),
    ("gsr_bold",       4, "Bold",        None),
    ("gsr_bold",       5, "Black",       "1.35"),
]
WEIGHT_NAMES = [w[2] for w in WEIGHTS]

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
    ("h_weight",   "Hours weight",        4, WEIGHT_NAMES),
    ("h_width",    "Hours width",         2, WIDTH_NAMES),
    ("m_weight",   "Minutes weight",      4, WEIGHT_NAMES),
    ("m_width",    "Minutes width",       2, WIDTH_NAMES),
    ("s_weight",   "Seconds weight",      3, WEIGHT_NAMES),
    ("s_width",    "Seconds width",       2, WIDTH_NAMES),
    ("hour_mode",  "Hours orientation",   0, ["Upright", "Radial", "Pointing"]),
    ("bg_mode",    "Background",          0, ["Theme color", "Pure black"]),
    ("glass_str",  "Diopter refraction",  2, ["Subtle", "Balanced", "Exaggerated"]),
    ("aod_style",  "Always-on style",     0, ["Dual orbit lenses", "Triple monolith slits", "Eclipse glass ring"]),
    ("aod_bright", "Always-on brightness", 0, ["Dim", "Normal"]),
]

strings = {
    "app_name": "Three Lens",
    "cfg_palette": "Theme",
}

uc = []
uc.append('    <ColorConfiguration id="palette" displayName="cfg_palette" defaultValue="0">')
for i, (k, label, face, bezel, ink, dim, acc) in enumerate(THEMES):
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
    ("f_dual_orbit", 0),
    ("f_monolith",   1),
    ("f_eclipse",    2),
]
FLAVORS = '    <Flavors defaultValue="f_dual_orbit">\n' + "\n".join(
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

H_WIDTH_EXPR = tern("h_width", WIDTH_VALS)
M_WIDTH_EXPR = tern("m_width", WIDTH_VALS)
S_WIDTH_EXPR = tern("s_width", WIDTH_VALS)

# Dial radii scaled from 400x400 HTML (RH=58, RM=118, RS=165) to 450x450
RH = 58 * S     # 65.25
RM = 118 * S    # 132.75
RS = 165 * S    # 185.625

# Smooth continuous motion for Minute and Second diopters; smooth hour transition
ANG_H = "(([HOUR_0_11]%12)*30)"
ANG_M = "(([MINUTE]+[SECOND_MILLISECOND]/60)*6)"
ANG_S = "([SECOND_MILLISECOND]*6)"

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

# ---------------- Per-ring multi-weight & multi-width text helpers ----------------
def weight_font_nodes(prefix, weight_cfg, w, h, size, col, text_body, minor_fast=False):
    """Generates font-weight PartText layers for a specific ring's weight configuration."""
    nodes = []
    if minor_fast:
        tiers = [
            ("gsr_extralight", f'({cfg(weight_cfg)} == "0" || {cfg(weight_cfg)} == "1") ? 255 : 0', None),
            ("gsr_medium",     f'({cfg(weight_cfg)} == "2" || {cfg(weight_cfg)} == "3") ? 255 : 0', None),
            ("gsr_bold",       f'({cfg(weight_cfg)} == "4" || {cfg(weight_cfg)} == "5") ? 255 : 0', "0.9"),
        ]
        for fam, a_expr, out_w in tiers:
            inner = f'<Outline color="{col}" width="{out_w}">{text_body}</Outline>' if (out_w and "5" in a_expr and False) else text_body
            nodes.append(
                f'            <PartText name="{nm(prefix)}" x="0" y="0" width="{w}" height="{h}">'
                f"<Transform target=\"alpha\" value='{a_expr}'/>"
                f'<Text align="CENTER"><Font family="{fam}" size="{size}" color="{col}">{inner}</Font></Text></PartText>'
            )
        return "\n".join(nodes)
    for fam, wk, _, out_w in WEIGHTS:
        a_expr = sel(weight_cfg, wk)
        inner = f'<Outline color="{col}" width="{out_w}">{text_body}</Outline>' if out_w else text_body
        nodes.append(
            f'            <PartText name="{nm(prefix)}" x="0" y="0" width="{w}" height="{h}">'
            f"<Transform target=\"alpha\" value='{a_expr}'/>"
            f'<Text align="CENTER"><Font family="{fam}" size="{size}" color="{col}">{inner}</Font></Text></PartText>'
        )
    return "\n".join(nodes)

def dial_numeral(deg, r, text_str, size, box_w, box_h, col, weight_cfg, width_expr, angle_expr=None, static_angle=0, minor_fast=False):
    cx, cy = pt(deg, r)
    x = round(cx - box_w / 2)
    y = round(cy - box_h / 2)
    px = f"{(cx - x) / box_w:.4f}"
    py = f"{(cy - y) / box_h:.4f}"
    ang_attr = f' angle="{f(static_angle)}"' if (angle_expr is None and static_angle != 0) else ""
    ang_tf = f'\n            <Transform target="angle" value=\'{angle_expr}\'/>' if angle_expr else ""
    return (
        f'          <Group name="{nm("ng")}" x="{x}" y="{y}" width="{box_w}" height="{box_h}" pivotX="{px}" pivotY="{py}"{ang_attr}>{ang_tf}\n'
        f"            <Transform target=\"scaleX\" value='{width_expr}'/>\n"
        f'{weight_font_nodes("nt", weight_cfg, box_w, box_h, size, col, text_str, minor_fast=minor_fast)}\n'
        f'          </Group>'
    )

# ---------------- Ring builders (reused for fixed base dial AND magnified inside diopters) ----------------
def build_hour_ring(group_name, minor_fast=False):
    h_nodes = []
    for h in range(1, 13):
        deg = h * 30
        r_rot = radial_rot(deg)
        ang_expr = f'({cfg("hour_mode")} == "0" ? 0 : ({cfg("hour_mode")} == "1" ? {r_rot} : {deg}))'
        h_nodes.append(dial_numeral(deg, RH, str(h), 16.5, 36, 26, TXT, "h_weight", H_WIDTH_EXPR, angle_expr=ang_expr, minor_fast=minor_fast))
    return f'        <Group name="{group_name}" x="0" y="0" width="450" height="450">\n' + "\n".join(h_nodes) + "\n        </Group>"

def build_minute_ring(group_name, minor_fast=True):
    m_nodes = []
    m_maj_ticks = []
    m_min_ticks = []
    for m in range(60):
        deg = m * 6
        five = (m % 5 == 0)
        r_rot = radial_rot(deg)
        col = TXT if five else DIMT
        m_nodes.append(dial_numeral(deg, RM, f"{m:02d}", 10.5, 26, 18, col, "m_weight", M_WIDTH_EXPR, static_angle=r_rot, minor_fast=(minor_fast and not five)))
        x1, y1 = pt(deg, (134 if five else 136) * S)
        x2, y2 = pt(deg, 141 * S)
        line = f'<Line startX="{f(x1)}" startY="{f(y1)}" endX="{f(x2)}" endY="{f(y2)}"><Stroke color="{TXT}" thickness="{f((1.6 if five else 1.0)*S)}" cap="BUTT"/></Line>'
        (m_maj_ticks if five else m_min_ticks).append(line)
    return (
        f'        <Group name="{group_name}" x="0" y="0" width="450" height="450">\n'
        + "\n".join(m_nodes) + "\n"
        + f'          <PartDraw name="{group_name}_tmin" x="0" y="0" width="450" height="450" alpha="95">{"".join(m_min_ticks)}</PartDraw>\n'
        + f'          <PartDraw name="{group_name}_tmaj" x="0" y="0" width="450" height="450" alpha="205">{"".join(m_maj_ticks)}</PartDraw>\n'
        + "        </Group>"
    )

def build_second_ring(group_name, minor_fast=True):
    s_nodes = []
    s_maj_ticks = []
    s_min_ticks = []
    for s_idx in range(60):
        deg = s_idx * 6
        five = (s_idx % 5 == 0)
        r_rot = radial_rot(deg)
        col = ACC if five else DIMT
        s_nodes.append(dial_numeral(deg, RS, f"{s_idx:02d}", 11, 26, 18, col, "s_weight", S_WIDTH_EXPR, static_angle=r_rot, minor_fast=(minor_fast and not five)))
        x1, y1 = pt(deg, (176 if five else 178) * S)
        x2, y2 = pt(deg, 184 * S)
        line = f'<Line startX="{f(x1)}" startY="{f(y1)}" endX="{f(x2)}" endY="{f(y2)}"><Stroke color="{ACC}" thickness="{f((2.0 if five else 1.1)*S)}" cap="BUTT"/></Line>'
        (s_maj_ticks if five else s_min_ticks).append(line)
    return (
        f'        <Group name="{group_name}" x="0" y="0" width="450" height="450">\n'
        + "\n".join(s_nodes) + "\n"
        + f'          <PartDraw name="{group_name}_tmin" x="0" y="0" width="450" height="450" alpha="115">{"".join(s_min_ticks)}</PartDraw>\n'
        + f'          <PartDraw name="{group_name}_tmaj" x="0" y="0" width="450" height="450" alpha="240">{"".join(s_maj_ticks)}</PartDraw>\n'
        + "        </Group>"
    )

def build_fixed_rings():
    bands = (
        f'      <PartDraw name="ring_bands" x="0" y="0" width="450" height="450">'
        f'<Ellipse x="{f(C-RH)}" y="{f(C-RH)}" width="{f(2*RH)}" height="{f(2*RH)}"><Stroke color="#10FFFFFF" thickness="{f(56*S)}"/></Ellipse>'
        f'<Ellipse x="{f(C-RM)}" y="{f(C-RM)}" width="{f(2*RM)}" height="{f(2*RM)}"><Stroke color="#0CFFFFFF" thickness="{f(46*S)}"/></Ellipse>'
        f'<Ellipse x="{f(C-RS)}" y="{f(C-RS)}" width="{f(2*RS)}" height="{f(2*RS)}"><Stroke color="#10FFFFFF" thickness="{f(38*S)}"/></Ellipse>'
        f'</PartDraw>'
    )
    return "\n".join([
        bands,
        build_hour_ring("ringH", minor_fast=False),
        build_minute_ring("ringM", minor_fast=True),
        build_second_ring("ringS", minor_fast=True),
    ])

# ---------------- Wider Frameless Light-Bending Glass Diopter Slits ----------------
def make_real_diopter_slit(lid, R, hw, hl, mag, ang_expr, ring_xml):
    """
    True optical glass diopter slit that glides smoothly over the stationary index ring:
    - Capsule is wider (2*hw) than the numeral beneath it so adjacent numerals enter/exit
      through the peripheral caustic refraction zone, exaggerating the liquid-glass bend.
    - Counter-rotates the entire stationary ring by -ang_expr around (225,225) inside a
      Group scaled by mag around the lens center (225, 225-R), clipped by renderMode="MASK".
    - Pure frameless glass structure (radial caustic dome, edge refraction vignette,
      curved meniscus sheen, and translucent specular rim — zero solid colored borders).
    """
    lx = f(C - hw)
    ly = f(C - R - hl)
    lw = f(2 * hw)
    lh = f(2 * hl)
    cr = f(hw)
    cy = f(C - R)
    piv_y = f"{(C - R) / 450.0:.4f}"
    glass_alpha = tern("glass_str", [155, 215, 255])
    # Peripheral magnification Halo: an outer 1.12x ring rim + inner magx core so edges bend optically!
    return f'''      <Group name="lens_{lid}_orbit" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">
        <Transform target="angle" value='{ang_expr}'/>
        <PartDraw name="lens_{lid}_shadow" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(C-hw+2.2)}" y="{f(C-R-hl+4.5)}" width="{lw}" height="{lh}" cornerRadiusX="{cr}" cornerRadiusY="{cr}"><Fill color="#50000000"/></RoundRectangle></PartDraw>
        <Group name="lens_{lid}_clip" x="0" y="0" width="450" height="450">
          <PartDraw name="lens_{lid}_mask" x="0" y="0" width="450" height="450" renderMode="MASK"><RoundRectangle x="{lx}" y="{ly}" width="{lw}" height="{lh}" cornerRadiusX="{cr}" cornerRadiusY="{cr}"><Fill color="#FFFFFFFF"/></RoundRectangle></PartDraw>
          <PartDraw name="lens_{lid}_bg_theme" x="0" y="0" width="450" height="450" renderMode="SOURCE"><Rectangle x="{f(C-hw-3)}" y="{f(C-R-hl-3)}" width="{f(2*hw+6)}" height="{f(2*hl+6)}"><Fill color="{BG}"/></Rectangle></PartDraw>
          <PartDraw name="lens_{lid}_bg_black" x="0" y="0" width="450" height="450" renderMode="SOURCE"><Transform target="alpha" value='{sel("bg_mode", 1)}'/><Rectangle x="{f(C-hw-3)}" y="{f(C-R-hl-3)}" width="{f(2*hw+6)}" height="{f(2*hl+6)}"><Fill color="#FF000000"/></Rectangle></PartDraw>
          <PartDraw name="lens_{lid}_band" x="0" y="0" width="450" height="450" renderMode="SOURCE"><Rectangle x="{f(C-hw-3)}" y="{f(C-R-hl-3)}" width="{f(2*hw+6)}" height="{f(2*hl+6)}"><Fill color="#12FFFFFF"/></Rectangle></PartDraw>
          <Group name="lens_{lid}_mag" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="{piv_y}" scaleX="{mag}" scaleY="{mag}" renderMode="SOURCE">
            <Group name="lens_{lid}_unrot" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">
              <Transform target="angle" value='0-({ang_expr})'/>
{ring_xml}
            </Group>
          </Group>
          <Group name="lens_{lid}_optics" x="0" y="0" width="450" height="450" renderMode="SOURCE">
            <Transform target="alpha" value='{glass_alpha}'/>
            <PartDraw name="lens_{lid}_caustic" x="0" y="0" width="450" height="450"><RoundRectangle x="{lx}" y="{ly}" width="{lw}" height="{lh}" cornerRadiusX="{cr}" cornerRadiusY="{cr}"><Fill color="#00FFFFFF"><RadialGradient centerX="{f(C-hw*0.16)}" centerY="{f(C-R-hl*0.20)}" radius="{f(hl*1.10)}" colors="#03FFFFFF #16FFFFFF #46FFFFFF" positions="0 0.64 1"/></Fill></RoundRectangle></PartDraw>
            <PartDraw name="lens_{lid}_vignette" x="0" y="0" width="450" height="450"><RoundRectangle x="{lx}" y="{ly}" width="{lw}" height="{lh}" cornerRadiusX="{cr}" cornerRadiusY="{cr}"><Stroke color="#82000000" thickness="5.5"/></RoundRectangle></PartDraw>
            <PartDraw name="lens_{lid}_refract_in" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(C-hw+2.4)}" y="{f(C-R-hl+2.4)}" width="{f(2*hw-4.8)}" height="{f(2*hl-4.8)}" cornerRadiusX="{f(hw-2.4)}" cornerRadiusY="{f(hw-2.4)}"><Stroke color="#2EFFFFFF" thickness="1.8"/></RoundRectangle></PartDraw>
            <PartDraw name="lens_{lid}_meniscus" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(C-hw+3)}" y="{f(C-R-hl+2)}" width="{f(2*hw-6)}" height="{f(hl*0.88)}" cornerRadiusX="{f(hw-3)}" cornerRadiusY="{f(hw*0.58)}"><Fill color="#00FFFFFF"><LinearGradient startX="225" startY="{f(C-R-hl+2)}" endX="225" endY="{cy}" colors="#3EFFFFFF #12FFFFFF #00FFFFFF" positions="0 0.54 1"/></Fill></RoundRectangle></PartDraw>
            <PartDraw name="lens_{lid}_spec" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(C-hw+0.8)}" y="{f(C-R-hl+0.8)}" width="{f(2*hw-1.6)}" height="{f(2*hl-1.6)}" cornerRadiusX="{f(hw-0.8)}" cornerRadiusY="{f(hw-0.8)}"><Stroke color="#FFFFFFFF" thickness="1.5"><LinearGradient startX="{lx}" startY="{ly}" endX="{f(C+hw)}" endY="{f(C-R+hl)}" colors="#A6FFFFFF #26FFFFFF #08FFFFFF #5EFFFFFF" positions="0 0.3 0.7 1"/></Stroke></RoundRectangle></PartDraw>
          </Group>
        </Group>
      </Group>'''

def build_three_lenses():
    # Wider diopter capsules so adjacent numerals enter/exit the curved glass edge:
    # - Hour lens:   RH=65.25,  hw=25.5 (width 51), hl=39.0 (height 78), mag=1.62x
    # - Minute lens: RM=132.75, hw=20.5 (width 41), hl=34.5 (height 69), mag=1.95x
    # - Second lens: RS=185.62, hw=17.5 (width 35), hl=27.5 (height 55), mag=1.82x
    lens_h = make_real_diopter_slit("H", RH, 25.5, 39.0, 1.62, ANG_H, build_hour_ring("z_ringH", minor_fast=False))
    lens_m = make_real_diopter_slit("M", RM, 20.5, 34.5, 1.95, ANG_M, build_minute_ring("z_ringM", minor_fast=True))
    lens_s = make_real_diopter_slit("S", RS, 17.5, 27.5, 1.82, ANG_S, build_second_ring("z_ringS", minor_fast=True))

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

# ---------------- 3 Brand-New AOD Styles Built Exclusively for Three Lens ----------------
SHIFT_X = "(([MINUTE]%5)-2)*2"
SHIFT_Y = "((floor([MINUTE]/5)%5)-2)*2"

def aod_style_group(k, body):
    s_aod = sel("aod_style", k)
    return (
        f'        <Group name="aod_style{k}" x="0" y="0" width="450" height="450">\n'
        f"          <Transform target=\"alpha\" value='{s_aod}'/>\n"
        + body + "\n        </Group>"
    )

# --- AOD 0: Dual Orbit Lenses ---
# Sparse stationary Hour (1..12) and Minute (00..59) index with wide orbiting Hour & Minute
# frameless glass diopter slits magnifying the index & bending adjacent numerals at the edges.
def build_aod0_ring_h(gname):
    nodes = []
    for h in range(1, 13):
        cx, cy = pt(h * 30, RH)
        nodes.append(f'            <PartText name="{nm(gname)}" x="{round(cx-18)}" y="{round(cy-13)}" width="36" height="26"><Text align="CENTER"><Font family="gsr_bold" size="16" color="{TXT}">{h}</Font></Text></PartText>')
    return f'          <Group name="{gname}" x="0" y="0" width="450" height="450">\n' + "\n".join(nodes) + "\n          </Group>"

def build_aod0_ring_m(gname, col_5, col_1):
    nodes = []
    for m in range(60):
        deg = m * 6
        five = (m % 5 == 0)
        cx, cy = pt(deg, RM)
        col = col_5 if five else col_1
        nodes.append(f'            <PartText name="{nm(gname)}" x="{round(cx-14)}" y="{round(cy-10)}" width="28" height="20" pivotX="0.5" pivotY="0.5" angle="{f(radial_rot(deg))}"><Text align="CENTER"><Font family="gsr_bold" size="10.5" color="{col}">{m:02d}</Font></Text></PartText>')
    return f'          <Group name="{gname}" x="0" y="0" width="450" height="450">\n' + "\n".join(nodes) + "\n          </Group>"

aod0_base_h = build_aod0_ring_h("aod0_bh")
aod0_base_m = []
for m in range(0, 60, 5):
    deg = m * 6
    cx, cy = pt(deg, RM)
    aod0_base_m.append(f'          <PartText name="aod0_bm{m}" x="{round(cx-15)}" y="{round(cy-11)}" width="30" height="22" pivotX="0.5" pivotY="0.5" angle="{f(radial_rot(deg))}"><Text align="CENTER"><Font family="gsr_bold" size="10.5" color="{DIMT}">{m:02d}</Font></Text></PartText>')

aod0_lens_h = make_real_diopter_slit("aodH", RH, 25.5, 39.0, 1.62, ANG_H, build_aod0_ring_h("aod0_zh"))
aod0_lens_m = make_real_diopter_slit("aodM", RM, 20.5, 34.5, 1.95, "[MINUTE]*6", build_aod0_ring_m("aod0_zm", ACC, TXT))
s0 = "\n".join([f'          <Group name="aod0_dim_idx" x="0" y="0" width="450" height="450" alpha="115">\n{aod0_base_h}\n' + "\n".join(aod0_base_m) + "\n          </Group>", aod0_lens_h, aod0_lens_m])

# --- AOD 1: Triple Monolith Slits ---
# Three horizontal frameless glass diopter slits stacked at center (Top: Hour strip with adjacent hours,
# Middle: wide Minute strip with adjacent minutes bending at the edges, Bottom: Day/Date glass slit).
def horizontal_slit_optics(sid, x, y, w, h):
    r = f(h / 2.0)
    cx = f(x + w * 0.36)
    cy = f(y + h * 0.32)
    return (
        f'          <PartDraw name="ms_{sid}_caustic" x="0" y="0" width="450" height="450"><RoundRectangle x="{x}" y="{y}" width="{w}" height="{h}" cornerRadiusX="{r}" cornerRadiusY="{r}"><Fill color="#00FFFFFF"><RadialGradient centerX="{cx}" centerY="{cy}" radius="{f(w*0.62)}" colors="#04FFFFFF #15FFFFFF #3EFFFFFF" positions="0 0.66 1"/></Fill></RoundRectangle></PartDraw>\n'
        f'          <PartDraw name="ms_{sid}_vig" x="0" y="0" width="450" height="450"><RoundRectangle x="{x}" y="{y}" width="{w}" height="{h}" cornerRadiusX="{r}" cornerRadiusY="{r}"><Stroke color="#80000000" thickness="5"/></RoundRectangle></PartDraw>\n'
        f'          <PartDraw name="ms_{sid}_sheen" x="0" y="0" width="450" height="450"><RoundRectangle x="{x+3}" y="{y+2}" width="{w-6}" height="{f(h*0.46)}" cornerRadiusX="{f(h*0.23)}" cornerRadiusY="{f(h*0.23)}"><Fill color="#00FFFFFF"><LinearGradient startX="225" startY="{y+2}" endX="225" endY="{f(y+h*0.5)}" colors="#36FFFFFF #0EFFFFFF #00FFFFFF" positions="0 0.6 1"/></Fill></RoundRectangle></PartDraw>\n'
        f'          <PartDraw name="ms_{sid}_spec" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(x+0.8)}" y="{f(y+0.8)}" width="{f(w-1.6)}" height="{f(h-1.6)}" cornerRadiusX="{f(h/2-0.8)}" cornerRadiusY="{f(h/2-0.8)}"><Stroke color="#FFFFFFFF" thickness="1.5"><LinearGradient startX="{x}" startY="{y}" endX="{x+w}" endY="{y+h}" colors="#9EFFFFFF #22FFFFFF #08FFFFFF #58FFFFFF" positions="0 0.32 0.7 1"/></Stroke></RoundRectangle></PartDraw>'
    )

s1 = "\n".join([
    # Top Hour Monolith Slit (shows prev hour dimmed on left, magnified active hour centered, next hour dimmed on right)
    '          <PartText name="aod1_hp" x="118" y="84" width="60" height="46" alpha="85"><Text align="CENTER"><Font family="gsr_medium" size="24" color="#00000000"><Outline color="#FFFFFFFF" width="1.6"><Template>%d<Parameter expression="([HOUR_1_12]+10)%12+1"/></Template></Outline></Font></Text></PartText>',
    '          <PartText name="aod1_hc" x="175" y="76" width="100" height="60"><Text align="CENTER"><Font family="gsr_bold" size="46" color="#00000000"><Outline color="#FFFFFFFF" width="2.8"><Template>%s<Parameter expression="[HOUR_1_12_Z]"/></Template></Outline></Font></Text></PartText>',
    '          <PartText name="aod1_hn" x="272" y="84" width="60" height="46" alpha="85"><Text align="CENTER"><Font family="gsr_medium" size="24" color="#00000000"><Outline color="#FFFFFFFF" width="1.6"><Template>%d<Parameter expression="[HOUR_1_12]%12+1"/></Template></Outline></Font></Text></PartText>',
    horizontal_slit_optics("top", 112, 72, 226, 66),
    # Middle Wide Minute Monolith Slit (shows m-1 and m+1 bending inside the glass edges around large magnified [MINUTE_Z])
    f'          <PartText name="aod1_mp" x="74" y="192" width="76" height="64" alpha="95"><Text align="CENTER"><Font family="gsr_medium" size="34" color="{DIMT}"><Template>%d<Parameter expression="([MINUTE]+59)%60"/></Template></Font></Text></PartText>',
    f'          <PartText name="aod1_mc" x="148" y="176" width="154" height="92"><Text align="CENTER"><Font family="gsr_bold" size="72" color="{ACC}"><Template>%s<Parameter expression="[MINUTE_Z]"/></Template></Font></Text></PartText>',
    f'          <PartText name="aod1_mn" x="300" y="192" width="76" height="64" alpha="95"><Text align="CENTER"><Font family="gsr_medium" size="34" color="{DIMT}"><Template>%d<Parameter expression="([MINUTE]+1)%60"/></Template></Font></Text></PartText>',
    horizontal_slit_optics("mid", 68, 174, 314, 96),
    # Bottom Date Monolith Slit
    f'          <PartText name="aod1_dt" x="135" y="314" width="180" height="40"><Text align="CENTER"><Font family="gsr_bold" size="20" color="{TXT}" letterSpacing="0.12"><Upper><Template>%s  %d<Parameter expression="[DAY_OF_WEEK_S]"/><Parameter expression="[DAY]"/></Template></Upper></Font></Text></PartText>',
    horizontal_slit_optics("bot", 132, 308, 186, 52),
])

# --- AOD 2: Eclipse Glass Ring ---
# A wide orbiting crescent glass lens illuminates a 110° arc of the stationary minute index ring
# while a large central circular glass diopter lens frames the hour & minute in the center.
s2 = "\n".join([
    f'          <Group name="aod2_idx" x="0" y="0" width="450" height="450" alpha="165">\n{build_aod0_ring_m("aod2_rm", ACC, DIMT)}\n          </Group>',
    f'          <Group name="aod2_eclipse_orbit" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">\n'
    f"            <Transform target=\"angle\" value='[MINUTE]*6'/>\n"
    f'            <PartDraw name="aod2_ec_glow" x="0" y="0" width="450" height="450"><Arc centerX="225" centerY="225" width="{f(2*RM)}" height="{f(2*RM)}" startAngle="315" endAngle="45" direction="CLOCKWISE"><Stroke color="#2EFFFFFF" thickness="44" cap="ROUND"/></Arc></PartDraw>\n'
    f'            <PartDraw name="aod2_ec_rim" x="0" y="0" width="450" height="450"><Arc centerX="225" centerY="225" width="{f(2*RM+42)}" height="{f(2*RM+42)}" startAngle="320" endAngle="40" direction="CLOCKWISE"><Stroke color="#88FFFFFF" thickness="1.6" cap="ROUND"/></Arc></PartDraw>\n'
    f'            <PartDraw name="aod2_ec_in" x="0" y="0" width="450" height="450"><Arc centerX="225" centerY="225" width="{f(2*RM-42)}" height="{f(2*RM-42)}" startAngle="320" endAngle="40" direction="CLOCKWISE"><Stroke color="#55FFFFFF" thickness="1.4" cap="ROUND"/></Arc></PartDraw>\n'
    f'          </Group>',
    f'          <PartText name="aod2_ch" x="125" y="138" width="200" height="68"><Text align="CENTER"><Font family="gsr_bold" size="52" color="#00000000"><Outline color="{TXT}" width="2.6"><Template>%s<Parameter expression="[HOUR_1_12_Z]"/></Template></Outline></Font></Text></PartText>',
    f'          <PartText name="aod2_cm" x="125" y="206" width="200" height="90"><Text align="CENTER"><Font family="gsr_bold" size="76" color="{ACC}"><Template>%s<Parameter expression="[MINUTE_Z]"/></Template></Font></Text></PartText>',
    horizontal_slit_optics("center_orb", 137, 137, 176, 176),
])

_aod_br_expr = cfg("aod_bright") + ' == "0" ? 140 : 205'
AOD = (
    '    <Group name="aod_root" x="0" y="0" width="450" height="450" alpha="0">\n'
    '      <Variant mode="AMBIENT" target="alpha" value="255"/>\n'
    f'      <Transform target="x" value="{SHIFT_X}"/>\n'
    f'      <Transform target="y" value="{SHIFT_Y}"/>\n'
    '      <Group name="aod_bright" x="0" y="0" width="450" height="450">\n'
    f"        <Transform target=\"alpha\" value='{_aod_br_expr}'/>\n"
    + "\n".join(aod_style_group(k, b) for k, b in enumerate([s0, s1, s2]))
    + "\n      </Group>\n    </Group>"
)

xml = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- Three Lens Watch Face for Wear OS (WFF v3).
     Three concentric fixed numeral/tick rings with wide orbiting frameless light-bending glass diopter slits.
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
