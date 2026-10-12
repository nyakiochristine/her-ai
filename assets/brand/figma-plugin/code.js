// her/ai tokens: creates colour, spacing and radius variables, plus paint and text styles.
// Run in Figma desktop: Plugins > Development > Import plugin from manifest...
const DATA = {"colors": {"beige": "#f1e9df", "green-darktech": "#0d403b", "green-highlighter": "#28b87a", "orange": "#d96a3a", "ink": "#0d403b", "white": "#ffffff", "green-highlighter-600": "#1fa268", "green-highlighter-200": "#bee9d4", "green-darktech-700": "#093230", "green-darktech-300": "#3e746f", "beige-200": "#fbf7f1", "beige-300": "#e2dacf", "orange-200": "#f2c9b5", "brush-green": "#33be87", "brush-orange": "#c05f39", "surface-page": "#f1e9df", "surface-page-alt": "#fbf7f1", "surface-muted": "#e2dacf", "surface-card": "#f1e9df", "surface-inverse": "#0d403b", "surface-inverse-2": "#093230", "surface-green": "#28b87a", "text-body": "#0d403b", "text-heading": "#0d403b", "text-muted": "#3e746f", "text-on-dark": "#f1e9df", "text-on-dark-muted": "rgba(241, 233, 223, 0.70)", "text-on-green": "#0d403b", "text-accent": "#28b87a", "border-subtle": "#dad2c8", "border-on-dark": "rgba(241, 233, 223, 0.20)", "accent": "#28b87a", "accent-hover": "#1fa268", "accent-soft": "#bee9d4", "accent-secondary": "#d96a3a", "brush": "#33be87", "focus-ring": "rgba(40, 184, 122, 0.45)"}, "spacing": {"space-1": 4.0, "space-2": 8.0, "space-3": 12.0, "space-4": 16.0, "space-5": 24.0, "space-6": 32.0, "space-7": 48.0, "space-8": 64.0, "space-9": 96.0, "space-10": 128.0, "section-y": 80.0, "section-y-large": 128.0}, "radius": {"radius-sm": 4.0, "radius-md": 8.0, "radius-lg": 16.0, "radius-pill": 999.0}, "textStyles": [{"name": "Titles/display-hero", "family": "MyeongjoExt", "style": "Regular", "size": 76.0, "lh": 1.08, "ls": -0.01, "upper": false}, {"name": "Titles/display", "family": "MyeongjoExt", "style": "Regular", "size": 60.0, "lh": 1.08, "ls": -0.01, "upper": false}, {"name": "Titles/title-page", "family": "MyeongjoExt", "style": "Regular", "size": 48.0, "lh": 1.08, "ls": 0, "upper": false}, {"name": "Titles/title-section", "family": "MyeongjoExt", "style": "Regular", "size": 36.0, "lh": 1.25, "ls": 0, "upper": false}, {"name": "Titles/title-card", "family": "MyeongjoExt", "style": "Regular", "size": 28.0, "lh": 1.25, "ls": 0, "upper": false}, {"name": "Titles/title-small", "family": "MyeongjoExt", "style": "Regular", "size": 22.0, "lh": 1.25, "ls": 0, "upper": false}, {"name": "Body/lead", "family": "DM Sans", "style": "Regular", "size": 18.0, "lh": 1.5, "ls": 0, "upper": false}, {"name": "Body/body", "family": "DM Sans", "style": "Regular", "size": 16.0, "lh": 1.5, "ls": 0, "upper": false}, {"name": "Body/body-long", "family": "DM Sans", "style": "Regular", "size": 16.0, "lh": 1.7, "ls": 0, "upper": false}, {"name": "Body/body-strong", "family": "DM Sans", "style": "Bold", "size": 16.0, "lh": 1.5, "ls": 0, "upper": false}, {"name": "Body/caption", "family": "DM Sans", "style": "Regular", "size": 14.0, "lh": 1.5, "ls": 0, "upper": false}, {"name": "Body/eyebrow", "family": "DM Sans", "style": "Bold", "size": 12.0, "lh": 1.5, "ls": 0.08, "upper": true}]};

function hexToRgb(h) {
  if (h.startsWith('rgba')) {
    const m = h.match(/[\d.]+/g).map(Number);
    return { rgb: { r: m[0] / 255, g: m[1] / 255, b: m[2] / 255 }, a: m[3] };
  }
  const n = parseInt(h.slice(1), 16);
  return { rgb: { r: ((n >> 16) & 255) / 255, g: ((n >> 8) & 255) / 255, b: (n & 255) / 255 }, a: 1 };
}

(async () => {
  const log = [];
  const colorCol = figma.variables.createVariableCollection('her/ai colour');
  const cMode = colorCol.modes[0].modeId;
  for (const [name, hex] of Object.entries(DATA.colors)) {
    const { rgb, a } = hexToRgb(hex);
    const v = figma.variables.createVariable(name, colorCol, 'COLOR');
    v.setValueForMode(cMode, { ...rgb, a });
    const ps = figma.createPaintStyle();
    ps.name = 'her-ai/' + name;
    ps.paints = [{ type: 'SOLID', color: rgb, opacity: a }];
  }
  const numCol = figma.variables.createVariableCollection('her/ai spacing and radius');
  const nMode = numCol.modes[0].modeId;
  for (const [name, val] of Object.entries(DATA.spacing)) {
    const v = figma.variables.createVariable('spacing/' + name, numCol, 'FLOAT');
    v.setValueForMode(nMode, val);
  }
  for (const [name, val] of Object.entries(DATA.radius)) {
    const v = figma.variables.createVariable('radius/' + name, numCol, 'FLOAT');
    v.setValueForMode(nMode, Math.min(val, 999));
  }
  for (const s of DATA.textStyles) {
    try {
      await figma.loadFontAsync({ family: s.family, style: s.style });
      const ts = figma.createTextStyle();
      ts.name = s.name;
      ts.fontName = { family: s.family, style: s.style };
      ts.fontSize = s.size;
      ts.lineHeight = { unit: 'PERCENT', value: s.lh * 100 };
      ts.letterSpacing = { unit: 'PERCENT', value: s.ls * 100 };
      if (s.upper) ts.textCase = 'UPPER';
    } catch (e) {
      log.push('skipped text style ' + s.name + ': install ' + s.family + ' ' + s.style);
    }
  }
  figma.closePlugin('her/ai tokens created.' + (log.length ? ' ' + log.join('; ') : ''));
})();
