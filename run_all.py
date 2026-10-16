import os
import glob
import subprocess
import sys

def main():
    lessons = sorted(glob.glob("lessons/[0-9][0-9]_*.py"))

    if not lessons:
        print("No lessons found.")
        sys.exit(1)

    for lesson in lessons:
        print(f"Running {lesson}...")
        result = subprocess.run([sys.executable, lesson])
        if result.returncode != 0:
            print(f"Failed running {lesson}")
            sys.exit(1)

    print("All lessons ran successfully.")

if __name__ == "__main__":
    main()
