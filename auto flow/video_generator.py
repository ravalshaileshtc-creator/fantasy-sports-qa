import os
import urllib.parse
import subprocess
import time
import math
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from config import TEMP_DIR, FFMPEG_EXE, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, GOOGLE_FLOW_API_KEY, REPLICATE_API_TOKEN

def fetch_ai_scene_image(scene, output_img_path):
    """
    Fetches ultra-realistic 3D Unreal Engine 5 AI image using Flux model matching the 22-year-old Indian creator design spec.
    """
    shot_desc = scene.get("shot_description", "futuristic tech highlight")
    scene_num = scene.get("scene_number", 1)

    # 6 Scene Action Breakdowns matching the Master Prompt Blueprint
    scene_actions = [
        "handsome 22 year old indian boy walking towards camera in futuristic cyberpunk city, looking directly at camera, energetic confident smile",
        "handsome 22 year old indian boy pointing at glowing blue holographic screen animations behind him in futuristic city at night",
        "handsome 22 year old indian boy standing beside luxury sports car in glowing cyberpunk city street with neon reflections",
        "handsome 22 year old indian boy explaining with hand gestures, surrounded by high tech futuristic 3D holograms",
        "handsome 22 year old indian boy giving closing tip with confident expression in futuristic neon studio environment",
        "handsome 22 year old indian boy asking viewers to subscribe, energetic powerful stance, sharp jawline, black hoodie"
    ]
    action_text = scene_actions[(scene_num - 1) % len(scene_actions)]

    # Ultra-Realistic 3D Master Prompt
    prompt = (
        f"create an ultra-realistic 3D cinematic influencer photo. "
        f"Main Character: handsome 22-year-old Indian boy, athletic body, stylish modern haircut, sharp jawline, expressive eyes, natural skin texture, wearing premium black hoodie, black cargo pants. "
        f"Action: {action_text}. "
        f"Style: Hyper-realistic 3D graphics, Unreal Engine 5 quality, cinematic realism, Hollywood production quality, volumetric blue and orange lighting, ray tracing, global illumination, ultra detailed textures. "
        f"Environment: Futuristic city at night, neon lights, digital billboards, cyberpunk atmosphere, cinematic fog, reflective roads after rain. "
        f"Camera: 9:16 vertical cinema camera, shallow depth of field, 8K UHD render."
    )
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&width=1080&height=1920&nologo=true&seed=42069"

    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200 and len(resp.content) > 5000:
            with open(output_img_path, "wb") as f:
                f.write(resp.content)
            print(f"[VideoGenerator] Flux 3D AI image generated for Scene {scene_num} ({len(resp.content)} bytes)")
            return True
    except Exception as e:
        print(f"[VideoGenerator] AI image fetch error for scene {scene_num}: {e}")

    return False

def render_cinematic_ai_clip(image_path, output_clip_path, duration=10.0):
    """
    Converts a photorealistic AI image into a 10-second 60fps cinematic video clip using FFmpeg zoompan.
    """
    width = VIDEO_WIDTH
    height = VIDEO_HEIGHT
    fps = VIDEO_FPS
    total_frames = int(duration * fps)

    clean_img_path = str(Path(image_path).resolve()).replace("\\", "/")

    # FFmpeg dynamic zoom-in filter (Ken Burns camera movement)
    zoom_filter = (
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"zoompan=z='min(zoom+0.0012,1.20)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s={width}x{height}:fps={fps}"
    )

    cmd = [
        FFMPEG_EXE, "-y",
        "-loop", "1",
        "-i", clean_img_path,
        "-vf", zoom_filter,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        "-r", str(fps),
        str(output_clip_path)
    ]
    
    subprocess.run(cmd, check=True)
    return str(output_clip_path)

