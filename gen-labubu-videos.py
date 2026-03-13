#!/usr/bin/env python3
"""Generate high-quality Labubu pet Veo videos for Nuoqi demo V14."""

import requests
import time
import json
import sys
import base64
import os

API_KEY = "AIzaSyAJw9iWFNVddfEflZ8lAoP5ibr-pWafHVA"
MODEL = "veo-2.0-generate-001"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}"

# Each pet has a carefully crafted prompt for a small circular badge video
PETS = {
    "lawrence": {
        "prompt": (
            "A cute golden lion Labubu vinyl toy figure with a tiny crown and gavel, "
            "standing on a polished dark desk surface. The figure gently sways and tilts its head side to side "
            "with a subtle bouncing motion. Warm golden ambient lighting creates soft reflections on the metallic finish. "
            "The background is a dark elegant office with bokeh lights. Cinematic shallow depth of field. "
            "Smooth looping animation. High-end product photography style. 4K quality."
        ),
        "output": "nuoqi/pet-lawrence-labubu-veo.mp4"
    },
    "luke": {
        "prompt": (
            "A cute baby blue owl Labubu vinyl toy figure wearing tiny black headphones, "
            "sitting in a relaxed pose on a dark surface. The figure gently bobs its head to music "
            "with a subtle rhythmic swaying motion. Cool blue ambient lighting with soft glowing accents. "
            "Dark minimalist background with subtle blue bokeh. Cinematic shallow depth of field. "
            "Smooth looping animation. High-end collectible toy photography. 4K quality."
        ),
        "output": "nuoqi/pet-luke-labubu-veo.mp4"
    },
    "lawra": {
        "prompt": (
            "A small pink fox-shaped designer vinyl collectible toy with a fluffy tail and pearl beads around its neck, "
            "placed on a dark reflective surface. The toy slowly rotates on a display turntable, "
            "reflecting warm rose-gold ambient light. Dark luxurious background with subtle sparkle bokeh dots. "
            "Cinematic shallow depth of field. Product photography turntable rotation. "
            "Smooth looping animation. No humans. 4K quality."
        ),
        "output": "nuoqi/pet-lawra-labubu-veo.mp4"
    },
    "lancelot": {
        "prompt": (
            "A cute lavender purple dragon Labubu vinyl toy figure with tiny wings and horns, "
            "sitting and holding a small glowing book. The figure gently reads, looking down at the book "
            "which emits a soft warm golden glow. Magical purple and starlight ambient lighting. "
            "Galaxy sparkle patterns shimmer across the figure's surface. Dark mystical background with star bokeh. "
            "Cinematic shallow depth of field. Smooth looping animation. Fantasy collectible toy photography. 4K quality."
        ),
        "output": "nuoqi/pet-lancelot-labubu-veo.mp4"
    }
}


def generate_video(name, config):
    print(f"\n{'='*60}")
    print(f"Generating video for: {name}")
    print(f"Prompt: {config['prompt'][:80]}...")
    
    url = f"{BASE_URL}:predictLongRunning?key={API_KEY}"
    payload = {
        "instances": [{
            "prompt": config["prompt"]
        }],
        "parameters": {
            "sampleCount": 1,
            "durationSeconds": 5,
            "aspectRatio": "9:16",
            "personGeneration": "dont_allow"
        }
    }
    
    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code != 200:
        print(f"ERROR: {resp.status_code} - {resp.text[:500]}")
        return False
    
    result = resp.json()
    op_name = result.get("name")
    if not op_name:
        print(f"ERROR: No operation name. Response: {json.dumps(result)[:300]}")
        return False
    
    print(f"Operation: {op_name}")
    print("Polling for completion...")
    
    for i in range(60):
        time.sleep(10)
        poll_url = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={API_KEY}"
        poll_resp = requests.get(poll_url, timeout=30)
        poll_data = poll_resp.json()
        
        done = poll_data.get("done", False)
        print(f"  Poll {i+1}: done={done}")
        
        if done:
            if "error" in poll_data:
                print(f"ERROR: {poll_data['error']}")
                return False
            
            response = poll_data.get("response", {})
            videos = response.get("generateVideoResponse", {}).get("generatedSamples", [])
            if not videos:
                print(f"ERROR: No videos in response. Keys: {list(response.keys())}")
                print(f"Full response: {json.dumps(response)[:500]}")
                return False
            
            video_data = videos[0].get("video", {}).get("bytesBase64Encoded")
            if not video_data:
                # Try URI
                video_uri = videos[0].get("video", {}).get("uri")
                if video_uri:
                    print(f"Downloading from URI: {video_uri[:80]}...")
                    sep = "&" if "?" in video_uri else "?"
                    dl = requests.get(f"{video_uri}{sep}key={API_KEY}", timeout=120)
                    with open(f"/tmp/nuoqi-v8/{config['output']}", "wb") as f:
                        f.write(dl.content)
                    print(f"Saved: {config['output']} ({len(dl.content)} bytes)")
                    return True
                print(f"ERROR: No video data. Sample keys: {list(videos[0].keys())}")
                return False
            
            video_bytes = base64.b64decode(video_data)
            with open(f"/tmp/nuoqi-v8/{config['output']}", "wb") as f:
                f.write(video_bytes)
            print(f"Saved: {config['output']} ({len(video_bytes)} bytes)")
            return True
    
    print("TIMEOUT: Video generation did not complete in 10 minutes")
    return False


def main():
    # Which pets to generate
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(PETS.keys())
    
    results = {}
    for name in targets:
        if name not in PETS:
            print(f"Unknown pet: {name}")
            continue
        success = generate_video(name, PETS[name])
        results[name] = "OK" if success else "FAILED"
    
    print(f"\n{'='*60}")
    print("RESULTS:")
    for name, status in results.items():
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
