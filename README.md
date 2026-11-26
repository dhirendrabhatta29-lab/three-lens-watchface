# Three Lens Watch Face

**A Wear OS 6 (One UI Watch 9) Watch Face Format v3 watch face with three fixed concentric index rings, three orbiting frameless light-bending glass diopter slits, 6 font weights × 6 font widths, 17 color themes, and 5 OLED burn-in-safe AOD styles.**

![Build](../../actions/workflows/build.yml/badge.svg)
![Wear OS 6](https://img.shields.io/badge/Wear%20OS-6-4285F4)
![Watch Face Format](https://img.shields.io/badge/Watch%20Face%20Format-v3-34A853)
![License](https://img.shields.io/badge/license-MIT-blue)

Three fixed concentric numeral and tick rings (**Hours** `1..12`, **Minutes** `00..59`, **Seconds** `00..59`) stay stationary on the dial while three frameless optical glass diopter slits orbit above them—bending light around their edges and magnifying the exact hour, minute, and second they pass over.

## Features

- **Three Orbiting Frameless Glass Diopter Slits**:
  - Pure optical glass refraction (`renderMode="MASK"` + radial caustic dome + peripheral refraction vignette + meniscus sheen + translucent specular rim) with zero opaque colored borders—just a slit of glass that bends light and enlarges the index underneath.
  - **Hour lens** (`1.65×` magnification), **Minute lens** (`2.15×` magnification, smooth continuous sweep), and **Second lens** (`1.90×` magnification, cubic ease-out step every second).
- **6 Font Weights × 6 Font Widths** (36 typographic combinations using bundled **Google Sans Flex Rounded**):
  - **Font weight**: *Thin*, *Extra light*, *Light*, *Medium*, *Bold*, *Black*
  - **Font width**: *Ultra condensed* (`0.74×`), *Condensed* (`0.86×`), *Normal* (`1.00×`), *Semi expanded* (`1.13×`), *Expanded* (`1.26×`), *Ultra expanded* (`1.40×`)
- **Configurable Ring Orientations**:
  - **Hours orientation**: *Upright* (default), *Radial*, *Pointing*
  - **Min/Sec orientation**: *Radial* (default), *Pointing*
- **17 Built-in Themes**: *Mono*, *OLED Black*, *Metro*, *Catppuccin*, *Gruvbox*, *Nord*, *Tokyo Night*, *Dracula*, *Rosé Pine*, *Everforest*, *Solarized*, plus 6 Material 3 tonal palettes (*M3 Purple*, *M3 Blue*, *M3 Teal*, *M3 Green*, *M3 Rose*, *M3 Amber*).
- **5 Bold, Burn-In-Protected Always-On (AOD) Styles**:
  - **Three lenses** (sparse index with moving Hour & Minute glass diopter slits)
  - **Chunky stack** (smaller filled bold Hour over a huge chunky outline bold Minute + date)
  - **Activity rings** (three full-360° bold concentric rings for Steps, Calories, and Active Time)
  - **Minutes pie** (streamlined radial wedge + chunky Hour/Minute + centered live step count)
  - **Minimal slit** (frameless glass slit framing chunky Hour & outline Minute)
- **Zero Code, Zero Lag**: Pure declarative Watch Face Format v3 (`android:hasCode="false"`), batched `<Line>` tick rings, zero second-level expressions in AOD, and `±4px` 5×5 OLED burn-in pixel shifting.

## Install

```bash
adb connect <watch-ip>:<port>
adb install -r three-lens-v1.0.apk
```