def generate_procedural_scene_clip(scene, output_clip_path, duration=10.0):
    """
    Fallback canvas renderer.
    """
    width = VIDEO_WIDTH
    height = VIDEO_HEIGHT
    fps = VIDEO_FPS
    total_frames = int(duration * fps)

    frames_dir = TEMP_DIR / f"frames_scene_{scene['scene_number']}"
    if frames_dir.exists():
        import shutil
        try:
            shutil.rmtree(frames_dir)
        except Exception:
            pass
    frames_dir.mkdir(parents=True, exist_ok=True)

    narration_text = scene.get("narration", f"Scene {scene['scene_number']}")
    shot_desc = scene.get("shot_description", "News highlight")
    scene_num = scene.get("scene_number", 1)

    color_schemes = [
        ((15, 23, 42), (99, 102, 241), (168, 85, 247)),
        ((10, 25, 47), (14, 165, 233), (56, 189, 248)),
        ((24, 9, 39), (236, 72, 153), (244, 114, 182)),
        ((17, 24, 39), (34, 197, 94), (74, 222, 128)),
        ((30, 15, 10), (249, 115, 22), (251, 146, 60)),
        ((15, 23, 42), (234, 179, 8), (250, 204, 21))
    ]
    bg_dark, accent1, accent2 = color_schemes[(scene_num - 1) % len(color_schemes)]

    try:
        font_large = ImageFont.truetype("arial.ttf", 64)
        font_mid = ImageFont.truetype("arial.ttf", 44)
        font_small = ImageFont.truetype("arial.ttf", 32)
    except Exception:
        font_large = font_mid = font_small = ImageFont.load_default()

    frame_count = 0
    for frame_i in range(0, total_frames, 2):
        t = frame_i / float(total_frames)

        img = Image.new("RGB", (width, height), bg_dark)
        draw = ImageDraw.Draw(img)

        glow_radius = int(300 + 80 * math.sin(t * math.pi * 2))
        cx = int(width / 2 + 100 * math.cos(t * math.pi))
        cy = int(height / 3 + 100 * math.sin(t * math.pi))
        draw.ellipse([cx - glow_radius, cy - glow_radius, cx + glow_radius, cy + glow_radius], fill=accent1)
        img = img.filter(ImageFilter.GaussianBlur(radius=70))
        draw = ImageDraw.Draw(img)

        badge_text = f"NEWS SHORT • SCENE 0{scene_num} / 06"
        draw.rounded_rectangle([80, 120, width - 80, 200], radius=40, fill=(0, 0, 0, 180), outline=accent1, width=3)
        draw.text((width // 2, 160), badge_text, font=font_small, fill=(255, 255, 255), anchor="mm")

        card_zoom = 1.0 + 0.05 * math.sin(t * math.pi)
        card_w = int(880 * card_zoom)
        card_h = int(720 * card_zoom)
        card_x = (width - card_w) // 2
        card_y = (height - card_h) // 2 - 40

        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=30, fill=(15, 23, 42), outline=accent2, width=4)
        
        char_cx = width // 2
        char_cy = card_y + 200
        draw.ellipse([char_cx - 90, char_cy - 90, char_cx + 90, char_cy + 90], fill=(30, 41, 59), outline=accent1, width=4)
        draw.text((char_cx, char_cy), "👦🏻", font=font_large, anchor="mm")
        draw.text((width // 2, card_y + 320), "22Y INDIAN CREATOR • BLACK HOODIE", font=font_small, fill=accent1, anchor="mm")

        words = shot_desc.upper().split()
        line1 = " ".join(words[:len(words)//2 + 1])
        line2 = " ".join(words[len(words)//2 + 1:])
        draw.text((width // 2, card_y + 400), line1, font=font_mid, fill=accent2, anchor="mm")
        if line2:
            draw.text((width // 2, card_y + 460), line2, font=font_mid, fill=(255, 255, 255), anchor="mm")

        frame_file = frames_dir / f"frame_{frame_count:04d}.png"
        img.save(frame_file)
        frame_count += 1

    pattern_path = str((frames_dir / "frame_%04d.png").resolve()).replace("\\", "/")
    cmd = [
        FFMPEG_EXE, "-y",
        "-framerate", str(fps // 2),
        "-i", pattern_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={width}:{height},fps={fps}",
        str(output_clip_path)
    ]
    subprocess.run(cmd, check=True)
    return str(output_clip_path)

def generate_video_clips(enhanced_scenes):
    """
    Stage 5 & 6: Photorealistic 3D AI Video Clips Engine (1080x1920 9:16 Vertical)
    Synthesizes 6 ultra-realistic 3D AI scene video clips.
    """
    clip_paths = []
    
    for scene in enhanced_scenes:
        scene_num = scene["scene_number"]
        out_clip = TEMP_DIR / f"scene_clip_{scene_num}.mp4"
        ai_img_file = TEMP_DIR / f"ai_scene_{scene_num}.jpg"

        print(f"[VideoGenerator] Processing Photorealistic 3D Scene {scene_num}/6 Clip...")

        if os.path.exists(out_clip):
            try:
                os.remove(out_clip)
            except Exception:
                pass

        # Step 1: Fetch photorealistic 3D AI image for scene
        got_ai_img = fetch_ai_scene_image(scene, ai_img_file)

        # Step 2: Render 10s cinematic video clip with camera motion
        if got_ai_img:
            try:
                clip_file = render_cinematic_ai_clip(ai_img_file, out_clip, duration=scene.get("duration", 10.0))
                clip_paths.append(clip_file)
                continue
            except Exception as e:
                print(f"[VideoGenerator] FFmpeg zoompan render error: {e}")

        # Fallback to dynamic procedural canvas clip
        clip_file = generate_procedural_scene_clip(scene, out_clip, duration=scene.get("duration", 10.0))
        clip_paths.append(clip_file)

    return clip_paths

if __name__ == "__main__":
    test_scenes = [{
        "scene_number": 1,
        "duration": 5.0,
        "narration": "First scene narration test",
        "shot_description": "Futuristic Glowing AI Brain Core",
        "video_prompt": "Cinematic visual prompt test"
    }]
    clips = generate_video_clips(test_scenes)
    print("Generated clips:", clips)
