import os
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from config import FFMPEG_EXE, VIDEO_WIDTH, VIDEO_HEIGHT

def generate_thumbnail(video_path, title_text, output_thumbnail_path):
    """
    Stage 10: Thumbnail Generator
    Extracts a frame from the video, applies high-CTR graphics, gradient overlays, and typography.
    """
    print("[ThumbnailGenerator] Generating thumbnail image...")
    
    extracted_frame = str(output_thumbnail_path).replace(".jpg", "_raw.png")

    # Step 1: Extract frame at 2.0 seconds mark
    cmd = [
        FFMPEG_EXE, "-y",
        "-ss", "00:00:02.000",
        "-i", str(video_path),
        "-vframes", "1",
        extracted_frame
    ]
    
    try:
        subprocess.run(cmd, check=True)
        img = Image.open(extracted_frame).convert("RGB")
    except Exception as e:
        print(f"[ThumbnailGenerator] Frame extract fallback: {e}")
        img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), (15, 23, 42))

    # Step 2: Overlay Dark Gradient Vignette for text contrast
    overlay = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    # Top & Bottom Gradient shadows
    for y in range(0, 500):
        alpha = int(220 * (1.0 - y / 500.0))
        draw_overlay.line([(0, y), (VIDEO_WIDTH, y)], fill=(0, 0, 0, alpha))
    for y in range(VIDEO_HEIGHT - 600, VIDEO_HEIGHT):
        alpha = int(240 * ((y - (VIDEO_HEIGHT - 600)) / 600.0))
        draw_overlay.line([(0, y), (VIDEO_WIDTH, y)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Load Fonts
    try:
        font_badge = ImageFont.truetype("arial.ttf", 40)
        font_title = ImageFont.truetype("arial.ttf", 72)
    except Exception:
        font_badge = font_title = ImageFont.load_default()

    # Draw "BREAKING NEWS" badge pill
    badge_x1, badge_y1, badge_x2, badge_y2 = 100, 250, 600, 330
    draw.rounded_rectangle([badge_x1, badge_y1, badge_x2, badge_y2], radius=20, fill=(239, 68, 68))
    draw.text(((badge_x1 + badge_x2) // 2, (badge_y1 + badge_y2) // 2), "🔥 BREAKING NEWS", font=font_badge, fill=(255, 255, 255), anchor="mm")

    # Draw Title Typography
    clean_title = title_text.upper()
    words = clean_title.split()
    lines = []
    current_line = []
    for w in words:
        current_line.append(w)
        if len(" ".join(current_line)) > 15:
            lines.append(" ".join(current_line[:-1]))
            current_line = [w]
    if current_line:
        lines.append(" ".join(current_line))

    start_y = 400
    for idx, line in enumerate(lines[:3]):
        # Text shadow
        draw.text((104, start_y + idx * 85 + 4), line, font=font_title, fill=(0, 0, 0))
        # Text main yellow/white fill
        fill_color = (255, 234, 0) if idx == 0 else (255, 255, 255)
        draw.text((100, start_y + idx * 85), line, font=font_title, fill=fill_color)

    # Save finalized thumbnail
    img.save(output_thumbnail_path, "JPEG", quality=95)
    
    # Cleanup raw frame temp file
    if os.path.exists(extracted_frame):
        os.remove(extracted_frame)

    print(f"[ThumbnailGenerator] Thumbnail saved at: {output_thumbnail_path}")
    return str(output_thumbnail_path)

if __name__ == "__main__":
    print("Thumbnail generator module loaded.")
