import os
import re
import subprocess
from pathlib import Path
from config import TEMP_DIR, FFMPEG_EXE

def format_timestamp_srt(seconds):
    """Formats float seconds into SRT timestamp HH:MM:SS,mmm"""
    millis = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_timestamp_ass(seconds):
    """Formats float seconds into ASS timestamp H:MM:SS.cs"""
    cs = int((seconds - int(seconds)) * 100)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"

def create_subtitles_file(scenes, srt_path, ass_path):
    """
    Generates timed SRT and styled ASS subtitle files.
    """
    srt_lines = []
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,52,&H0000FFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,80,80,480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_events = []
    current_time = 0.0
    sub_index = 1

    for scene in scenes:
        narration = scene.get("narration", "")
        duration = scene.get("duration", 10.0)
        words = [w.strip() for w in narration.split() if w.strip()]

        if not words:
            current_time += duration
            continue

        # Group into 4-6 word caption chunks for short-form video readability
        words_per_chunk = 5
        chunk_duration = duration / max(1, (len(words) / words_per_chunk))

        for i in range(0, len(words), words_per_chunk):
            chunk_words = words[i:i + words_per_chunk]
            chunk_text = " ".join(chunk_words)

            start_t = current_time + (i / len(words)) * duration
            end_t = min(current_time + ((i + words_per_chunk) / len(words)) * duration, current_time + duration)

            # SRT entry
            srt_lines.append(f"{sub_index}")
            srt_lines.append(f"{format_timestamp_srt(start_t)} --> {format_timestamp_srt(end_t)}")
            srt_lines.append(chunk_text)
            srt_lines.append("")

            # ASS entry (with bold uppercase short format styling)
            styled_text = chunk_text.upper()
            ass_events.append(
                f"Dialogue: 0,{format_timestamp_ass(start_t)},{format_timestamp_ass(end_t)},Default,,0,0,0,,{styled_text}"
            )
            sub_index += 1

        current_time += duration

    # Write SRT
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    # Write ASS
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(ass_events))

    return srt_path, ass_path

def burn_subtitles(input_video_path, scenes, output_video_path):
    """
    Stage 9: Subtitles
    Generates subtitle files and burns high-visibility vertical short subtitles onto the video.
    """
    print("[SubtitleEngine] Generating dynamic subtitles and burning onto video...")
    srt_path = TEMP_DIR / "subtitles.srt"
    ass_path = TEMP_DIR / "subtitles.ass"

    create_subtitles_file(scenes, srt_path, ass_path)

    # Escape path for FFmpeg subtitles filter
    clean_ass = str(ass_path.resolve()).replace("\\", "/").replace(":", "\\:")

    cmd = [
        FFMPEG_EXE, "-y",
        "-i", str(input_video_path),
        "-vf", f"ass='{clean_ass}'",
        "-c:v", "libx264",
        "-c:a", "copy",
        str(output_video_path)
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"[SubtitleEngine] ASS filter failed, attempting SRT burn fallback: {e}")
        clean_srt = str(srt_path.resolve()).replace("\\", "/").replace(":", "\\:")
        cmd_fallback = [
            FFMPEG_EXE, "-y",
            "-i", str(input_video_path),
            "-vf", f"subtitles='{clean_srt}'",
            "-c:v", "libx264",
            "-c:a", "copy",
            str(output_video_path)
        ]
        subprocess.run(cmd_fallback, check=True)

    print(f"[SubtitleEngine] Subtitled video created at: {output_video_path}")
    return str(output_video_path)

if __name__ == "__main__":
    print("Subtitle engine loaded.")
