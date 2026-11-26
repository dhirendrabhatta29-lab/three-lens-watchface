# Changelog

## 1.2
- **Upgraded to Watch Face Format v4 (`minSdk = 36`)**: added native `<PhotosConfiguration>` support so users can select any custom background photo alongside *Pure black* (default) and *Theme color*
- **Three Selectable Dial Styles (`dial_style`)**:
  - **Classic Three Lens** *(default)*: stationary concentric Hour, Minute, and Second rings with pure-black background and smooth-gliding optical diopter slits
  - **Hidden Index Reveal**: hidden stationary indexes over subtle orbital tracks that smoothly emerge and magnify inside the orbiting diopters
  - **Liquid Glass Blob**: machined radial-sunburst & circular-azurage horological dial with micro-dot index pips, a single connected tri-lobed liquid glass silhouette, and watch-font (`GoogleSansRounded`) Day/Date (`[DAY_OF_WEEK_S] [DAY]`) and dynamic `[BATTERY_PERCENT]` arc telemetry positioned symmetrically between the Hour and Minute tracks (no dial text branding)
- **Pure Crystal-Clear Apple-Style Liquid Glass**: removed all milky white interior fills; replaced glass optics across active and AOD modes with transparent crystal interiors featuring cyan/aqua chromatic edge dispersion, dark refractive grooves, and Fresnel specular highlights (`Kyant0/AndroidLiquidGlass` style)
- **Official Static Google Sans Rounded Fonts**: instantiated all 6 true static weights (`Thin 140`, `ExtraLight 260`, `Light 380`, `Medium 530`, `Bold 700`, `Black 900`) directly from `GoogleSansRounded-Regular.ttf`

## 1.1
- **Smooth-gliding wider glass diopters**: Minute and Second diopters now glide continuously (`[SECOND_MILLISECOND]`) over the actual stationary index rings using counter-rotated magnified ring layers, with tight optical rim refraction
- **Per-ring Weight & Width controls**: added individual 6-option weight and 6-option width settings for **Hours** (`h_weight`, `h_width`), **Minutes** (`m_weight`, `m_width`), and **Seconds** (`s_weight`, `s_width`)
- **3 new exclusive AOD styles**: replaced previous AOD styles with three glass-diopter-native designs—**Dual orbit lenses**, **Triple monolith slits**, and **Eclipse glass ring**

## 1.0
- Initial release of **Three Lens Watch Face** for Galaxy Watch 7 (One UI Watch 9 / Wear OS 6, WFF v3)
