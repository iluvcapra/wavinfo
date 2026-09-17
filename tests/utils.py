import json
import os.path
import subprocess
from subprocess import PIPE

FFPROBE = "ffprobe"


def ffprobe(path):
    arguments = [FFPROBE, "-of", "json", "-show_format", "-show_streams", path]
    process = subprocess.run(arguments, stdin=None, stdout=PIPE, stderr=PIPE, check=True)
    if process.returncode == 0:
        output_str = process.stdout.decode("utf-8")
        return json.loads(output_str)
    else:
        return None


def all_files():
    for dirpath, _, filenames in os.walk("tests/test_files"):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in [".wav", ".WAV"]:
                yield os.path.join(dirpath, filename)
