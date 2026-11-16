# Run before rendering:  python fact_check.py   (must print ALL FACTS OK)
import json, math, sys
t_mm = 0.1
moon_km = 384400
moon_mm = moon_km * 1e6
facts = json.load(open("fact_sheet.json", encoding="utf-8"))["facts"]
bad = 0
for f in facts:
    try:
        ok = bool(eval(f["check"]))
    except Exception as e:
        ok = False
    print(("OK   " if ok else "FAIL ") + f["id"] + "  " + f["claim"])
    bad += (not ok)
print("ALL FACTS OK" if bad == 0 else f"{bad} FACT(S) FAILED")
sys.exit(1 if bad else 0)
