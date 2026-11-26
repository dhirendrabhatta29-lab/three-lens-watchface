import json, math, os, xml.etree.ElementTree as ET

C = 225
S = 450 / 400.0  # Scale from 400x400 SVG to 450x450 Wear OS WFF v4
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(TOOLS_DIR, "..", "app", "src", "main", "res") + os.sep

with open(os.path.join(TOOLS_DIR, "glass_rects.json"), "r", encoding="utf-8") as fh:
    GLASS_RECTS = json.load(fh)

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

# ---------------- 6 True Google Sans Rounded Font Weights & 6 Widths ----------------
WEIGHTS = [
    ("gsr_thin",       0, "Thin",        None),
    ("gsr_extralight", 1, "Extra light", None),
    ("gsr_light",      2, "Light",       None),
    ("gsr_medium",     3, "Medium",      None),
    ("gsr_bold",       4, "Bold",        None),
    ("gsr_black",      5, "Black",       None),
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
    ("dial_style", "Dial style",          0, ["Classic Three Lens", "Hidden Index Reveal", "Liquid Glass Blob"]),
    ("bg_mode",    "Background",          0, ["Pure black", "Theme color", "Custom photo"]),
    ("h_weight",   "Hours weight",        4, WEIGHT_NAMES),
    ("h_width",    "Hours width",         2, WIDTH_NAMES),
    ("m_weight",   "Minutes weight",      4, WEIGHT_NAMES),
    ("m_width",    "Minutes width",       2, WIDTH_NAMES),
    ("s_weight",   "Seconds weight",      3, WEIGHT_NAMES),
    ("s_width",    "Seconds width",       2, WIDTH_NAMES),
    ("hour_mode",  "Hours orientation",   0, ["Upright", "Radial", "Pointing"]),
    ("glass_str",  "Diopter refraction",  2, ["Subtle", "Balanced", "Exaggerated"]),
    ("aod_style",  "Always-on style",     0, ["Dual orbit lenses", "Triple monolith slits", "Eclipse glass ring"]),
    ("aod_bright", "Always-on brightness", 0, ["Dim", "Normal"]),
]

strings = {
    "app_name": "Three Lens",
    "cfg_palette": "Theme",
}

