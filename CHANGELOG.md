# Changelog

## 1.3
- **True Static Indexes + Smooth `1.16×` Optical Zoom (Zero Number Popping)**: removed per-numeral visibility thresholds in `z_ringM` and `z_ringS` across all 3 dial modes (*Classic Three Lens*, *Hidden Index Reveal*, *Liquid Glass Blob*). All numerals stay completely static (`alpha="255"`) while the glass aperture zooms (`scaleX="1.16" scaleY="1.16"`) and glides smoothly over both the index rings and any user-selected photo
- **100% Pure Colorless Glass Lenses**: stripped all prebaked cyan/blue dispersion tints and milky white fills from every active and AOD lens sprite (`glass_slit_*`, `glass_arm_*`, `glass_bridge_*`, `glass_hub`, and AOD monolith/eclipse optics)—leaving crystal-clear interiors with neutral refractive dark grooves and specular Fresnel edge rims
- **Dimmed Radial Vignette for Custom Photos**: added `bg_photo_vignette.png` over user-selected `<PhotosConfiguration>` backgrounds so time remains effortlessly legible across bright wallpapers
- **Fixed Always-On Display Across All Dial Modes**: rebuilt AOD Style 0 (*Dual orbit lenses*) with lightweight pure-vector OLED black capsules and dynamic counter-rotated `[HOUR_1_12]` / `[MINUTE_Z]` templates (zero `renderMode="MASK"` / `<PartImage>` / theme-bleed issues)
- **Liquid Glass Blob Proximity Merge Bridges**: added `blob_merge_hm` and `blob_merge_ms` colorless meniscus bridges driven by angular proximity (`clamp(1 - abs(delta) / 26.0, 0, 1)`) so lobes merge and separate smoothly as they pass each other

## 1.2
- Upgraded to Watch Face Format v4 (`minSdk = 36`) with native `<PhotosConfiguration>` custom photo support, 3 selectable dial styles, true static `GoogleSansRounded` weights, and watch-font Day/Date + `[BATTERY_PERCENT]` arc telemetry

## 1.1
- Smooth-gliding continuous `[SECOND_MILLISECOND]` motion, per-ring 6-weight × 6-width controls, and 3 glass-native AOD styles

## 1.0
- Initial release of **Three Lens Watch Face** for Galaxy Watch 7 (One UI Watch 9 / Wear OS 6)
