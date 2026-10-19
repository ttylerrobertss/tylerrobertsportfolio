"""Download a poster still for each video on multi-video projects.

Saves assets/img/posters/yt-<id>.webp (black letterbox/pillarbox bars trimmed).
Run once when adding a multi-video project, then `python3 build.py`.
"""
import io, json, os, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "posters")


def fetch(video_id):
    for name in ("maxresdefault", "sddefault", "hqdefault"):
        url = f"https://i.ytimg.com/vi/{video_id}/{name}.jpg"
        r = subprocess.run(["curl", "-sf", url], capture_output=True)
        if r.returncode != 0:
            continue
        im = Image.open(io.BytesIO(r.stdout)).convert("RGB")
        if im.width > 120:
            return im
    return None


def trim_bars(im, threshold=18):
    gray = im.convert("L")
    w, h = gray.size
    rows = [sum(gray.getpixel((x, y)) for x in range(0, w, 8)) / len(range(0, w, 8)) for y in range(h)]
    cols = [sum(gray.getpixel((x, y)) for y in range(0, h, 8)) / len(range(0, h, 8)) for x in range(w)]
    top = next((i for i, v in enumerate(rows) if v > threshold), 0)
    bottom = h - next((i for i, v in enumerate(reversed(rows)) if v > threshold), 0)
    left = next((i for i, v in enumerate(cols) if v > threshold), 0)
    right = w - next((i for i, v in enumerate(reversed(cols)) if v > threshold), 0)
    if right - left < w * 0.3 or bottom - top < h * 0.3:
        return im
    return im.crop((left, top, right, bottom))


with open(os.path.join(ROOT, "data.json")) as f:
    data = json.load(f)

os.makedirs(OUT, exist_ok=True)
for p in data["projects"]:
    videos = p.get("videos", [])
    if len(videos) < 2:
        continue
    for v in videos:
        if v.get("provider") != "youtube":
            continue
        path = os.path.join(OUT, f"yt-{v['id']}.webp")
        if os.path.exists(path):
            continue
        im = fetch(v["id"])
        if im is None:
            print("no still:", p["slug"], v["id"])
            continue
        if p.get("video_aspect") != "9:16":
            im = trim_bars(im)
        im.save(path, "WEBP", quality=90, method=6)
        print(p["slug"], v["id"], im.size)
