from PIL import Image
import json

path = "macintosh.png"

with open("avg_values.json", "r") as f: avg_values = json.load(f)
img = Image.open(path).convert("RGBA")
pixels = img.load()

new_img = Image.new("RGBA", (img.width*16, img.height*16))
print()
for x in range(img.width):
    for y in range(img.height):
        print(f"\033[1A{x}/{img.width} {y}/{img.height}     ")
        pr, pg, pb, _ = pixels[x, y]
        current_texture = None
        cr, cg, cb = 9999, 9999, 9999
        for texture, (tr, tg, tb) in avg_values.items():
            if abs(pr-tr) + abs(pg-tg) + abs(pb-tb) < abs(pr-cr) + abs(pg-cg) + abs(pb-cb):
                current_texture = texture
                cr, cg, cb = tr, tg, tb
        
        texture_img = Image.open(f"textures/{current_texture}").convert("RGB")
        texture_pixels = texture_img.load()
        for i in range(16):
            for j in range(16):
                px = list(texture_pixels[i, j])
                px.append(pixels[x, y][3])
                new_img.putpixel((x*16+i, y*16+j), tuple(px))

new_img.save(f"{path.split('.')[0]}_converted.png")