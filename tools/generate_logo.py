#!/usr/bin/env python3
"""
Generate a full-logo animation as a sequence of PNG frames.
Usage:
    python3 tools/generate_logo.py "STRAHDICA" --frames 30
Outputs:
    game/gui/frames/frame_0000.png ... frame_N.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys, random, argparse, math

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
    # Build a transparent image that contains ONLY the outlined text.
    font = load_font_file(font_size)
    dummy = Image.new("RGBA", (10,10), BG)
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0,0), text, font=font)
    width = bbox[2] - bbox[0] + 160
    height = bbox[3] - bbox[1] + 260
    # base_text will hold the text and outline so it can be composited on top of pools.
    base_text = Image.new("RGBA", (width, height), BG)
    draw_text = ImageDraw.Draw(base_text)
    x = 80
    y = 40
    draw_text_outline(draw_text, (x, y), text, font, TITLE_COLOR, OUTLINE_COLOR, outline_w=8)

    # collect per-letter boxes for drip placement (coordinates relative to base_text)
    xpos = x
    per = []
    for ch in text:
        ch_bbox = draw_text.textbbox((xpos, y), ch, font=font)
        ch_w = ch_bbox[2] - ch_bbox[0]
        ch_h = ch_bbox[3] - ch_bbox[1]
        per.append((ch, (xpos, y, ch_w, ch_h)))
        xpos += ch_w
    return base_text, per, font

def _ease_out_cubic(t):
    # smooth ease-out for stretching
    return 1 - pow(1 - t, 3)

def make_drip_specs(per_boxes, frame_count):
    random.seed(1)
    specs = []
    for ch, (lx, ly, lw, lh) in per_boxes:
        n = random.choice([0,0,1,1,2])
        for i in range(n):
            cx = int(lx + random.uniform(0.15, 0.85) * lw)
            pool_w = max(6, int(lw * random.uniform(0.28, 0.5)))
            pool_depth = max(6, int(lh * random.uniform(0.04, 0.09)))
            pool_top = int(ly + lh + (pool_depth // 2) + random.uniform(0, 2))
            fall = int(lh * random.uniform(0.25, 0.55)) + 30
            width = max(3, int(lw * random.uniform(0.04, 0.09)))
            phase = random.randint(0, frame_count-1)
            # stretching parameters
            tension = random.uniform(0.55, 1.15)        # how long the neck can stretch relative to fall
            neck_segments = random.randint(6, 14)       # number of ellipses used to draw the neck
            drop_period = random.randint(max(6,int(frame_count*0.15)), max(10,int(frame_count*0.4)))
            specs.append({
                "cx": cx,
                "pool_top": pool_top,
                "fall": fall,
                "w": width,
                "pool_w": pool_w,
                "pool_depth": pool_depth,
                "phase": phase,
                "length": int(fall * random.uniform(0.6, 0.95)),
                "tension": tension,
                "segments": neck_segments,
                "drop_period": drop_period,
            })
    return specs

def render_frame(base_text_im, specs, frame_idx, frame_count):
    # Draw pools & viscous stretching drips + detached droplets, then composite text on top.
    width, height = base_text_im.size
    backdrop = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(backdrop, "RGBA")

    for s in specs:
        prog = ((frame_idx + s["phase"]) % frame_count) / float(frame_count)
        # eased progress for smoother motion (0..1)
        eprog = _ease_out_cubic(prog)
        # total drop travel (head)
        head_y = s["pool_top"] + int(eprog * s["fall"])
        # neck length increases smoothly with progress and tension
        max_neck = int(s["tension"] * s["fall"])
        neck_len = int(max_neck * eprog)
        # draw pool first (same as before, slightly adjusted)
        pool_top = s["pool_top"]
        pool_w = s["pool_w"]
        pool_depth = s["pool_depth"]
        pool_alpha = int(200 * (1.0 if prog < 0.85 else max(0.0, 1.0 - (prog - 0.85) / 0.15)))
        pool_color = (DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], pool_alpha)
        draw.ellipse([s["cx"] - pool_w, pool_top - pool_depth//2,
                      s["cx"] + pool_w, pool_top + pool_depth//2], fill=pool_color)
        # highlight + rim for pool
        hl_color = (min(255, DRIP_COLOR[0]+30), min(255, DRIP_COLOR[1]+20), min(255, DRIP_COLOR[2]+20),
                    int(pool_alpha*0.45))
        draw.ellipse([s["cx"] - pool_w//2, pool_top - pool_depth//2 - 2,
                      s["cx"] - pool_w//2 + pool_w//3, pool_top + pool_depth//4], fill=hl_color)
        rim_color = (20, 8, 10, 100)
        draw.ellipse([s["cx"] - pool_w - 2, pool_top - pool_depth - 2,
                      s["cx"] + pool_w + 2, pool_top + pool_depth + 2], outline=rim_color)

        # draw a viscous neck as a stack of ellipses from pool edge down to head_y
        segs = s["segments"]
        if segs < 3:
            segs = 3
        # start point slightly below pool center
        start_y = pool_top + pool_depth//2
        for seg in range(segs):
            t = (seg + 1) / float(segs)            # 0..1 along the neck
            # position along the neck from pool start to (start_y + neck_len)
            ny = start_y + int(t * neck_len)
            # taper width: thicker near pool, thinner near head
            seg_w = max(1, int(s["w"] * (1.0 - (t*0.9)) * (1.0 + (1.0 - eprog)*0.25)))
            # alpha taper (head more opaque)
            seg_alpha = int(220 * (0.6 + 0.4 * (1.0 - t)) * (1.0 if eprog < 0.95 else max(0.15, 1.0 - (eprog-0.95)/0.05)))
            seg_color = (DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], seg_alpha)
            draw.ellipse([s["cx"] - seg_w, ny - seg_w, s["cx"] + seg_w, ny + seg_w*2], fill=seg_color)

        # draw the main drop head with motion-smear ghosts (smoother)
        head_alpha = int(255 * (1.0 if eprog < 0.95 else max(0.0, 1.0 - (eprog-0.95)/0.05)))
        head_color = (DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], head_alpha)
        # smear: draw 2 faded ellipses behind head
        for ghost in range(2):
            gmul = 1.0 - ghost * 0.45
            gy = head_y - ghost * int(6 * (1.0 - eprog*0.6))
            gw = max(1, int(s["w"] * (1.0 + ghost * 0.4)))
            ga = int(head_alpha * (0.5 * gmul))
            draw.ellipse([s["cx"] - gw, gy - 4, s["cx"] + gw, gy + 8], fill=(DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], ga))
        # head
        draw.ellipse([s["cx"] - s["w"], head_y - 4, s["cx"] + s["w"], head_y + 8], fill=head_color)

        # long thin tail behind head (subtle)
        tail_top = head_y + 8
        tail_bottom = head_y + int(s["length"] * (0.4 + 0.6 * eprog))
        if tail_bottom > tail_top:
            draw.rectangle([s["cx"] - max(1, s["w"]//3), tail_top, s["cx"] + max(1, s["w"]//3), tail_bottom], fill=(DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], int(200 * (1.0 - eprog*0.6))))

        # detached droplets: spawn periodically based on drop_period
        dp = s["drop_period"]
        # number of small droplets spawned so far in this cycle
        cycle_pos = (frame_idx + s["phase"]) % dp
        # spawn a small droplet that moves faster than the main head
        # droplet progress in [0,1)
        dprog = cycle_pos / float(dp)
        # only draw if droplet has left the pool area a bit (avoid overlap)
        if dprog > 0.05:
            # droplet falls further than neck but with its own easing (faster)
            droplet_y = start_y + int(_ease_out_cubic(dprog) * (s["fall"] * 1.05))
            droplet_w = max(1, int(s["w"] * 0.6))
            droplet_alpha = int(200 * (1.0 - dprog))
            draw.ellipse([s["cx"] - droplet_w, droplet_y - droplet_w, s["cx"] + droplet_w, droplet_y + droplet_w], fill=(DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], droplet_alpha))

        # occasional tiny secondary droplets trailing the head for realism
        if eprog > 0.3:
            for j in range(1, 3):
                trail_t = (eprog + j*0.06) % 1.0
                tj = _ease_out_cubic(trail_t)
                ty = start_y + int(tj * s["fall"] * 0.9)
                tw = max(1, int(s["w"] * (0.35 - j*0.08)))
                ta = int(160 * (1.0 - j*0.3))
                draw.ellipse([s["cx"] - tw, ty - tw, s["cx"] + tw, ty + tw], fill=(DRIP_COLOR[0], DRIP_COLOR[1], DRIP_COLOR[2], ta))

    # gentle blur and slight sharpen combo to keep text crisp later
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(radius=0.75))

    # composite text on top so blood pools touch bottoms only
    composed = Image.alpha_composite(backdrop, base_text_im)
    return composed

def generate_animation(text, frames):
    # Bigger logo: 3x scale (was 220 -> now 660)
    base_text, per, font = build_base(text, font_size=1660)
    specs = make_drip_specs(per, frames)
    for i in range(frames):
        frame = render_frame(base_text, specs, i, frames)
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