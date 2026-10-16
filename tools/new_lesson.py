import os
import sys
import json
import shutil

def main():
    if len(sys.argv) != 3:
        print("Usage: python new_lesson.py <number> <name>")
        print("Example: python new_lesson.py 13 test_lesson")
        sys.exit(1)

    num_str = sys.argv[1]
    name = sys.argv[2]

    num = int(num_str)
    formatted_num = f"{num:02d}"
    filename = f"{formatted_num}_{name}.py"
    filepath = os.path.join("lessons", filename)

    if os.path.exists(filepath):
        print(f"Error: {filepath} already exists.")
        sys.exit(1)

    with open("lessons/_template.py", "r") as f:
        template = f.read()

    template = template.replace("{lesson_name}", name)
    template = template.replace("{lesson_number}", formatted_num)

    with open(filepath, "w") as f:
        f.write(template)

    print(f"Created {filepath}")

    with open("lessons.json", "r") as f:
        data = json.load(f)

    new_entry = {
        "day": len(data["lessons"]) + 1,
        "title": name.replace("_", " ").title(),
        "summary": "First sentence. Second sentence. Third sentence.",
        "script": f"lessons/{filename}",
        "figures": [
            f"{formatted_num}_{name}.png"
        ]
    }

    data["lessons"].append(new_entry)

    with open("lessons.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Updated lessons.json with a placeholder entry.")

if __name__ == "__main__":
    main()
