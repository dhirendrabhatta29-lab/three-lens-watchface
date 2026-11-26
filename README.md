# Three Lens Watch Face

**A Wear OS 6 (One UI Watch 9) Watch Face Format v3 watch face with three fixed concentric index rings, three wide orbiting frameless light-bending glass diopter slits that glide smoothly over the index and refract adjacent numerals at their edges, independent 6-weight × 6-width controls for every ring, 17 color themes, and 3 exclusive glass AOD styles.**

![Build](../../actions/workflows/build.yml/badge.svg)
![Wear OS 6](https://img.shields.io/badge/Wear%20OS-6-4285F4)
![Watch Face Format](https://img.shields.io/badge/Watch%20Face%20Format-v3-34A853)
![License](https://img.shields.io/badge/license-MIT-blue)

Three stationary concentric numeral and tick rings (**Hours** `1..12`, **Minutes** `00..59`, **Seconds** `00..59`) sit on the dial while three wider frameless optical glass diopter slits glide smoothly over them—magnifying the active numerals and bending adjacent numerals as they enter and exit the curved caustic edges of each glass lens.

## Features

- **Smooth-Gliding Wider Frameless Glass Diopter Slits**:
  - Pure optical glass refraction (`renderMode="MASK"` + radial caustic dome + peripheral refraction vignette + inner refraction halo + meniscus sheen + translucent specular rim) with zero opaque colored borders.
  - **Wider lens apertures** (`51×78` Hour at `1.62×`, `41×69` Minute at `1.95×`, `35×55` Second at `1.82×`) so adjacent numerals bend and refract along the curved glass periphery as the Minute and Second lenses glide continuously (`[SECOND_MILLISECOND]`) over the stationary index.
- **Individual 6-Weight × 6-Width Controls per Ring**:
  - Separate **Hours weight** & **Hours width**, **Minutes weight** & **Minutes width**, and **Seconds weight** & **Seconds width** (6 weights × 6 widths = 36 combinations independently per ring, `$36^3 = 46,656$` total typographic combinations!).
  - **Weights**: *Thin*, *Extra light*, *Light*, *Medium*, *Bold*, *Black*
  - **Widths**: *Ultra condensed* (`0.74×`), *Condensed* (`0.86×`), *Normal* (`1.00×`), *Semi expanded* (`1.13×`), *Expanded* (`1.26×`), *Ultra expanded* (`1.40×`)
- **17 Built-in Themes**: *Mono*, *OLED Black*, *Metro*, *Catppuccin*, *Gruvbox*, *Nord*, *Tokyo Night*, *Dracula*, *Rosé Pine*, *Everforest*, *Solarized*, plus 6 Material 3 tonal palettes (*M3 Purple*, *M3 Blue*, *M3 Teal*, *M3 Green*, *M3 Rose*, *M3 Amber*).
- **3 Exclusive Optical-Glass Always-On (AOD) Styles**:
  - **Dual orbit lenses** *(default)* — dimmed stationary Hour & Minute index with wide orbiting Hour & Minute frameless glass diopter slits magnifying the index and bending adjacent numerals at the edges.
  - **Triple monolith slits** — three horizontal frameless glass capsule slits stacked across the dial (top Hour slit with flanking hours, wide center Minute slit with `m-1` and `m+1` refracting inside the glass edges, and bottom Day/Date glass slit).
  - **Eclipse glass ring** — an orbiting `110°` crescent glass ring lens illuminating the active arc of the stationary minute index around a central circular glass diopter orb.
- **Zero Code, Zero AOD Lag**: Pure declarative Watch Face Format v3 (`android:hasCode="false"`), batched `<Line>` tick rings, zero second-level expressions in AOD, and `±4px` 5×5 OLED burn-in pixel shifting.

## Install

```bash
adb connect <watch-ip>:<port>
adb install -r three-lens-v1.1.apk
```
