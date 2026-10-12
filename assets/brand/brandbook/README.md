# her/ai brandbook for Figma

Built from the her/ai design system artifact. Ten pages, 1440 x 1024 each.

## 1. Import the pages
1. Open Figma and create a new design file.
2. Select all ten files in `01-cover.svg` to `10-checklist.svg` and drag them onto the canvas.
3. Each SVG becomes one frame. Rename the frames if you like, then set them to a Section or a Page each.

All type is converted to outlines, so the pages look right without installing fonts. The trade-off: the text is vector shapes, not editable text. Layer names carry the original copy so you can find it, and you can retype it with the real fonts (below).

## 2. Create variables and text styles (optional)
1. Install the fonts first: `MyeongjoExt-Regular.ttf` and DM Sans from the design system `fonts/` folder.
2. In Figma desktop: Plugins > Development > Import plugin from manifest, and pick `figma-plugin/manifest.json`.
3. Run "her/ai tokens". It creates a colour collection, a spacing and radius collection, paint styles and text styles.

The plugin has not been run inside Figma by me, so treat its first run as a test. If a font is missing it skips that text style and says so.

`herai-tokens.json` holds the same values if you prefer another token plugin.

## Notes
- MyeongjoExt licensing is unverified in the source. Check with Sandoll before using it publicly.
- Some logo file names in the source do not match the colours inside them. The brandbook labels each tile by file name.
