from PIL import Image
import os, json

def get_avg(path):
    if "mcmeta" in path or "debug" in path or ".DS_Store" in path or "stage" in path: return None
    img = Image.open(path).convert("RGBA")
    pixels = img.load()
    if any([pixels[x, y][3] == 0 for x in range(img.width) for y in range(img.height)]): return None
    width, height = img.size
    r, g, b = 0, 0, 0
    for x in range(width):
        for y in range(height):
            pr, pg, pb, _ = pixels[x, y]
            r += pr
            g += pg
            b += pb
    total = width * height
    return r // total, g // total, b // total

def load_avg_values():
    textures = os.listdir("textures")
    textures.sort()
    avg_values = {}
    for texture in textures:
        avg = get_avg(f"textures/{texture}")
        if avg and texture:
            avg_values[texture] = avg
    return avg_values

if __name__ == "__main__":
    with open("avg_values.json", "w") as f: json.dump(load_avg_values(), f)