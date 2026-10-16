import os
import json
import subprocess
import shutil
import tempfile
import pytest

def load_lessons_data():
    with open("lessons.json", "r") as f:
        return json.load(f)

data = load_lessons_data()

@pytest.mark.parametrize("lesson", data["lessons"])
def test_lesson_structure(lesson):
    """Test that every lesson's script and figures exist."""
    script_path = lesson["script"]
    assert os.path.exists(script_path), f"Script missing: {script_path}"

    for figure in lesson["figures"]:
        fig_path = os.path.join("outputs", figure)
        assert os.path.exists(fig_path), f"Figure missing: {fig_path}"

def test_docs_in_sync():
    """
    Test that the docs/ folder is up to date by running build_docs.py
    in a temporary copy and comparing the resulting cache version or hashes.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy the necessary files to the temp dir to simulate a clean build
        for item in ["lessons", "outputs", "tools", "lessons.json", "docs"]:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.copytree(item, os.path.join(tmpdir, item))
                else:
                    shutil.copy2(item, tmpdir)

        # Change directory to the temp dir
        original_cwd = os.getcwd()
        os.chdir(tmpdir)

        try:
            # Build docs in the temp dir
            subprocess.run(["python", "tools/build_docs.py"], check=True, capture_output=True)

            # Compare the newly built docs/sw.js with the original one
            # Because we re-built it in the temp dir, if the original one was out of sync,
            # the cache hashes would differ, or files would be missing in the original docs/.

            with open("docs/sw.js", "r") as f:
                new_sw = f.read()

            os.chdir(original_cwd)

            with open("docs/sw.js", "r") as f:
                old_sw = f.read()

            assert new_sw == old_sw, "docs/sw.js is out of sync. Please run `python tools/build_docs.py`."

            # Optionally check if all files in temp docs exist in real docs
            for root, _, files in os.walk(os.path.join(tmpdir, "docs")):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), os.path.join(tmpdir, "docs"))
                    assert os.path.exists(os.path.join("docs", rel_path)), f"File missing in docs: {rel_path}. Run build_docs.py."

        finally:
            if os.getcwd() != original_cwd:
                os.chdir(original_cwd)
