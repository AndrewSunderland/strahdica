#!/usr/bin/env python3
"""
Generate a full-logo animation as a sequence of PNG frames.
Usage:
    python3 tools/generate_logo.py "STRAHDICA" --frames 30
Outputs:
    game/gui/frames/frame_0000.png ... frame_N.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys, random, argparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUI_DIR = os.path.join(ROOT, "gui")
FONTS_DIR = os.path.join(ROOT, "fonts")
FRAMES_DIR = os.path.join(GUI_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

# Config defaults
TITLE_COLOR = (242, 230, 210, 255)
OUTLINE_COLOR = (38, 14, 18, 255)
DRIP_COLOR = (138, 11, 11, 220)
BG = (0, 0, 0, 0)

def load_font_file(size):
    preferred = os.path.join(FONTS_DIR, "AtkinsonHyperlegible-Regular.ttf")
    if os.path.exists(preferred):
        return ImageFont.truetype(preferred, size)
    # fallback to default PIL font
    return ImageFont.load_default()

def draw_text_outline(draw, pos, text, font, fill, outline, outline_w=6):
    x, y = pos
    for dx in range(-outline_w, outline_w+1):
        for dy in range(-outline_w, outline_w+1):
            if dx*dx + dy*dy <= outline_w*outline_w:
                draw.text((x+dx, y+dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)

def build_base(text, font_size):
    font = load_font_file(font_size)
    dummy = Image.new("RGBA", (10,10), BG)
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0,0), text, font=font)
    width = bbox[2] - bbox[0] + 160
    height = bbox[3] - bbox[1] + 260
    base = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(base)
    x = 80
    y = 40
    draw_text_outline(draw, (x, y), text, font, TITLE_COLOR, OUTLINE_COLOR, outline_w=6)
    # collect per-letter boxes for drip placement
    xpos = x
    per = []
    for ch in text:
        ch_bbox = draw.textbbox((xpos, y), ch, font=font)
        ch_w = ch_bbox[2] - ch_bbox[0]
        ch_h = ch_bbox[3] - ch_bbox[1]
        per.append((ch, (xpos, y, ch_w, ch_h)))
        xpos += ch_w
    return base, per, font

def make_drip_specs(per_boxes, frame_count):
    random.seed(1)
    specs = []
    for ch, (lx, ly, lw, lh) in per_boxes:
        # each letter gets 0..2 drips
        n = random.choice([0,0,1,1,2])
        for i in range(n):
            cx = int(lx + random.uniform(0.15, 0.85) * lw)
            # place pool so it slightly overlaps the bottom of the glyph
            top_y = int(ly + lh - random.uniform(2, 6))
            fall = int(lh * random.uniform(0.25, 0.55)) + 30
            width = max(3, int(lw * random.uniform(0.04, 0.09)))
            # pool dimensions (wider than single drip)
            pool_w = max(width * 2, int(lw * random.uniform(0.28, 0.5)))
            pool_depth = max(6, int(lh * random.uniform(0.04, 0.09)))
            phase = random.randint(0, frame_count-1)
            specs.append({
                "cx": cx,
                "top_y": top_y,
                "fall": fall,
                "w": width,
                "pool_w": pool_w,
                "pool_depth": pool_depth,
                "phase": phase,
                "length": int(fall * random.uniform(0.6, 0.95))
            })
    return specs

def render_frame(base_im, specs, frame_idx, frame_count):
    im = base_im.copy()
    draw = ImageDraw.Draw(im, "RGBA")
    for s in specs:
        # loopable progress in [0,1)
        prog = ((frame_idx + s["phase"]) % frame_count) / float(frame_count)
        # progress 0..1 maps to yoffset 0..fall
        yoff = int(prog * s["fall"])
        # pool base (touching glyph)
        pool_top = s["top_y"]
        pool_w = s["pool_w"]
        pool_depth = s["pool_depth"]

        # pool alpha fades slightly as drips depart
        if prog > 0.85:
            pool_alpha = int(180 * max(0.0, 1.0 - (prog - 0.85) / 0.15))
        else:
            pool_alpha = 200
        pool_color = (DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], pool_alpha)

        # draw pool (ellipse) so it visually 'sits' on the glyph baseline
        draw.ellipse([s["cx"] - pool_w, pool_top - pool_depth//2,
                      s["cx"] + pool_w, pool_top + pool_depth//2],
                     fill=pool_color)

        # small pooled highlights (lighter, near top edge)
        hl_color = (min(255, DRIP_COLOR[0]+30), min(255, DRIP_COLOR[1]+20), min(255, DRIP_COLOR[2]+20),
                    int(pool_alpha*0.45))
        draw.ellipse([s["cx"] - pool_w//2, pool_top - pool_depth//2 - 2,
                      s["cx"] - pool_w//2 + pool_w//3, pool_top + pool_depth//4],
                     fill=hl_color)

        # drip start position is just below the pool
        cy = pool_top + pool_depth//2 + yoff
        length = s["length"]
        w = s["w"]

        # head alpha fades near end of its fall
        if prog > 0.80:
            head_alpha = int(255 * max(0.0, 1.0 - (prog - 0.80)/0.20))
        else:
            head_alpha = 255
        head_color = (DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], int(DRIP_COLOR[3]*head_alpha/255))

        # draw drop head and tail
        draw.ellipse([s["cx"] - w, cy - 4, s["cx"] + w, cy + 8], fill=head_color)
        draw.rectangle([s["cx"] - w//2, cy + 4, s["cx"] + w//2, cy + length], fill=head_color)

        # occasional small splat near bottom
        if prog > 0.5 and random.Random(s["cx"] + s["phase"] + frame_idx).random() > 0.92:
            sx = s["cx"] + int(random.uniform(-w*2, w*2))
            sy = cy + length - random.randint(0,6)
            draw.ellipse([sx-6, sy-4, sx+6, sy+6], fill=(180,20,20,int(180*head_alpha/255)))

    # soften drips + pool slightly
    im = im.filter(ImageFilter.GaussianBlur(radius=0.7))
    return im

def generate_animation(text, frames):
    base, per, font = build_base(text, font_size=220)
    specs = make_drip_specs(per, frames)
    for i in range(frames):
        frame = render_frame(base, specs, i, frames)
        out = os.path.join(FRAMES_DIR, f"frame_{i:04d}.png")
        frame.save(out)
    print(f"Saved {frames} frames to {FRAMES_DIR}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", default="STRAHDICA")
    parser.add_argument("--frames", type=int, default=30)
    args = parser.parse_args()
    generate_animation(args.text, args.frames)

if __name__ == "__main__":
    main()