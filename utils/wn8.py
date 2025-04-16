import json
import os

# Načítanie očakávaných hodnôt pre každý tank
def load_expected_values():
    with open("utils/wn8exp.json", "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_wn8(tank_stats, expected_values):
    total = {
        "damage": 0,
        "frag": 0,
        "spot": 0,
        "def": 0,
        "win": 0,
        "expDamage": 0,
        "expFrag": 0,
        "expSpot": 0,
        "expDef": 0,
        "expWin": 0,
        "battles": 0
    }

    for tank in tank_stats:
        tank_id = tank.get("tank_id")
        battles = tank.get("statistics", {}).get("battles", 0)
        if battles == 0:
            continue

        wn8_ref = next((item for item in expected_values if item["IDNum"] == tank_id), None)
        if not wn8_ref:
            continue

        stats = tank["statistics"]
        total["battles"] += battles
        total["damage"] += stats["damage_dealt"]
        total["frag"] += stats["frags"]
        total["spot"] += stats["spotted"]
        total["def"] += stats["dropped_capture_points"]
        total["win"] += stats["wins"]

        total["expDamage"] += wn8_ref["expDamage"] * battles
        total["expFrag"] += wn8_ref["expFrag"] * battles
        total["expSpot"] += wn8_ref["expSpot"] * battles
        total["expDef"] += wn8_ref["expDef"] * battles
        total["expWin"] += wn8_ref["expWinRate"] * battles

    if total["battles"] == 0:
        return 0

    rDAMAGE = total["damage"] / total["expDamage"] if total["expDamage"] else 0
    rFRAG = total["frag"] / total["expFrag"] if total["expFrag"] else 0
    rSPOT = total["spot"] / total["expSpot"] if total["expSpot"] else 0
    rDEF = total["def"] / total["expDef"] if total["expDef"] else 0
    rWIN = total["win"] / total["expWin"] if total["expWin"] else 0

    rDAMAGEc = max(0, (rDAMAGE - 0.22) / (1 - 0.22))
    rFRAGc = max(0, min(rDAMAGEc + 0.2, (rFRAG - 0.12) / (1 - 0.12)))
    rSPOTc = max(0, min(rDAMAGEc + 0.1, (rSPOT - 0.38) / (1 - 0.38)))
    rDEFc = max(0, min(rDAMAGEc + 0.1, (rDEF - 0.10) / (1 - 0.10)))
    rWINc = max(0, (rWIN - 0.71) / (1 - 0.71))

    wn8 = (
        980 * rDAMAGEc +
        210 * rDAMAGEc * rFRAGc +
        155 * rFRAGc * rSPOTc +
        75 * rDEFc * rFRAGc +
        145 * min(1.8, rWINc)
    )

    return round(wn8)
