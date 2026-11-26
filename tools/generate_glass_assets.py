"""Generate pure colorless optical glass lens sprites, machined dial background,
soft photo vignette, proximity merge bridges, and photo fallback drawable
for Three Lens Watch Face v1.3 (WFF v4).

All glass assets have ZERO white milky interior tint and ZERO prebaked blue/cyan tint:
interior (alpha = 0) lets the real dial/index/photo shine directly through while
curved edges show only neutral colorless refraction shadow, Fresnel highlights,
and crisp hairline specular meniscus rims.
"""

import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw

OUT_DRAWABLE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "app", "src", "main", "res", "drawable"
)
OUT_META = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glass_rects.json")

W = 450
C = 225.0
S = 450.0 / 400.0

RH = 58.0 * S      # 65.25
RM = 118.0 * S     # 132.75
RS = 165.0 * S     # 185.625

Y_GRID, X_GRID = np.mgrid[0:W, 0:W].astype(np.float32)


def pt(deg, r):
    a = math.radians(deg)
    return C + math.sin(a) * r, C - math.cos(a) * r


def smin(a, b, k):
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def sd_capsule(px, py, ax, ay, bx, by, r):
    vx, vy = bx - ax, by - ay
    denom = vx * vx + vy * vy + 1e-6
    t = np.clip(((px - ax) * vx + (py - ay) * vy) / denom, 0.0, 1.0)
    return np.hypot(px - (ax + t * vx), py - (ay + t * vy)) - r


def shade_pure_liquid_glass(d, fade_mask=None):
    """Shade an SDF into a pure colorless optical glass RGBA overlay.
    - 0% blue/cyan prebaked tint.
    - 0% milky white interior fill (d < -6 has alpha = 0).
    - Neutral colorless optics: soft outer drop shadow, thin inner dark refraction
      thickness groove, and crisp white Fresnel specular meniscus highlights.
    """
    gy, gx = np.gradient(d)
    glen = np.hypot(gx, gy) + 1e-6
    nx, ny = gx / glen, gy / glen

    # Light source from top-left (-0.68, -0.68) + subtle opposing bounce
    l1 = np.clip(-(nx * 0.68 + ny * 0.68), 0.0, 1.0)
    l2 = np.clip(nx * 0.68 + ny * 0.68, 0.0, 1.0)
    spec_shoulder = 0.24 + 0.76 * (l1 ** 2.2) + 0.42 * (l2 ** 2.6)

    # Outer soft drop shadow (offset down-right slightly)
    d_sh = np.roll(d, shift=(3, 2), axis=(0, 1))
    sh_a = (
        np.clip(1.0 - np.maximum(d_sh, 0.0) / 7.5, 0.0, 1.0) ** 1.9
        * 0.42
        * np.clip(d * 0.8 + 0.5, 0.0, 1.0)
    )

    # Inner dark optical thickness groove (d around -1.8)
    dark_groove = np.exp(-((d + 1.8) / 1.15) ** 2) * 0.36

    # Colorless neutral inner caustic shimmer along meniscus shoulder
    inner_caustic = np.exp(-((d + 2.3) / 1.35) ** 2) * (0.14 + 0.34 * (l1 ** 1.6 + 0.5 * l2 ** 2.0))

    # Crisp white Fresnel outer edge rim (d around -0.45)
    white_rim = np.exp(-((d + 0.45) / 0.85) ** 2) * np.clip(spec_shoulder, 0.22, 1.0)

    # Sharp hairline specular glint on curved top-left / bottom-right shoulders
    glint = np.exp(-((d + 0.35) / 0.52) ** 2) * (l1 ** 4.0) * 0.90

    rgb = np.zeros((W, W, 3), dtype=np.float32)
    alpha = np.zeros((W, W), dtype=np.float32)

    def over(col_rgb, col_a):
        nonlocal rgb, alpha
        ca = np.clip(col_a, 0.0, 1.0)
        new_a = ca + alpha * (1.0 - ca)
        safe = np.maximum(new_a, 1e-6)
        rgb = (col_rgb * ca[..., None] + rgb * (alpha * (1.0 - ca))[..., None]) / safe[..., None]
        alpha = new_a

    over(np.array([0.0, 0.0, 0.0], dtype=np.float32), sh_a)
    over(np.array([0.0, 0.0, 0.0], dtype=np.float32), dark_groove)
    over(np.array([0.92, 0.92, 0.92], dtype=np.float32), np.clip(inner_caustic, 0.0, 0.42))
    over(np.array([1.0, 1.0, 1.0], dtype=np.float32), np.clip(white_rim * 0.78, 0.0, 0.88))
    over(np.array([1.0, 1.0, 1.0], dtype=np.float32), np.clip(glint, 0.0, 0.95))

    if fade_mask is not None:
        alpha *= fade_mask

    rgba = np.zeros((W, W, 4), dtype=np.uint8)
    rgba[..., :3] = np.clip(rgb * 255.0, 0, 255).astype(np.uint8)
    rgba[..., 3] = np.clip(alpha * 255.0, 0, 255).astype(np.uint8)
    return rgba


