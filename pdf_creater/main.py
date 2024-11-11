
from pdf_generator import generate_ocr_v2,generate_ocr
import json 
maps_vins = generate_ocr_v2(50,"examples","output.pdf")

check_gen = set()
for v in maps_vins.values():
    check_gen.update(v)
assert len(check_gen) == len(maps_vins)*17

with open("output.json","w") as f:
    json.dump(maps_vins,f)