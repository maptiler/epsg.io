import os 
import subprocess

files = [os.path.join(dir, f) for (dir, subdirs, fs) in os.walk("./tests") for f in fs if f.endswith(".py")]

# TODO add all these files to sys
# Then call pytest once

for file in files:
    subprocess.call(["pytest", "-rP", file])
    # subprocess.call(["python", file])
