import asyncio
import os
import edge_tts
from pathlib import Path
from config import TEMP_DIR, DEFAULT_VOICE

async def generate_tts_async(text, output_audio_path, voice=DEFAULT_VOICE):
    """
    Generates neural audio file using edge-tts.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_audio_path))
    return str(output_audio_path)

def generate_voiceover(text, output_audio_path, voice=DEFAULT_VOICE):
    """
    Stage 7: Voice Generator
    Synchronous wrapper for generating high-quality neural voiceover audio files.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If already inside an active loop
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(generate_tts_async(text, output_audio_path, voice))
        else:
            return asyncio.run(generate_tts_async(text, output_audio_path, voice))
    except Exception as e:
        print(f"[VoiceGenerator] edge-tts error, attempting new loop: {e}")
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        return new_loop.run_until_complete(generate_tts_async(text, output_audio_path, voice))

def generate_all_scene_voices(scenes, full_script):
    """
    Synthesizes audio for all 6 individual scenes and the master full audio track.
    Returns list of scene audio paths and master audio path.
    """
    scene_audio_paths = []
    
    # 1. Master audio track
    master_audio_path = TEMP_DIR / "master_voiceover.mp3"
    print("[VoiceGenerator] Generating master full voiceover audio...")
    generate_voiceover(full_script.get("full_script", "Breaking news announcement."), master_audio_path)

    # 2. Scene-by-scene audio tracks
    for scene in scenes:
        s_num = scene["scene_number"]
        scene_audio = TEMP_DIR / f"scene_audio_{s_num}.mp3"
        print(f"[VoiceGenerator] Generating Scene {s_num} voiceover...")
        generate_voiceover(scene.get("narration", f"Scene {s_num}"), scene_audio)
        scene_audio_paths.append(str(scene_audio))

    return {
        "master_audio": str(master_audio_path),
        "scene_audios": scene_audio_paths
    }

if __name__ == "__main__":
    out_file = TEMP_DIR / "test_voice.mp3"
    generate_voiceover("Hello! Welcome to the automated news video pipeline test.", out_file)
    print("Generated voice file:", out_file, "Size:", os.path.getsize(out_file))