def crop_save(rgba, name):
    ys, xs = np.where(rgba[..., 3] > 0)
    x0 = max(0, int(xs.min()) - 2)
    y0 = max(0, int(ys.min()) - 2)
    x1 = min(W, int(xs.max()) + 3)
    y1 = min(W, int(ys.max()) + 3)
    cropped = rgba[y0:y1, x0:x1]
    out_p = os.path.join(OUT_DRAWABLE, f"{name}.png")
    Image.fromarray(cropped, mode="RGBA").save(out_p, format="PNG", optimize=True)
    return {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0, "bytes": os.path.getsize(out_p)}


def build_photo_vignette():
    """Smooth dark radial dim + vignette overlay for user background photos
    (alpha ~130 center -> 215 edge) for effortless watch face contrast and legibility.
    """
    r = np.hypot(X_GRID - C, Y_GRID - C)
    norm = np.clip(r / 225.0, 0.0, 1.0)
    alpha = 130.0 + 85.0 * (norm ** 1.7)
    arr = np.zeros((W, W, 4), dtype=np.uint8)
    arr[..., 3] = np.clip(alpha, 0, 255).astype(np.uint8)
    out_p = os.path.join(OUT_DRAWABLE, "bg_photo_vignette.png")
    Image.fromarray(arr, mode="RGBA").save(out_p, format="PNG", optimize=True)


