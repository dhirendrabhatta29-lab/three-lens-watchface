# Customization guide

Long-press the watch face, then tap **Customize** (the pencil / gear).

## Presets (flavors)

Three one-tap presets are included: **Classic Three Lens** *(default)*, **Hidden Index Reveal**, and **Liquid Glass Blob**.

## Dial Style (`dial_style`, 3 options)

- **Classic Three Lens** *(default)*: keeps all three stationary concentric index rings visible on pure black (or theme/photo background) with three smooth-gliding pure-glass diopter slits
- **Hidden Index Reveal**: hides the concentric numerals behind subtle dark orbital tracks so numbers only emerge and magnify inside the orbiting glass diopter slits
- **Liquid Glass Blob**: displays a machined circular-azurage horological dial (`dial_machined`) with micro-dot index pips, a connected tri-lobed crystal-clear glass silhouette anchored at the center jewel, and watch-font (`GoogleSansRounded`) **Day/Date** and curved **Battery %** telemetry cleanly placed between the Hour and Minute rings

## Custom Photo & Background (`bg_mode` + `<PhotosConfiguration>`)

- **Background**: **Pure black** *(default)*, **Theme color**, or **Custom photo**
- **Custom Photo Picker (`bg_photo`)**: choose any personal picture from the Wear / Galaxy Wearable watch face editor; rendered full-bleed with a subtle legibility scrim under crystal-clear glass (with zero milky white tint)

## Theme (17 options)

Sets the dial background, bezel, primary numeral ink, dimmed index ink, and seconds accent color:
*Mono* (default), *OLED Black*, *Metro*, *Catppuccin*, *Gruvbox*, *Nord*, *Tokyo Night*, *Dracula*, *Rosé Pine*, *Everforest*, *Solarized*, *M3 Purple*, *M3 Blue*, *M3 Teal*, *M3 Green*, *M3 Rose*, *M3 Amber*.

## Per-Ring Typography (6 Weights × 6 Widths Individually for Hours, Minutes, and Seconds)

Each ring has its own independent **weight** and **width** setting:
- **Hours weight** & **Hours width**
- **Minutes weight** & **Minutes width**
- **Seconds weight** & **Seconds width**

### Weight options (6)
- Thin (`100`)
- Extra light (`200`)
- Light (`300`)
- Medium (`500`)
- Bold (`700`)
- Black (`900`)

### Width options (6)
- Ultra condensed (`0.74×`)
- Condensed (`0.86×`)
- Normal (`1.00×`, *default*)
- Semi expanded (`1.13×`)
- Expanded (`1.26×`)
- Ultra expanded (`1.40×`)

## Additional Options

- **Hours orientation**: *Upright* (default), *Radial*, *Pointing*
- **Diopter refraction**: *Subtle*, *Balanced*, *Exaggerated* (default)
- **Always-on brightness**: *Dim* (default), *Normal*

## Always-On Display Styles (3 Exclusive Glass Designs)

| Style | Description |
| --- | --- |
| Dual orbit lenses *(default)* | dimmed stationary Hour and Minute index rings with wide orbiting Hour & Minute frameless glass diopter slits magnifying the active numerals and bending adjacent numerals at the edges |
| Triple monolith slits | three horizontal frameless glass capsule slits stacked across the dial: top Hour slit with flanking hours, wide middle Minute slit with `m-1` and `m+1` refracting inside the glass edges, and bottom Day/Date slit |
| Eclipse glass ring | an orbiting `110°` crescent glass ring lens illuminating the active arc of the stationary minute index around a central circular glass diopter orb |
