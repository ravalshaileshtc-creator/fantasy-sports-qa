import json
import re

def split_into_scenes(script_data, num_scenes=6):
    """
    Stage 3: Scene Splitter
    Splits the full script into exactly 6 timed scenes with visual descriptions.
    """
    full_script = script_data.get("full_script", "")
    
    # Clean and split full script into sentences
    sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', full_script) if s.strip()]
    if not sentences:
        sentences = [full_script]

    # Distribute sentences across num_scenes (6 scenes)
    scenes = []
    chunk_size = max(1, len(sentences) // num_scenes)

    shot_concepts = [
        "Dynamic viral news headline with energetic glowing particle backgrounds",
        "High-tech futuristic visual representation of key story concept",
        "Data metrics visualization and expanding digital network nodes",
        "Cinematic portrait of industry leaders and expert insights",
        "Dramatic world map digital overlay highlighting global impact",
        "Call to action ending screen with subscribe button and comment prompt"
    ]

    for i in range(num_scenes):
        start_idx = i * chunk_size
        if i == num_scenes - 1:
            scene_sentences = sentences[start_idx:]
        else:
            scene_sentences = sentences[start_idx : start_idx + chunk_size]

        if not scene_sentences and scenes:
            scene_sentences = [scenes[-1]["narration"]]

        narration_text = " ".join(scene_sentences) if scene_sentences else f"Scene {i+1} covering {script_data.get('title', 'breaking news')}."
        
        scenes.append({
            "scene_number": i + 1,
            "duration": 10.0,  # 10s per clip x 6 = 60s total
            "narration": narration_text,
            "shot_description": shot_concepts[i % len(shot_concepts)]
        })

    return scenes

if __name__ == "__main__":
    test_script = {"title": "Tech News", "full_script": "Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5. Sentence 6. Sentence 7. Sentence 8."}
    scenes = split_into_scenes(test_script)
    print(f"Generated {len(scenes)} scenes:")
    print(json.dumps(scenes, indent=2))