def build_machined_dial():
    """Machined dark horological dial background (azurage graining, chamfered bezel,
    60 rehaut chapter notches, 12 radial sector hairlines, recessed orbital tracks & micro-pips).
    """
    dx = X_GRID - C
    dy = Y_GRID - C
    r = np.hypot(dx, dy)
    theta = np.arctan2(dy, dx)

    sunburst = 0.5 + 0.5 * np.cos(2.0 * theta + 0.75)
    azurage = 0.5 + 0.5 * np.sin(r * 1.55)
    vignette = np.clip(1.0 - (r / 220.0) ** 2.6, 0.0, 1.0)

    lum = 15.0 + 9.0 * vignette + 4.5 * sunburst * vignette + 2.6 * azurage
    arr = np.zeros((W, W, 4), dtype=np.uint8)
    arr[..., 0] = np.clip(lum * 0.96, 0, 255).astype(np.uint8)
    arr[..., 1] = np.clip(lum * 1.00, 0, 255).astype(np.uint8)
    arr[..., 2] = np.clip(lum * 1.18, 0, 255).astype(np.uint8)
    arr[..., 3] = 255
    arr[r > 214.0, :3] = 0

    dial = Image.fromarray(arr, mode="RGBA")

    SS = 2
    SW = W * SS
    ov = Image.new("RGBA", (SW, SW), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    cx = C * SS

    od.ellipse((cx - 214 * SS, cx - 214 * SS, cx + 214 * SS, cx + 214 * SS), outline=(56, 58, 68, 255), width=4)
    od.ellipse((cx - 208 * SS, cx - 208 * SS, cx + 208 * SS, cx + 208 * SS), outline=(10, 10, 14, 240), width=4)
    od.ellipse((cx - 204 * SS, cx - 204 * SS, cx + 204 * SS, cx + 204 * SS), outline=(255, 255, 255, 18), width=2)

    for k in range(60):
        deg = k * 6.0
        five = (k % 5 == 0)
        r1 = (205.5 if five else 208.0) * SS
        r2 = 212.0 * SS
        a = math.radians(deg)
        x1, y1 = cx + math.sin(a) * r1, cx - math.cos(a) * r1
        x2, y2 = cx + math.sin(a) * r2, cx - math.cos(a) * r2
        col = (145, 84, 44, 175) if five else (76, 80, 92, 120)
        od.line((x1, y1, x2, y2), fill=col, width=3 if five else 2)

    for h in range(12):
        a = math.radians(h * 30.0)
        x1, y1 = cx + math.sin(a) * (24 * SS), cx - math.cos(a) * (24 * SS)
        x2, y2 = cx + math.sin(a) * (203 * SS), cx - math.cos(a) * (203 * SS)
        od.line((x1, y1, x2, y2), fill=(255, 255, 255, 14), width=1)

    for r_mid, band_w in [(RH, 42 * S), (RM, 34 * S), (RS, 28 * S)]:
        rm_p = r_mid * SS
        bw_p = int(round(band_w * SS))
        od.ellipse((cx - rm_p, cx - rm_p, cx + rm_p, cx + rm_p), outline=(6, 7, 10, 130), width=bw_p)
        ri = (r_mid - band_w * 0.5) * SS
        ro = (r_mid + band_w * 0.5) * SS
        od.ellipse((cx - ri, cx - ri, cx + ri, cx + ri), outline=(255, 255, 255, 18), width=2)
        od.ellipse((cx - ro, cx - ro, cx + ro, cx + ro), outline=(255, 255, 255, 14), width=2)

    for h in range(12):
        px, py = pt(h * 30.0, RH)
        pr = 2.0 * SS
        od.ellipse((px * SS - pr, py * SS - pr, px * SS + pr, py * SS + pr), fill=(68, 70, 82, 175))
    for m in range(60):
        five = (m % 5 == 0)
        px, py = pt(m * 6.0, RM)
        pr = (1.8 if five else 1.0) * SS
        col = (90, 92, 104, 175) if five else (52, 54, 64, 130)
        od.ellipse((px * SS - pr, py * SS - pr, px * SS + pr, py * SS + pr), fill=col)
    for s_idx in range(60):
        five = (s_idx % 5 == 0)
        px, py = pt(s_idx * 6.0, RS)
        pr = (1.9 if five else 0.9) * SS
        col = (145, 75, 34, 165) if five else (54, 56, 66, 125)
        od.ellipse((px * SS - pr, py * SS - pr, px * SS + pr, py * SS + pr), fill=col)

    ov_sm = ov.resize((W, W), resample=Image.Resampling.LANCZOS)
    dial.alpha_composite(ov_sm)
    dial.convert("RGB").save(os.path.join(OUT_DRAWABLE, "dial_machined.png"), format="PNG", optimize=True)


def main():
    os.makedirs(OUT_DRAWABLE, exist_ok=True)
    rects = {}

    # 1. Default pure-black fallback photo + radial photo vignette scrim
    Image.new("RGB", (W, W), (0, 0, 0)).save(
        os.path.join(OUT_DRAWABLE, "bg_photo_default.png"), format="PNG", optimize=True
    )
    build_photo_vignette()

    # 2. Machined horological dial for Liquid Glass Blob mode
    build_machined_dial()

    # 3. Upright pure colorless glass diopter slits (used in Classic & Hidden Index modes)
    slit_specs = [
        ("glass_slit_h", RH, 19.5, 33.0),
        ("glass_slit_m", RM, 15.0, 29.5),
        ("glass_slit_s", RS, 13.5, 24.0),
    ]
    for name, r_dial, hw, hl in slit_specs:
        d = sd_capsule(X_GRID, Y_GRID, C, C - r_dial - (hl - hw), C, C - r_dial + (hl - hw), hw)
        rects[name] = crop_save(shade_pure_liquid_glass(d), name)

    # 4. Pure colorless connected blob hub + 3 flared orbiting arms (Liquid Glass Blob mode)
    r_center = np.hypot(X_GRID - C, Y_GRID - C)
    d_hub = r_center - 18.0
    rects["glass_hub"] = crop_save(shade_pure_liquid_glass(d_hub), "glass_hub")

    arm_specs = [
        ("glass_arm_h", RH, 25.5, 6.8, 22.0, 18.0),
        ("glass_arm_m", RM, 21.5, 5.2, 19.0, 16.0),
        ("glass_arm_s", RS, 19.5, 4.4, 17.0, 15.0),
    ]
    for name, r_dial, r_dome, r_neck, k_dome, k_center in arm_specs:
        d_dome = np.hypot(X_GRID - C, Y_GRID - (C - r_dial)) - r_dome
        d_neck = sd_capsule(X_GRID, Y_GRID, C, C, C, C - r_dial, r_neck)
        d_arm = smin(smin(d_hub, d_neck, k_center), d_dome, k_dome)
        root_fade = np.clip((C - Y_GRID - 8.0) / 10.0, 0.0, 1.0)
        rects[name] = crop_save(shade_pure_liquid_glass(d_arm, fade_mask=root_fade), name)

    # 5. Proximity merge bridges between adjacent domes (H<->M and M<->S) at 12 o'clock
    bridge_specs = [
        ("glass_bridge_hm", RH, 25.5, RM, 21.5, 13.5, 22.0),
        ("glass_bridge_ms", RM, 21.5, RS, 19.5, 11.5, 18.0),
    ]
    for name, r_a, rad_a, r_b, rad_b, neck_r, k_b in bridge_specs:
        ya, yb = C - r_a, C - r_b
        d_a = np.hypot(X_GRID - C, Y_GRID - ya) - rad_a
        d_b = np.hypot(X_GRID - C, Y_GRID - yb) - rad_b
        d_n = sd_capsule(X_GRID, Y_GRID, C, ya, C, yb, neck_r)
        d_br = smin(smin(d_a, d_n, k_b), d_b, k_b)
        # Keep bridge concentrated strictly in the waist gap between the two dome rims
        y_fade_a = np.clip((ya - Y_GRID - rad_a * 0.35) / 10.0, 0.0, 1.0)
        y_fade_b = np.clip((Y_GRID - yb - rad_b * 0.35) / 10.0, 0.0, 1.0)
        rects[name] = crop_save(shade_pure_liquid_glass(d_br, fade_mask=y_fade_a * y_fade_b), name)

    with open(OUT_META, "w", encoding="utf-8") as fh:
        json.dump(rects, fh, indent=2)
    print("Generated colorless liquid glass assets:", json.dumps(rects, indent=2))


if __name__ == "__main__":
    main()
