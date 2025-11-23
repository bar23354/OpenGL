import sys

if len(sys.argv) < 2:
    print("Uso: python check_obj.py <archivo.obj>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    lines = f.readlines()

vertex_count = 0
texcoord_count = 0
normal_count = 0
face_count = 0

for line in lines:
    line = line.strip()
    if line.startswith('v '):
        vertex_count += 1
    elif line.startswith('vt '):
        texcoord_count += 1
    elif line.startswith('vn '):
        normal_count += 1
    elif line.startswith('f '):
        face_count += 1

import os
print(f"{os.path.basename(filename):30} | v:{vertex_count:8} | vt:{texcoord_count:8} | vn:{normal_count:8} | f:{face_count:8}")
