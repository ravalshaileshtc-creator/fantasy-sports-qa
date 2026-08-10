import argparse
import json
import sys
import time
from pathlib import Path
from config import OUTPUT_DIR, TEMP_DIR
from news_scraper import fetch_trending_news
from script_writer import generate_script
from scene_splitter import split_into_scenes
from prompt_generator import generate_prompts
from video_generator import generate_video_clips
from voice_generator import generate_all_scene_voices
from ffmpeg_merger import merge_clips_and_audio
from subtitle_engine import burn_subtitles
from thumbnail_generator import generate_thumbnail

def run_pipeline(topic=None, progress_callback=None):
    """
    Stage 11: End-to-End Orchestrator (11 Stages)
    Executes the entire automated news-to-video workflow.
    """
    start_time = time.time()

    def update_status(stage_num, stage_name, details=""):
        msg = f"[Stage {stage_num:02d}/11] {stage_name}: {details}"
        print(msg, flush=True)
        sys.stdout.flush()
        if progress_callback:
            progress_callback(stage_num, stage_name, details)

    # Stage 01: News Scraper
    update_status(1, "News Scraper", f"Fetching trending news for '{topic or 'Headlines'}'...")
    news_items = fetch_trending_news(topic=topic, limit=1)
    article = news_items[0]

    # Stage 02: Gemini Script Writer
    update_status(2, "Gemini Script Writer", "Writing viral 60s video script with Gemini...")
    script_data = generate_script(article, custom_topic=topic)

    # Stage 03: Scene Splitter
    update_status(3, "Scene Splitter", "Splitting narration script into 6 scenes...")
    raw_scenes = split_into_scenes(script_data, num_scenes=6)

    # Stage 04: Prompt Generator
    update_status(4, "Prompt Generator", "Generating visual AI video prompts for scenes...")
    enhanced_scenes = generate_prompts(raw_scenes, topic_context=article["title"])

    # Stage 05 & 06: Google Flow API & 6 Video Clips
    update_status(5, "Google Flow API", "Synthesizing AI video scene footage...")
    update_status(6, "6 Video Clips", "Processing and rendering 6 clip segments...")
    clip_paths = generate_video_clips(enhanced_scenes)

    # Stage 07: Voice Generator
    update_status(7, "Voice Generator", "Generating neural voiceover audio files...")
    voice_results = generate_all_scene_voices(enhanced_scenes, script_data)

    # Stage 08: FFmpeg Merge
    update_status(8, "FFmpeg Merge", "Merging 6 video clips with voiceover & audio ducking...")
    merged_raw_video = TEMP_DIR / "merged_raw.mp4"
    merge_clips_and_audio(clip_paths, voice_results["master_audio"], merged_raw_video)

    # Stage 09: Subtitles
    update_status(9, "Subtitles", "Generating and burning dynamic short captions...")
    final_video_path = OUTPUT_DIR / "final_1min_video.mp4"
    burn_subtitles(merged_raw_video, enhanced_scenes, final_video_path)

    # Stage 10: Thumbnail
    update_status(10, "Thumbnail", "Creating high-CTR thumbnail graphic...")
    thumbnail_path = OUTPUT_DIR / "thumbnail.jpg"
    generate_thumbnail(final_video_path, script_data["title"], thumbnail_path)

    # Stage 11: Ready 1 Minute Video
    total_elapsed = round(time.time() - start_time, 2)
    manifest = {
        "status": "COMPLETED",
        "elapsed_seconds": total_elapsed,
        "article": article,
        "script": script_data,
        "scenes": enhanced_scenes,
        "clips": clip_paths,
        "master_audio": voice_results["master_audio"],
        "video_output": str(final_video_path),
        "thumbnail_output": str(thumbnail_path)
    }

    manifest_path = OUTPUT_DIR / "video_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    update_status(11, "Ready 1 Minute Video", f"Pipeline completed in {total_elapsed}s! Output: {final_video_path}")
    return manifest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated News-to-Video Generator")
    parser.add_argument("--topic", type=str, default="Artificial Intelligence", help="News topic to search and generate video for")
    args = parser.parse_args()

    result = run_pipeline(topic=args.topic)
    print("\n--- FINAL PIPELINE MANIFEST ---")
    print(json.dumps(result, indent=2))
