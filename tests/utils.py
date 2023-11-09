import os.path
import sys
import subprocess
from subprocess import PIPE
import json

FFPROBE = 'ffprobe'


def ffprobe(path):
    arguments = [FFPROBE, "-of", "json", 
                 "-show_format", "-show_streams", path]
    if int(sys.version[0]) <  3:
        process = subprocess.Popen(arguments, stdout=PIPE)
        process.wait()
        if process.returncode == 0:
            output = process.communicate()[0]
            if output:
                output_str = output.decode('utf-8')
                return json.loads(output_str)
        else:
            return None
    else: 
        process = subprocess.run(arguments, stdin=None, 
                                 stdout=PIPE, stderr=PIPE)
        if process.returncode == 0:
            output_str = process.stdout.decode('utf-8')
            return json.loads(output_str)
        else:
            return None


def all_files():
    for dirpath, _, filenames in os.walk('tests/test_files'):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in ['.wav', '.WAV']:
                yield os.path.join(dirpath, filename)
