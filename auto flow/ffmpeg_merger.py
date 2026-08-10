import os
import subprocess
from pathlib import Path
from config import TEMP_DIR, FFMPEG_EXE, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, ASSETS_DIR

def create_dummy_bgm_if_missing(bgm_path):
    """
    Generates a soft, subtle background music tone track using FFmpeg if no audio asset exists.
    """
    if not os.path.exists(bgm_path):
        cmd = [
            FFMPEG_EXE, "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=110:sample_rate=44100",
            "-t", "60",
            "-af", "volume=0.08",
            str(bgm_path)
        ]
        os.system(" ".join(f'"{c}"' if " " in c else c for c in cmd))

def merge_clips_and_audio(clip_paths, voiceover_audio_path, output_video_path):
    """
    Stage 8: FFmpeg Merge
    Concatenates the 6 video scene clips, combines with voiceover, and adds background music.
    """
    print("[FFmpegMerger] Concatenating video clips and mixing audio tracks...")

    # Create file manifest list for FFmpeg concat filter
    concat_list_path = TEMP_DIR / "concat_clips.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for clip in clip_paths:
            # Escape single quotes and backslashes for FFmpeg list
            clean_clip_path = str(Path(clip).resolve()).replace("\\", "/")
            f.write(f"file '{clean_clip_path}'\n")

    merged_raw_video = TEMP_DIR / "raw_concat_video.mp4"

    # Step 1: Concatenate clips
    cmd_concat = [
        FFMPEG_EXE, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(VIDEO_FPS),
        str(merged_raw_video)
    ]
    subprocess.run(cmd_concat, check=True)

    # Background music asset
    bgm_path = ASSETS_DIR / "background_music.mp3"
    create_dummy_bgm_if_missing(bgm_path)

    # Step 2: Combine video + voiceover audio + background music with ducking
    cmd_mix = [
        FFMPEG_EXE, "-y",
        "-i", str(merged_raw_video),
        "-i", str(voiceover_audio_path),
        "-i", str(bgm_path),
        "-filter_complex",
        "[1:a]volume=1.4[voice];[2:a]volume=0.12[bgm];[voice][bgm]amix=inputs=2:duration=first[audio]",
        "-map", "0:v:0",
        "-map", "[audio]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_video_path)
    ]
    subprocess.run(cmd_mix, check=True)

    print(f"[FFmpegMerger] Merged video successfully created at: {output_video_path}")
    return str(output_video_path)

if __name__ == "__main__":
    print("FFmpeg merger module loaded.")
