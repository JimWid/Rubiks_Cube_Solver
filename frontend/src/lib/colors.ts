export const HSV_RANGES: Record<string, [[number, number, number], [number, number, number]]> = {
    red:    [[0, 130, 100], [8, 255, 255]],
    orange: [[6, 130, 100], [22, 255, 255]],
    yellow: [[26, 100, 100], [40, 255, 255]],
    green:  [[41, 80, 80], [85, 255, 255]],
    blue:   [[86, 100, 100], [130, 255, 255]],
    white:  [[0, 0, 160], [131, 60, 255]],
};

export const COLOR_TO_FACE_MAP: Record<string, string> = {
    white: "U",
    red: "R",
    green: "F",
    yellow: "D",
    orange: "L",
    blue: "B",
};

export const KOCIEMBA_FACE_ORDER = ['U', 'R', 'F', 'D', 'L', 'B'];

export function generateKociembaString(state: Record<string, string[]>): string {
  // Validate faces are present and have 9 stickers
  for (const f of KOCIEMBA_FACE_ORDER) {
    if (!(f in state) || !Array.isArray(state[f]) || state[f].length !== 9) {
      return 'Error: not all faces have been scanned';
    }
    if (state[f].some((c) => c === null || c === undefined || c === 'unknown')) {
      return 'Error: not all faces have been scanned';
    }
  }

  let kociemba = '';
  for (const face of KOCIEMBA_FACE_ORDER) {
    for (const color of state[face]) {
      const mapped = COLOR_TO_FACE_MAP[color];
      if (!mapped) throw new Error(`Invalid color name '${color}'`);
      kociemba += mapped;
    }
  }

  if (kociemba.length !== 54) {
    throw new Error(`Invalid cube string length: ${kociemba.length}. Should be 54.`);
  }

  const counts: Record<string, number> = {};
  for (const ch of kociemba) counts[ch] = (counts[ch] || 0) + 1;
  for (const faceChar of 'URFDLB') {
    if (counts[faceChar] !== 9) {
      throw new Error(
        `Invalid cube facelet '${faceChar}' appears ${counts[faceChar] || 0} times instead of 9.`
      );
    }
  }

  return kociemba;
}

export function getColorName(h: number, s: number, v: number): string | null {
  // White check (low saturation, high value)
  const white = HSV_RANGES['white'];
  if (white[0][1] <= s && s <= white[1][1] && white[0][2] <= v && v <= white[1][2]) {
    return 'white';
  }

  // Red special-case (as in original Python)
  if (165 <= h && h <= 179 && s > 120 && v > 100) {
    return 'red';
  }

  // Iterate other ranges (skip red and white which were handled)
  for (const color of Object.keys(HSV_RANGES)) {
    if (color === 'red' || color === 'white') continue;
    const [lower, upper] = HSV_RANGES[color];
    if (lower[0] <= h && h <= upper[0] && lower[1] <= s && s <= upper[1] && lower[2] <= v && v <= upper[2]) {
      return color;
    }
  }

  return null;
}

 // h: 0-179
 // s: 0-255
 // v: 0-255
export function rgbToHsv(r: number, g: number, b: number): [number, number, number] {
  const rPrime = r / 255;
  const gPrime = g / 255;
  const bPrime = b / 255;

  const max = Math.max(rPrime, gPrime, bPrime);
  const min = Math.min(rPrime, gPrime, bPrime);
  const delta = max - min;

  let hDeg = 0;
  if (delta !== 0) {
    if (max === rPrime) {
      hDeg = 60 * (((gPrime - bPrime) / delta) % 6);
    } else if (max === gPrime) {
      hDeg = 60 * (((bPrime - rPrime) / delta) + 2);
    } else {
      hDeg = 60 * (((rPrime - gPrime) / delta) + 4);
    }
  }
  if (hDeg < 0) hDeg += 360;

  const h = Math.round(hDeg / 2) % 180; // scale 0-360 -> 0-179
  const s = Math.round((max === 0 ? 0 : delta / max) * 255);
  const v = Math.round(max * 255);
  return [h, s, v];
}

function median(arr: number[]) {
  if (arr.length === 0) return 0;
  const sorted = arr.slice().sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  if (sorted.length % 2 === 0) return Math.round((sorted[mid - 1] + sorted[mid]) / 2);
  return sorted[mid];
}

export async function ColorGrid(
  ctx: CanvasRenderingContext2D,
  x: number, y: number, w: number, h: number,
  rows = 3, cols = 3
) {
  const colors: string[] = [];

  // Calculate padding and sticker
  const paddingX = Math.floor((w * 0.1) / 3);
  const paddingY = Math.floor((h * 0.1) / 3);

  const stickerW = Math.floor((w - 2 * paddingX * 3) / 3);
  const stickerH = Math.floor((h - 2 * paddingY * 3) / 3);

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const sx = Math.round(x + c * (stickerW + 2 * paddingX) + paddingX);
      const sy = Math.round(y + r * (stickerH + 2 * paddingY) + paddingY);
      const sw = Math.max(1, stickerW);
      const sh = Math.max(1, stickerH);

      // Clip to canvas bounds
      const sxClipped = Math.max(0, Math.min(ctx.canvas.width - 1, sx));
      const syClipped = Math.max(0, Math.min(ctx.canvas.height - 1, sy));
      const swClipped = Math.max(1, Math.min(ctx.canvas.width - sxClipped, sw));
      const shClipped = Math.max(1, Math.min(ctx.canvas.height - syClipped, sh));

      try {
        const img = ctx.getImageData(sxClipped, syClipped, swClipped, shClipped);
        const hs: number[] = [];
        const ss: number[] = [];
        const vs: number[] = [];

        for (let i = 0; i < img.data.length; i += 4) {
          const r = img.data[i];
          const g = img.data[i + 1];
          const b = img.data[i + 2];
          const [hh, ssVal, vv] = rgbToHsv(r, g, b);
          hs.push(hh);
          ss.push(ssVal);
          vs.push(vv);
        }

        const mh = median(hs);
        const ms = median(ss);
        const mv = median(vs);
        colors.push(getColorName(mh, ms, mv) || 'unknown');
      } catch (e) {
        // Fallback: sample center pixel
        const cx = Math.round(x + (c + 0.5) * (w / cols));
        const cy = Math.round(y + (r + 0.5) * (h / rows));
        const px = ctx.getImageData(cx, cy, 1, 1);
        const [hh, ssVal, vv] = rgbToHsv(px.data[0], px.data[1], px.data[2]);
        colors.push(getColorName(hh, ssVal, vv) || 'unknown');
      }
    }
  }

  return colors;
}