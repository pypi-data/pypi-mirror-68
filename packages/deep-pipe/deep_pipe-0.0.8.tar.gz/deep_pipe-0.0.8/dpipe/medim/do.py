from pathlib import Path

for file in Path('.').iterdir():
    if file.is_dir():
        continue
    with open(file, 'w') as f:
        f.write(f'from dpipe.im.{file.name.split(".")[0]} import *\n')
