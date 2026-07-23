#!/usr/bin/env python3
"""Генерация брендовых иллюстраций для дека через OpenRouter Gemini 2.5 Flash Image.
Стиль: брутализм red(#E10A17)/black/white, БЕЗ текста. Для отдельных слайдов.
"""
import os, base64, requests, sys

# ключ из .secrets
key = ""
with open(os.path.expanduser("~/.secrets/zinin-chat-openrouter.env")) as f:
    for line in f:
        if line.startswith("OPENROUTER_API_KEY="):
            key = line.split("=", 1)[1].strip()
os.environ["OPENROUTER_API_KEY"] = key

URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash-image"

NEG = ("no text, no letters, no words, no typography, no numbers, no captions, "
       "no blue, no navy, no teal, no pastel, no soft colors, no gradients of many colors, "
       "no generic stock photo, no smiling people, no handshakes, no laptops, "
       "no team meetings, no cartoon mascots, no neon signs, no charts, no tattoo flash")

OUT = "/Users/timofeyzinin/sarapulov-zinin-ai/webinar/gen"
os.makedirs(OUT, exist_ok=True)

JOBS = {
    "hero_exo": (
        "Bold graphic poster illustration of a single confident human figure wearing a "
        "powered mechanical exoskeleton frame, heroic upright stance, one person amplified "
        "by machine. STRICT palette: pure white background, black ink, one bold red accent "
        "(#E10A17) only. Flat geometric vector shapes, thick clean linework, brutalist "
        "poster aesthetic, strong diagonal composition, subtle halftone grain, very high contrast."
    ),
    "network_apparat": (
        "Bold graphic illustration of one large central node connected by clean straight lines "
        "to many smaller surrounding nodes, a hub-and-spoke network as abstract poster art, "
        "sense of a system radiating from a center. STRICT palette: pure white background, "
        "black lines and nodes, central node bold red (#E10A17). Flat geometric, brutalist "
        "poster, sharp edges, high contrast, minimal, subtle grain."
    ),
    "autonomous_agent": (
        "Bold graphic poster of a single autonomous robotic arm working by itself on a clean "
        "conveyor line, machine operating independently, industrial precision. STRICT palette: "
        "pure white background, black ink shapes, one red (#E10A17) accent. Flat geometric "
        "vector style, brutalist industrial poster, diagonal dynamic angle, halftone grain, high contrast."
    ),
}

def gen(name, prompt):
    full = f"Generate a high-quality image: {prompt}\n\nDo NOT include: {NEG}"
    r = requests.post(URL, headers={"Authorization": f"Bearer {key}",
                      "Content-Type": "application/json"},
                      json={"model": MODEL, "messages": [{"role": "user", "content": full}]},
                      timeout=120)
    r.raise_for_status()
    msg = r.json()["choices"][0]["message"]
    imgs = msg.get("images", [])
    if not imgs:
        print(f"{name}: NO IMAGE returned. content={str(msg.get('content'))[:120]}")
        return
    url = imgs[0].get("image_url", {}).get("url", "")
    if "base64," in url:
        data = base64.b64decode(url.split("base64,")[1])
        path = f"{OUT}/{name}.png"
        with open(path, "wb") as f:
            f.write(data)
        print(f"{name}: OK -> {path} ({len(data)} bytes)")
    else:
        print(f"{name}: url not base64: {url[:60]}")

for name, prompt in JOBS.items():
    try:
        gen(name, prompt)
    except Exception as e:
        print(f"{name}: ERROR {e}")
print("DONE")