uc = []
uc.append('    <PhotosConfiguration id="bg_photo" configType="SINGLE" />')
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
    ("f_classic",     0, 0),
    ("f_hidden",      1, 0),
    ("f_liquid_blob", 2, 0),
]
FLAVORS = '    <Flavors defaultValue="f_classic">\n' + "\n".join(
    f'      <Flavor id="{fid}" displayName="dial_style_{dk}"><Configuration id="dial_style" optionId="{dk}"/><Configuration id="aod_style" optionId="{ak}"/></Flavor>'
    for fid, dk, ak in FL
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
def sel(i, k, on=255): return f'{cfg(i)} == {k} ? {on} : 0'
def tern(i, vals):
    s = str(vals[-1])
    for k in range(len(vals) - 2, -1, -1):
        s = f'({cfg(i)} == {k} ? {vals[k]} : {s})'
    return s

H_WIDTH_EXPR = tern("h_width", WIDTH_VALS)
M_WIDTH_EXPR = tern("m_width", WIDTH_VALS)
S_WIDTH_EXPR = tern("s_width", WIDTH_VALS)

# Dial radii scaled from 400x400 HTML (RH=58, RM=118, RS=165) to 450x450
RH = 58 * S     # 65.25
RM = 118 * S    # 132.75
RS = 165 * S    # 185.625

# Smooth continuous sweep motion preserved from original
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
    nodes = []
    if minor_fast:
        tiers = [
            ("gsr_extralight", f'({cfg(weight_cfg)} == 0 || {cfg(weight_cfg)} == 1) ? 255 : 0'),
            ("gsr_medium",     f'({cfg(weight_cfg)} == 2 || {cfg(weight_cfg)} == 3) ? 255 : 0'),
            ("gsr_bold",       f'({cfg(weight_cfg)} == 4 || {cfg(weight_cfg)} == 5) ? 255 : 0'),
        ]
        for fam, a_expr in tiers:
            nodes.append(
                f'            <PartText name="{nm(prefix)}" x="0" y="0" width="{w}" height="{h}">'
                f"<Transform target=\"alpha\" value='{a_expr}'/>"
                f'<Text align="CENTER"><Font family="{fam}" size="{size}" color="{col}">{text_body}</Font></Text></PartText>'
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

# ---------------- Shared static ring builders (ZERO popping/springing!) ----------------
def build_hour_ring(group_name, minor_fast=False, inside_lens=False):
    h_nodes = []
    for h in range(1, 13):
        deg = h * 30
        r_rot = radial_rot(deg)
        ang_expr = f'({cfg("hour_mode")} == 0 ? 0 : ({cfg("hour_mode")} == 1 ? {r_rot} : {deg}))'
        bw, bh, sz = (46, 32, 23.5) if inside_lens else (36, 26, 16.5)
        h_nodes.append(dial_numeral(deg, RH, str(h), sz, bw, bh, TXT, "h_weight", H_WIDTH_EXPR, angle_expr=ang_expr, minor_fast=minor_fast))
    return f'        <Group name="{group_name}" x="0" y="0" width="450" height="450">\n' + "\n".join(h_nodes) + "\n        </Group>"

def build_minute_ring(group_name, minor_fast=True, inside_lens=False):
    m_nodes = []
    m_maj_ticks = []
    m_min_ticks = []
    for m in range(60):
        deg = m * 6
        five = (m % 5 == 0)
        r_rot = radial_rot(deg)
        col = TXT if five else DIMT
        # Non-overlapping static sizes so all 60 numerals stay permanently at alpha=255 with zero popping
        bw, bh, sz = (34, 22, 14.5) if inside_lens else (26, 18, 10.5)
        m_nodes.append(dial_numeral(deg, RM, f"{m:02d}", sz, bw, bh, col, "m_weight", M_WIDTH_EXPR, static_angle=r_rot, minor_fast=(minor_fast and not five)))
        x1, y1 = pt(deg, (133 if five else 135.5) * S if inside_lens else (134 if five else 136) * S)
        x2, y2 = pt(deg, (142.5 if inside_lens else 141) * S)
        line = f'<Line startX="{f(x1)}" startY="{f(y1)}" endX="{f(x2)}" endY="{f(y2)}"><Stroke color="{TXT}" thickness="{f((1.6 if five else 1.0)*S*(1.45 if inside_lens else 1.0))}" cap="BUTT"/></Line>'
        (m_maj_ticks if five else m_min_ticks).append(line)
    return (
        f'        <Group name="{group_name}" x="0" y="0" width="450" height="450">\n'
        + "\n".join(m_nodes) + "\n"
        + f'          <PartDraw name="{group_name}_tmin" x="0" y="0" width="450" height="450" alpha="95">{"".join(m_min_ticks)}</PartDraw>\n'
        + f'          <PartDraw name="{group_name}_tmaj" x="0" y="0" width="450" height="450" alpha="205">{"".join(m_maj_ticks)}</PartDraw>\n'
        + "        </Group>"
    )

def build_second_ring(group_name, minor_fast=True, inside_lens=False):
    s_nodes = []
    s_maj_ticks = []
    s_min_ticks = []
    for s_idx in range(60):
        deg = s_idx * 6
        five = (s_idx % 5 == 0)
        r_rot = radial_rot(deg)
        col = ACC if five else DIMT
        bw, bh, sz = (34, 22, 15.5) if inside_lens else (26, 18, 11)
        s_nodes.append(dial_numeral(deg, RS, f"{s_idx:02d}", sz, bw, bh, col, "s_weight", S_WIDTH_EXPR, static_angle=r_rot, minor_fast=(minor_fast and not five)))
        x1, y1 = pt(deg, (175 if five else 177.5) * S if inside_lens else (176 if five else 178) * S)
        x2, y2 = pt(deg, (185 if inside_lens else 184) * S)
        line = f'<Line startX="{f(x1)}" startY="{f(y1)}" endX="{f(x2)}" endY="{f(y2)}"><Stroke color="{ACC}" thickness="{f((2.0 if five else 1.1)*S*(1.45 if inside_lens else 1.0))}" cap="BUTT"/></Line>'
        (s_maj_ticks if five else s_min_ticks).append(line)
    return (
        f'        <Group name="{group_name}" x="0" y="0" width="450" height="450">\n'
        + "\n".join(s_nodes) + "\n"
        + f'          <PartDraw name="{group_name}_tmin" x="0" y="0" width="450" height="450" alpha="115">{"".join(s_min_ticks)}</PartDraw>\n'
        + f'          <PartDraw name="{group_name}_tmaj" x="0" y="0" width="450" height="450" alpha="240">{"".join(s_maj_ticks)}</PartDraw>\n'
        + "        </Group>"
    )

def build_fixed_rings():
    """Visible stationary rings for Mode 0 (Classic Three Lens) + subtle hidden-index grooves for Mode 1."""
    classic_group = (
        '      <Group name="classic_base_rings" x="0" y="0" width="450" height="450">\n'
        f'        <Transform target="alpha" value=\'{sel("dial_style", 0)}\'/>\n'
        f'        <PartDraw name="ring_bands" x="0" y="0" width="450" height="450">'
        f'<Ellipse x="{f(C-RH)}" y="{f(C-RH)}" width="{f(2*RH)}" height="{f(2*RH)}"><Stroke color="#0EFFFFFF" thickness="{f(56*S)}"/></Ellipse>'
        f'<Ellipse x="{f(C-RM)}" y="{f(C-RM)}" width="{f(2*RM)}" height="{f(2*RM)}"><Stroke color="#0BFFFFFF" thickness="{f(46*S)}"/></Ellipse>'
        f'<Ellipse x="{f(C-RS)}" y="{f(C-RS)}" width="{f(2*RS)}" height="{f(2*RS)}"><Stroke color="#0EFFFFFF" thickness="{f(38*S)}"/></Ellipse>'
        f'</PartDraw>\n'
        + build_hour_ring("ringH", minor_fast=False) + "\n"
        + build_minute_ring("ringM", minor_fast=True) + "\n"
        + build_second_ring("ringS", minor_fast=True) + "\n"
        + "      </Group>"
    )
    hidden_grooves = (
        '      <PartDraw name="hidden_track_grooves" x="0" y="0" width="450" height="450">\n'
        f'        <Transform target="alpha" value=\'{sel("dial_style", 1)}\'/>\n'
        f'        <Ellipse x="{f(C-RH)}" y="{f(C-RH)}" width="{f(2*RH)}" height="{f(2*RH)}"><Stroke color="#09FFFFFF" thickness="{f(46*S)}"/></Ellipse>\n'
        f'        <Ellipse x="{f(C-RM)}" y="{f(C-RM)}" width="{f(2*RM)}" height="{f(2*RM)}"><Stroke color="#07FFFFFF" thickness="{f(38*S)}"/></Ellipse>\n'
        f'        <Ellipse x="{f(C-RS)}" y="{f(C-RS)}" width="{f(2*RS)}" height="{f(2*RS)}"><Stroke color="#09FFFFFF" thickness="{f(32*S)}"/></Ellipse>\n'
        f'        <Ellipse x="{f(C-RH)}" y="{f(C-RH)}" width="{f(2*RH)}" height="{f(2*RH)}"><Stroke color="#14FFFFFF" thickness="1.2"/></Ellipse>\n'
        f'        <Ellipse x="{f(C-RM)}" y="{f(C-RM)}" width="{f(2*RM)}" height="{f(2*RM)}"><Stroke color="#12FFFFFF" thickness="1.2"/></Ellipse>\n'
        f'        <Ellipse x="{f(C-RS)}" y="{f(C-RS)}" width="{f(2*RS)}" height="{f(2*RS)}"><Stroke color="#14FFFFFF" thickness="1.2"/></Ellipse>\n'
        '      </PartDraw>'
    )
    return classic_group + "\n" + hidden_grooves

# ---------------- Pure Colorless Optical Glass Lens (True 1.16x Optical Zoom, ZERO Popping) ----------------
def make_real_diopter_slit(lid, R, hw, hl, r_blob, ang_expr, ring_xml, slit_img, arm_img):
    """
    Pure colorless optical glass diopter that glides smoothly over completely static indexes:
    - ZERO blue/cyan tint and ZERO milky white interior tint in glass overlays.
    - Wraps the counter-rotated static ring + background (theme, user photo + radial vignette,
      machined dial) inside a 1.16x scale group pivoted on the lens center (0.5, (C-R)/450)
      so numerals and background photo genuinely zoom inside the glass with zero springing!
    - Morphs its capsule mask smoothly between slit (Modes 0 & 1) and circular dome (Mode 2).
    """
    lx, ly, lw, lh, cr = C - hw, C - R - hl, 2 * hw, 2 * hl, hw
    bx, by, bw, bh, br = C - r_blob, C - R - r_blob, 2 * r_blob, 2 * r_blob, r_blob
    piv_y = f"{(C - R) / 450.0:.5f}"

    glass_alpha = tern("glass_str", [165, 220, 255])
    sr = GLASS_RECTS[slit_img]
    ar = GLASS_RECTS[arm_img]

    mask_shape = (
        f'<RoundRectangle x="{f(lx)}" y="{f(ly)}" width="{f(lw)}" height="{f(lh)}" cornerRadiusX="{f(cr)}" cornerRadiusY="{f(cr)}">'
        f'<Transform target="x" value=\'{cfg("dial_style")} == 2 ? {f(bx)} : {f(lx)}\'/>'
        f'<Transform target="y" value=\'{cfg("dial_style")} == 2 ? {f(by)} : {f(ly)}\'/>'
        f'<Transform target="width" value=\'{cfg("dial_style")} == 2 ? {f(bw)} : {f(lw)}\'/>'
        f'<Transform target="height" value=\'{cfg("dial_style")} == 2 ? {f(bh)} : {f(lh)}\'/>'
        f'<Transform target="cornerRadiusX" value=\'{cfg("dial_style")} == 2 ? {f(br)} : {f(cr)}\'/>'
        f'<Transform target="cornerRadiusY" value=\'{cfg("dial_style")} == 2 ? {f(br)} : {f(cr)}\'/>'
        f'<Fill color="#FFFFFFFF"/></RoundRectangle>'
    )

    slit_alpha_expr = f'{cfg("dial_style")} == 2 ? 0 : ({glass_alpha})'
    arm_alpha_expr = f'{cfg("dial_style")} == 2 ? ({glass_alpha}) : 0'

    zoom_bg_xml = f'''              <PartDraw name="lens_{lid}_bg_black" x="0" y="0" width="450" height="450"><Rectangle x="0" y="0" width="450" height="450"><Fill color="#FF000000"/></Rectangle></PartDraw>
              <PartDraw name="lens_{lid}_bg_theme" x="0" y="0" width="450" height="450"><Transform target="alpha" value='{sel("bg_mode", 1)}'/><Ellipse x="11.25" y="11.25" width="427.5" height="427.5"><Fill color="{BG}"/></Ellipse></PartDraw>
              <PartImage name="lens_{lid}_photo" x="0" y="0" width="450" height="450"><Transform target="alpha" value='{sel("bg_mode", 2)}'/><Photos source="[CONFIGURATION.bg_photo]" defaultImageResource="bg_photo_default" /></PartImage>
              <PartImage name="lens_{lid}_photo_vig" x="0" y="0" width="450" height="450"><Transform target="alpha" value='{sel("bg_mode", 2)}'/><Image resource="bg_photo_vignette"/></PartImage>
              <PartImage name="lens_{lid}_machined" x="0" y="0" width="450" height="450"><Transform target="alpha" value='({cfg("dial_style")} == 2) ? ({cfg("bg_mode")} == 2 ? 125 : 255) : 0'/><Image resource="dial_machined"/></PartImage>'''

    return f'''      <Group name="lens_{lid}_orbit" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">
        <Transform target="angle" value='{ang_expr}'/>
        <Group name="lens_{lid}_clip" x="0" y="0" width="450" height="450">
          <PartDraw name="lens_{lid}_mask" x="0" y="0" width="450" height="450" renderMode="MASK">{mask_shape}</PartDraw>
          <Group name="lens_{lid}_zoom" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="{piv_y}" scaleX="1.16" scaleY="1.16" renderMode="SOURCE">
            <Group name="lens_{lid}_unrot" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">
              <Transform target="angle" value='0-({ang_expr})'/>
{zoom_bg_xml}
{ring_xml}
            </Group>
          </Group>
        </Group>
        <PartImage name="lens_{lid}_slit_glass" x="{sr["x"]}" y="{sr["y"]}" width="{sr["w"]}" height="{sr["h"]}"><Transform target="alpha" value='{slit_alpha_expr}'/><Image resource="{slit_img}"/></PartImage>
        <PartImage name="lens_{lid}_arm_glass" x="{ar["x"]}" y="{ar["y"]}" width="{ar["w"]}" height="{ar["h"]}"><Transform target="alpha" value='{arm_alpha_expr}'/><Image resource="{arm_img}"/></PartImage>
      </Group>'''

def build_proximity_merge_bridge(name, ang_a, ang_b, img_name, glass_alpha):
    """Smoothly fades in a colorless glass meniscus bridge when adjacent domes come within 26 degrees
    in Liquid Glass Blob mode (Iteration 3), making lobes organically merge & break apart.
    """
    diff = f'((({ang_b}) - ({ang_a}) + 540) % 360) - 180'
    mid_ang = f'({ang_a}) + 0.5 * ({diff})'
    alpha_expr = f'({cfg("dial_style")} == 2) ? clamp(1 - abs({diff}) / 26.0, 0, 1) * ({glass_alpha}) : 0'
    br = GLASS_RECTS[img_name]
    return (
        f'      <Group name="{name}_orbit" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">\n'
        f"        <Transform target=\"angle\" value='{mid_ang}'/>\n"
        f'        <PartImage name="{name}_img" x="{br["x"]}" y="{br["y"]}" width="{br["w"]}" height="{br["h"]}">'
        f"<Transform target=\"alpha\" value='{alpha_expr}'/><Image resource=\"{img_name}\"/></PartImage>\n"
        f'      </Group>'
    )

def build_three_lenses():
    lens_h = make_real_diopter_slit("H", RH, 19.5, 33.0, 25.5, ANG_H, build_hour_ring("z_ringH", minor_fast=False, inside_lens=True), "glass_slit_h", "glass_arm_h")
    lens_m = make_real_diopter_slit("M", RM, 15.0, 29.5, 21.5, ANG_M, build_minute_ring("z_ringM", minor_fast=True, inside_lens=True), "glass_slit_m", "glass_arm_m")
    lens_s = make_real_diopter_slit("S", RS, 13.5, 24.0, 19.5, ANG_S, build_second_ring("z_ringS", minor_fast=True, inside_lens=True), "glass_slit_s", "glass_arm_s")

    glass_alpha = tern("glass_str", [165, 220, 255])
    merge_hm = build_proximity_merge_bridge("blob_merge_hm", ANG_H, ANG_M, "glass_bridge_hm", glass_alpha)
    merge_ms = build_proximity_merge_bridge("blob_merge_ms", ANG_M, ANG_S, "glass_bridge_ms", glass_alpha)

    hr = GLASS_RECTS["glass_hub"]
    hub = (
        f'      <PartImage name="blob_center_glass" x="{hr["x"]}" y="{hr["y"]}" width="{hr["w"]}" height="{hr["h"]}"><Transform target="alpha" value=\'{cfg("dial_style")} == 2 ? ({glass_alpha}) : 0\'/><Image resource="glass_hub"/></PartImage>\n'
        f'      <PartDraw name="center_hub" x="0" y="0" width="450" height="450">'
        f'<Ellipse x="212.5" y="212.5" width="25" height="25"><Stroke color="#72FFFFFF" thickness="1.3"/></Ellipse>'
        f'<Ellipse x="221" y="221" width="8" height="8"><Fill color="{ACC}"/></Ellipse>'
        f'</PartDraw>'
    )
    return "\n".join([lens_h, lens_m, lens_s, merge_hm, merge_ms, hub])

# ---------------- Watch-Font Date & Battery Telemetry (Liquid Glass Blob Mode) ----------------
TELEMETRY = (
    '      <Group name="blob_telemetry" x="0" y="0" width="450" height="450">\n'
    f'        <Transform target="alpha" value=\'{sel("dial_style", 2)}\'/>\n'
    f'        <PartText name="tel_date" x="145" y="114" width="160" height="22" alpha="200">\n'
    f'          <Text align="CENTER"><Font family="gsr_bold" size="13" color="{TXT}" letterSpacing="0.12">'
    f'<Upper><Template>%s %d<Parameter expression="[DAY_OF_WEEK_S]"/><Parameter expression="[DAY]"/></Template></Upper></Font></Text>\n'
    '        </PartText>\n'
    f'        <PartText name="tel_batt" x="165" y="309" width="120" height="22" alpha="200">\n'
    f'          <Text align="CENTER"><Font family="gsr_bold" size="13" color="{TXT}" letterSpacing="0.08">'
    f'<Template>%d%%<Parameter expression="[BATTERY_PERCENT]"/></Template></Font></Text>\n'
    '        </PartText>\n'
    '        <PartDraw name="tel_batt_arc_bg" x="0" y="0" width="450" height="450" alpha="70">\n'
    '          <Arc centerX="225" centerY="225" width="218" height="218" startAngle="158" endAngle="202" direction="CLOCKWISE"><Stroke color="#88FFFFFF" thickness="2.2" cap="ROUND"/></Arc>\n'
    '        </PartDraw>\n'
    '        <PartDraw name="tel_batt_arc_fg" x="0" y="0" width="450" height="450" alpha="210">\n'
    '          <Arc centerX="225" centerY="225" width="218" height="218" startAngle="202" endAngle="158" direction="COUNTER_CLOCKWISE">\n'
    '            <Transform target="endAngle" value="202 - 44 * ([BATTERY_PERCENT] / 100.0)"/>\n'
    f'            <Stroke color="{ACC}" thickness="2.4" cap="ROUND"/>\n'
    '          </Arc>\n'
    '        </PartDraw>\n'
    '      </Group>'
)

# ---------------- Background Layers ----------------
BGL = f'''    <Group name="bg_root" x="0" y="0" width="450" height="450">
      <Variant mode="AMBIENT" target="alpha" value="0"/>
      <PartDraw name="bg_black" x="0" y="0" width="450" height="450">
        <Rectangle x="0" y="0" width="450" height="450"><Fill color="#FF000000"/></Rectangle>
      </PartDraw>
      <PartDraw name="bg_theme" x="0" y="0" width="450" height="450">
        <Transform target="alpha" value='{sel("bg_mode", 1)}'/>
        <Ellipse x="4.5" y="4.5" width="441" height="441"><Fill color="#FF060608"/></Ellipse>
        <Ellipse x="11.25" y="11.25" width="427.5" height="427.5"><Fill color="{BG}"/><Stroke color="{BEZEL}" thickness="2.2"/></Ellipse>
      </PartDraw>
      <PartImage name="bg_user_photo" x="0" y="0" width="450" height="450">
        <Transform target="alpha" value='{sel("bg_mode", 2)}'/>
        <Photos source="[CONFIGURATION.bg_photo]" defaultImageResource="bg_photo_default" />
      </PartImage>
      <PartImage name="bg_photo_vignette" x="0" y="0" width="450" height="450">
        <Transform target="alpha" value='{sel("bg_mode", 2)}'/>
        <Image resource="bg_photo_vignette"/>
      </PartImage>
      <PartImage name="bg_machined_dial" x="0" y="0" width="450" height="450">
        <Transform target="alpha" value='({cfg("dial_style")} == 2) ? ({cfg("bg_mode")} == 2 ? 125 : 255) : 0'/>
        <Image resource="dial_machined"/>
      </PartImage>
    </Group>'''

ACTIVE_ROOT = (
    '    <Group name="active_root" x="0" y="0" width="450" height="450">\n'
    '      <Variant mode="AMBIENT" target="alpha" value="0"/>\n'
    + build_fixed_rings() + "\n"
    + TELEMETRY + "\n"
    + build_three_lenses()
    + "\n    </Group>"
)

# ---------------- 3 Rock-Solid AOD Styles (Pure Colorless Glass, Zero Mask/Image Failures) ----------------
SHIFT_X = "(([MINUTE]%5)-2)*2"
SHIFT_Y = "((floor([MINUTE]/5)%5)-2)*2"

def aod_style_group(k, body):
    s_aod = sel("aod_style", k)
    return (
        f'        <Group name="aod_style{k}" x="0" y="0" width="450" height="450">\n'
        f"          <Transform target=\"alpha\" value='{s_aod}'/>\n"
        + body + "\n        </Group>"
    )

# Pure colorless glass rim optics (used in AOD capsules and monolith slits — ZERO blue/cyan tint)
def colorless_capsule_rim(name_prefix, x, y, w, h, cr):
    return (
        f'          <PartDraw name="{name_prefix}_inner" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(x+1.8)}" y="{f(y+1.8)}" width="{f(w-3.6)}" height="{f(h-3.6)}" cornerRadiusX="{f(cr-1.8)}" cornerRadiusY="{f(cr-1.8)}"><Stroke color="#FFFFFFFF" thickness="1.2"><LinearGradient startX="{f(x)}" startY="{f(y)}" endX="{f(x+w)}" endY="{f(y+h)}" colors="#48FFFFFF #12FFFFFF #08FFFFFF #34FFFFFF" positions="0 0.34 0.7 1"/></Stroke></RoundRectangle></PartDraw>\n'
        f'          <PartDraw name="{name_prefix}_spec" x="0" y="0" width="450" height="450"><RoundRectangle x="{f(x+0.8)}" y="{f(y+0.8)}" width="{f(w-1.6)}" height="{f(h-1.6)}" cornerRadiusX="{f(cr-0.8)}" cornerRadiusY="{f(cr-0.8)}"><Stroke color="#FFFFFFFF" thickness="1.5"><LinearGradient startX="{f(x)}" startY="{f(y)}" endX="{f(x+w)}" endY="{f(y+h)}" colors="#CCFFFFFF #32FFFFFF #14FFFFFF #7CFFFFFF" positions="0 0.32 0.7 1"/></Stroke></RoundRectangle></PartDraw>'
    )

# --- AOD 0: Lightweight Vector Dual Orbit Lenses (works identically across ALL 3 dial styles & bg modes) ---
aod0_base_h = []
for h in range(1, 13):
    cx, cy = pt(h * 30, RH)
    aod0_base_h.append(f'            <PartText name="aod0_bh{h}" x="{round(cx-18)}" y="{round(cy-13)}" width="36" height="26"><Text align="CENTER"><Font family="gsr_bold" size="15" color="{DIMT}">{h}</Font></Text></PartText>')
aod0_base_m = []
for m in range(0, 60, 5):
    deg = m * 6
    cx, cy = pt(deg, RM)
    aod0_base_m.append(f'            <PartText name="aod0_bm{m}" x="{round(cx-15)}" y="{round(cy-11)}" width="30" height="22" pivotX="0.5" pivotY="0.5" angle="{f(radial_rot(deg))}"><Text align="CENTER"><Font family="gsr_bold" size="10.5" color="{DIMT}">{m:02d}</Font></Text></PartText>')

s0 = "\n".join([
    '          <Group name="aod0_dim_idx" x="0" y="0" width="450" height="450" alpha="105">',
    "\n".join(aod0_base_h),
    "\n".join(aod0_base_m),
    '          </Group>',
    # Orbiting Hour Capsule
    f'          <Group name="aod0_lensH_orbit" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">',
    f'            <Transform target="angle" value=\'{ANG_H}\'/>',
    f'            <PartDraw name="aod0_h_bg" x="0" y="0" width="450" height="450"><RoundRectangle x="205.5" y="{f(C-RH-33)}" width="39" height="66" cornerRadiusX="19.5" cornerRadiusY="19.5"><Fill color="#FF000000"/></RoundRectangle></PartDraw>',
    colorless_capsule_rim("aod0_h", 205.5, C - RH - 33, 39, 66, 19.5),
    f'            <Group name="aod0_h_txt_unrot" x="200" y="{round(C-RH-19)}" width="50" height="38" pivotX="0.5" pivotY="0.5">',
    f'              <Transform target="angle" value=\'0-({ANG_H})\'/>',
    f'              <PartText name="aod0_h_val" x="0" y="0" width="50" height="38"><Text align="CENTER"><Font family="gsr_bold" size="25" color="{TXT}"><Template>%d<Parameter expression="[HOUR_1_12]"/></Template></Font></Text></PartText>',
    '            </Group>',
    '          </Group>',
    # Orbiting Minute Capsule
    f'          <Group name="aod0_lensM_orbit" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">',
    f'            <Transform target="angle" value=\'[MINUTE]*6\'/>',
    f'            <PartDraw name="aod0_m_bg" x="0" y="0" width="450" height="450"><RoundRectangle x="210" y="{f(C-RM-29.5)}" width="30" height="59" cornerRadiusX="15" cornerRadiusY="15"><Fill color="#FF000000"/></RoundRectangle></PartDraw>',
    colorless_capsule_rim("aod0_m", 210, C - RM - 29.5, 30, 59, 15),
    f'            <Group name="aod0_m_txt_unrot" x="201" y="{round(C-RM-17)}" width="48" height="34" pivotX="0.5" pivotY="0.5">',
    f'              <Transform target="angle" value=\'0-([MINUTE]*6)\'/>',
    f'              <PartText name="aod0_m_val" x="0" y="0" width="48" height="34"><Text align="CENTER"><Font family="gsr_bold" size="21" color="{ACC}"><Template>%s<Parameter expression="[MINUTE_Z]"/></Template></Font></Text></PartText>',
    '            </Group>',
    '          </Group>',
])

# --- AOD 1: Triple Monolith Slits (pure colorless glass edges) ---
def horizontal_slit_optics(sid, x, y, w, h):
    return colorless_capsule_rim(f"ms_{sid}", x, y, w, h, h / 2.0)

s1 = "\n".join([
    '          <PartText name="aod1_hp" x="118" y="84" width="60" height="46" alpha="85"><Text align="CENTER"><Font family="gsr_medium" size="24" color="#00000000"><Outline color="#FFFFFFFF" width="1.6"><Template>%d<Parameter expression="([HOUR_1_12]+10)%12+1"/></Template></Outline></Font></Text></PartText>',
    '          <PartText name="aod1_hc" x="175" y="76" width="100" height="60"><Text align="CENTER"><Font family="gsr_bold" size="46" color="#00000000"><Outline color="#FFFFFFFF" width="2.8"><Template>%s<Parameter expression="[HOUR_1_12_Z]"/></Template></Outline></Font></Text></PartText>',
    '          <PartText name="aod1_hn" x="272" y="84" width="60" height="46" alpha="85"><Text align="CENTER"><Font family="gsr_medium" size="24" color="#00000000"><Outline color="#FFFFFFFF" width="1.6"><Template>%d<Parameter expression="[HOUR_1_12]%12+1"/></Template></Outline></Font></Text></PartText>',
    horizontal_slit_optics("top", 112, 72, 226, 66),
    f'          <PartText name="aod1_mp" x="74" y="192" width="76" height="64" alpha="95"><Text align="CENTER"><Font family="gsr_medium" size="34" color="{DIMT}"><Template>%d<Parameter expression="([MINUTE]+59)%60"/></Template></Font></Text></PartText>',
    f'          <PartText name="aod1_mc" x="148" y="176" width="154" height="92"><Text align="CENTER"><Font family="gsr_bold" size="72" color="{ACC}"><Template>%s<Parameter expression="[MINUTE_Z]"/></Template></Font></Text></PartText>',
    f'          <PartText name="aod1_mn" x="300" y="192" width="76" height="64" alpha="95"><Text align="CENTER"><Font family="gsr_medium" size="34" color="{DIMT}"><Template>%d<Parameter expression="([MINUTE]+1)%60"/></Template></Font></Text></PartText>',
    horizontal_slit_optics("mid", 68, 174, 314, 96),
    f'          <PartText name="aod1_dt" x="135" y="314" width="180" height="40"><Text align="CENTER"><Font family="gsr_bold" size="20" color="{TXT}" letterSpacing="0.12"><Upper><Template>%s  %d<Parameter expression="[DAY_OF_WEEK_S]"/><Parameter expression="[DAY]"/></Template></Upper></Font></Text></PartText>',
    horizontal_slit_optics("bot", 132, 308, 186, 52),
])

# --- AOD 2: Eclipse Glass Ring (pure colorless edge rim) ---
aod2_ring_m = []
for m in range(0, 60, 5):
    deg = m * 6
    cx, cy = pt(deg, RM)
    aod2_ring_m.append(f'            <PartText name="aod2_bm{m}" x="{round(cx-15)}" y="{round(cy-11)}" width="30" height="22" pivotX="0.5" pivotY="0.5" angle="{f(radial_rot(deg))}"><Text align="CENTER"><Font family="gsr_bold" size="10.5" color="{DIMT}">{m:02d}</Font></Text></PartText>')

s2 = "\n".join([
    '          <Group name="aod2_idx" x="0" y="0" width="450" height="450" alpha="165">',
    "\n".join(aod2_ring_m),
    '          </Group>',
    f'          <Group name="aod2_eclipse_orbit" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">\n'
    f"            <Transform target=\"angle\" value='[MINUTE]*6'/>\n"
    f'            <PartDraw name="aod2_ec_rim" x="0" y="0" width="450" height="450"><Arc centerX="225" centerY="225" width="{f(2*RM+42)}" height="{f(2*RM+42)}" startAngle="320" endAngle="40" direction="CLOCKWISE"><Stroke color="#99FFFFFF" thickness="1.6" cap="ROUND"/></Arc></PartDraw>\n'
    f'            <PartDraw name="aod2_ec_in" x="0" y="0" width="450" height="450"><Arc centerX="225" centerY="225" width="{f(2*RM-42)}" height="{f(2*RM-42)}" startAngle="320" endAngle="40" direction="CLOCKWISE"><Stroke color="#66FFFFFF" thickness="1.4" cap="ROUND"/></Arc></PartDraw>\n'
    f'          </Group>',
    f'          <PartText name="aod2_ch" x="125" y="138" width="200" height="68"><Text align="CENTER"><Font family="gsr_bold" size="52" color="#00000000"><Outline color="{TXT}" width="2.6"><Template>%s<Parameter expression="[HOUR_1_12_Z]"/></Template></Outline></Font></Text></PartText>',
    f'          <PartText name="aod2_cm" x="125" y="206" width="200" height="90"><Text align="CENTER"><Font family="gsr_bold" size="76" color="{ACC}"><Template>%s<Parameter expression="[MINUTE_Z]"/></Template></Font></Text></PartText>',
    horizontal_slit_optics("center_orb", 137, 137, 176, 176),
])

_aod_br_expr = cfg("aod_bright") + ' == 0 ? 140 : 205'
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
<!-- Three Lens Watch Face for Wear OS (WFF v4).
     Pure colorless optical glass diopters with 1.16x true optical zoom over static indexes,
     Classic / Hidden Index Reveal / Liquid Glass Blob dial styles, proximity merge bridges,
     and dimmed custom photo background support.
     Font: Google Sans Rounded (SIL OFL 1.1) - see FONT_LICENSE.txt -->
<WatchFace width="450" height="450">
{USERCFG}
  <Scene backgroundColor="#FF000000">
{BGL}
{ACTIVE_ROOT}
{AOD}
  </Scene>
</WatchFace>
'''

ET.fromstring(xml)
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
