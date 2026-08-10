import json
import requests
from config import GEMINI_API_KEY

def generate_prompts(scenes, topic_context="Breaking News"):
    """
    Stage 4: Prompt Generator
    Converts scene shot descriptions into 3D cinematic AI video prompts for Google Flow / Veo / Replicate,
    enforcing 100% character consistency across all 6 scenes.
    """
    enhanced_scenes = []

    character_spec = (
        "Main Character: Handsome 22-year-old Indian boy, athletic build, stylish modern hair, sharp jawline, expressive eyes, "
        "wearing premium black hoodie, black cargo pants, modern sneakers."
    )
    
    character_lock = (
        "Character Lock: Use the exact same 22-year-old Indian boy in every scene. "
        "Preserve face, hairstyle, eyes, skin tone, body proportions, clothing, age, and identity with 100% consistency."
    )

    style_spec = (
        "Style: Hyper-realistic 3D graphics, Unreal Engine 5 render, cinematic realism, Hollywood production quality, "
        "volumetric blue and orange lighting, ray tracing, global illumination, ultra-detailed textures, realistic facial expressions, smooth character motion."
    )

    negative_prompt = (
        "Negative Prompt: blurry, low quality, distorted face, extra fingers, cartoon, anime, low resolution, bad lighting, flickering, "
        "duplicated character, unrealistic movement, deformed body, watermark, text overlay."
    )

    for scene in scenes:
        scene_num = scene["scene_number"]
        narration = scene["narration"]
        shot_desc = scene["shot_description"]

        prompt_text = (
            f"{character_lock} | {character_spec} | Environment: Futuristic cyberpunk city at night with neon lights, digital billboards, holographic screens, reflective rain-soaked roads. "
            f"Action: {shot_desc}. Looking directly into cinema camera, talking confidently like a professional influencer. | "
            f"{style_spec} | {negative_prompt}"
        )

        # Optional Gemini API prompt refinement if key available
        if GEMINI_API_KEY:
            try:
                gen_prompt = (
                    f"Create a 1-sentence cinematic 3D Unreal Engine 5 text-to-video AI prompt for Scene {scene_num}:\n"
                    f"Character: 22-year-old Indian boy in black hoodie and cargo pants.\n"
                    f"Shot Action: {shot_desc}\n"
                    f"Context: {narration}\n"
                    f"Include character lock consistency instruction, cyberpunk neon lighting, volumetric fog, and 9:16 vertical cinema camera angle."
                )
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json={"contents": [{"parts": [{"text": gen_prompt}]}]}, timeout=10)
                if resp.status_code == 200:
                    out = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                    if out:
                        prompt_text = f"{character_lock} | {out} | {negative_prompt}"
            except Exception as e:
                print(f"[PromptGenerator] Gemini prompt enhancement fallback for scene {scene_num}: {e}")

        enhanced_scene = dict(scene)
        enhanced_scene["video_prompt"] = prompt_text
        enhanced_scenes.append(enhanced_scene)

    return enhanced_scenes

if __name__ == "__main__":
    test_scenes = [{"scene_number": 1, "duration": 10.0, "narration": "Breaking AI announcement.", "shot_description": "Futuristic glowing core"}]
    res = generate_prompts(test_scenes)
    print(json.dumps(res, indent=2))
