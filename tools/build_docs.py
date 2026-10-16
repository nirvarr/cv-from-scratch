import os
import sys
import json
import shutil
import hashlib
import numpy as np
import cv2

def generate_icons(output_dir):
    """Generates 192x192 and 512x512 icons using numpy and cv2."""
    os.makedirs(output_dir, exist_ok=True)
    sizes = [192, 512]

    for size in sizes:
        icon_path = os.path.join(output_dir, f'icon-{size}x{size}.png')
        if not os.path.exists(icon_path):
            img = np.zeros((size, size, 3), dtype=np.uint8)
            # Create a simple icon design: dark background with a colorful "CV" and circles
            img[:] = [30, 30, 40]

            center = (size // 2, size // 2)
            radius = int(size * 0.4)
            cv2.circle(img, center, radius, (255, 100, 100), -1)
            cv2.circle(img, center, int(radius * 0.8), (30, 30, 40), -1)

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = size / 100
            thickness = max(2, int(size / 30))

            text_size = cv2.getTextSize("CV", font, font_scale, thickness)[0]
            text_x = (size - text_size[0]) // 2
            text_y = (size + text_size[1]) // 2

            cv2.putText(img, "CV", (text_x, text_y), font, font_scale, (200, 255, 200), thickness, cv2.LINE_AA)
            cv2.imwrite(icon_path, img)

def copy_files(src_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    for item in os.listdir(src_dir):
        if item.endswith('.py') and not item.startswith('_') and not item.startswith('.'):
            shutil.copy2(os.path.join(src_dir, item), dest_dir)

def copy_figures(src_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    for item in os.listdir(src_dir):
        if item.endswith('.png'):
            shutil.copy2(os.path.join(src_dir, item), dest_dir)

def calculate_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def update_service_worker(sw_path, cache_version, files_to_cache):
    with open(sw_path, 'r') as f:
        sw_content = f.read()

    # We will replace the placeholder in sw.js or just re-write the top part
    import re
    sw_content = re.sub(r"const CACHE_NAME = 'cv-from-scratch-v.*';", f"const CACHE_NAME = 'cv-from-scratch-v{cache_version}';", sw_content)

    files_str = ",\n  ".join([f"'{f}'" for f in files_to_cache])
    sw_content = re.sub(r"const URLS_TO_CACHE = \[.*?\];", f"const URLS_TO_CACHE = [\n  {files_str}\n];", sw_content, flags=re.DOTALL)

    with open(sw_path, 'w') as f:
        f.write(sw_content)

def main():
    print("Building docs...")
    os.makedirs("docs/assets/lessons", exist_ok=True)
    os.makedirs("docs/icons", exist_ok=True)

    # Generate icons if missing
    generate_icons("docs/icons")

    # Copy lessons.json
    shutil.copy2("lessons.json", "docs/lessons.json")

    # Copy scripts
    copy_files("lessons", "docs/assets/lessons")

    # Copy figures
    if os.path.exists("outputs"):
        copy_figures("outputs", "docs/assets")

    # Build list of files to cache
    files_to_cache = [
        './',
        'index.html',
        'style.css',
        'app.js',
        'manifest.webmanifest',
        'lessons.json',
        'icons/icon-192x192.png',
        'icons/icon-512x512.png'
    ]

    with open("lessons.json", "r") as f:
        data = json.load(f)

    for lesson in data["lessons"]:
        script_name = os.path.basename(lesson["script"])
        files_to_cache.append(f"assets/lessons/{script_name}")
        for fig in lesson["figures"]:
            files_to_cache.append(f"assets/{fig}")

    # Calculate a combined hash for cache versioning
    combined_hash = hashlib.md5()
    combined_hash.update(json.dumps(files_to_cache).encode())
    if os.path.exists("docs/app.js"): combined_hash.update(calculate_hash("docs/app.js").encode())
    if os.path.exists("docs/style.css"): combined_hash.update(calculate_hash("docs/style.css").encode())
    cache_version = combined_hash.hexdigest()[:8]

    if os.path.exists("docs/sw.js"):
        update_service_worker("docs/sw.js", cache_version, files_to_cache)
    else:
        print("docs/sw.js not found, skipping service worker update. (Make sure you create it first!)")

    print("Docs built successfully.")

if __name__ == "__main__":
    main()
