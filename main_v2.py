from PIL import Image
import json, threading, time

path = input("Enter the path of the image you want to convert: ")
thread_num = input("Enter the number of threads you want to use or press enter for default of 10: ")
if thread_num: thread_num = int(thread_num)
else: thread_num = 10

with open("avg_values.json", "r") as f: avg_values = json.load(f)
img = Image.open(path).convert("RGBA")
pixels = img.load()
pixel_info = []
new_img = Image.new("RGBA", (img.width*16, img.height*16))

print(f"Total processing time should be around {round((img.width*img.height)/4000, 4)} seconds.")

def scan_image() -> None:
    global pixel_info
    for x in range(img.width):
        for y in range(img.height):
            pr, pg, pb, _ = pixels[x, y]
            pixel_info.append({"x": x, "y": y, "r": pr, "g": pg, "b": pb, "texture": None})

def choose_best_texture(pr, pg, pb) -> str:
    cr, cg, cb = 9999, 9999, 9999
    current_texture = None
    for texture, (tr, tg, tb) in avg_values.items():
        if abs(pr-tr) + abs(pg-tg) + abs(pb-tb) < abs(pr-cr) + abs(pg-cg) + abs(pb-cb):
            current_texture = texture
            cr, cg, cb = tr, tg, tb
    return current_texture

def choose_best_textures(start, end) -> None:
    global pixel_info
    for n in range(start, end):
        pixel = pixel_info[n]
        pixel_info[n]["texture"] = choose_best_texture(pixel["r"], pixel["g"], pixel["b"])

def place_texture(x, y, texture) -> None:
    global new_img
    texture_img = Image.open(f"textures/{texture}").convert("RGBA")
    texture_pixels = texture_img.load()
    for i in range(16):
        for j in range(16):
            px = list(texture_pixels[i, j])
            px[3] = (pixels[x, y][3])
            new_img.putpixel((x*16+i, y*16+j), tuple(px))

def place_textures(start, end) -> None:
    for n in range(start, end):
        pixel = pixel_info[n]
        place_texture(pixel["x"], pixel["y"], pixel["texture"])

def make_threads(target, data_length, num_threads) -> None:
    threads = []
    chunk = data_length // num_threads
    for i in range(num_threads):
        start = i * chunk
        end = (i+1) * chunk if i < num_threads-1 else data_length
        if i == num_threads-1: end = data_length
        threads.append(threading.Thread(target=target, args=(start, end)))
    for thread in threads: 
        thread.start()
    for thread in threads:
        thread.join()

total = 0
print("1) Getting pixel info.")
start = time.time()
scan_image()
print(f"\033[1A1) Getting pixel info. Time taken: {round(time.time()-start, 4)} seconds.")
total += time.time()-start

print("2) Choosing best texture for each pixel.")
start = time.time()
make_threads(choose_best_textures, len(pixel_info), thread_num)
print(f"\033[1A2) Choosing best texture for each pixel. Time taken: {round(time.time()-start, 4)} seconds.")
total += time.time()-start

print("3) Placing textures.")
start = time.time()
make_threads(place_textures, len(pixel_info), thread_num)
print(f"\033[1A3) Placing textures. Time taken: {round(time.time()-start, 4)} seconds.")
total += time.time()-start

print(f"Saving image as {path.split('.')[0]}_converted.png. Total processing time: {round(total, 4)} seconds.")
new_img.save(f"{path.split('.')[0]}_converted.png")