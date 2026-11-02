import json
import math
import sys
from datetime import datetime
from pathlib import Path

# Paths relative to this script's directory
PIPELINE_DIR = Path(__file__).resolve().parent
SEEDS_DIR = PIPELINE_DIR / "seeds"
LEADERSHIP_FILE = PIPELINE_DIR / "leadership.json"
ECONOMICS_FILE = PIPELINE_DIR / "economics.json"
CULTURE_FILE = PIPELINE_DIR / "culture.json"
EVENTS_FILE = SEEDS_DIR / "events.json"
LUMINARIES_FILE = SEEDS_DIR / "luminaries.json"

def get_moon_phase(d: datetime) -> str:
    year, month, day = d.year, d.month, d.day
    if month < 3:
        year -= 1
        month += 12
    days = (365.25 * year) + (30.6 * (month + 1)) + day - 694039.09
    days /= 29.5305882
    phase = days - math.floor(days)
    phase_idx = int(round(phase * 8)) % 8
    phases = [
        "New Moon (Amavasya)",
        "Waxing Crescent",
        "First Quarter",
        "Waxing Gibbous",
        "Full Moon (Purnima)",
        "Waning Gibbous",
        "Last Quarter",
        "Waning Crescent"
    ]
    return phases[phase_idx]


def get_leadership(target_date_str: str, leadership_data: dict) -> dict:
    target = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    result = {"head_of_state": "N/A", "president": "N/A", "role": "Prime Minister"}

    if target < datetime.strptime("1947-08-15", "%Y-%m-%d").date():
        result["role"] = "British Viceroy"
        for v in leadership_data.get("viceroys_pre_1947", []):
            start = datetime.strptime(v["start"], "%Y-%m-%d").date()
            end = datetime.strptime(v["end"], "%Y-%m-%d").date()
            if start <= target <= end:
                result["head_of_state"] = v["name"]
                break
        result["president"] = "Pre-Republic (British Crown)"
        return result

    for pm in leadership_data.get("prime_ministers", []):
        start = datetime.strptime(pm["start"], "%Y-%m-%d").date()
        end = datetime.strptime(pm["end"], "%Y-%m-%d").date()
        if start <= target <= end:
            result["head_of_state"] = f"{pm['name']} ({pm['party']})"
            break

    for pres in leadership_data.get("presidents", []):
        start = datetime.strptime(pres["start"], "%Y-%m-%d").date()
        end = datetime.strptime(pres["end"], "%Y-%m-%d").date()
        if start <= target <= end:
            result["president"] = pres["name"]
            break

    return result


def get_economics(year: int, economics_data: dict) -> dict:
    benchmarks = sorted(economics_data.get("benchmarks", []), key=lambda x: x["year"])
    if year <= benchmarks[0]["year"]:
        return benchmarks[0]
    if year >= benchmarks[-1]["year"]:
        return benchmarks[-1]

    for i in range(len(benchmarks) - 1):
        low, high = benchmarks[i], benchmarks[i + 1]
        if low["year"] <= year <= high["year"]:
            ratio = (year - low["year"]) / (high["year"] - low["year"])
            return {
                "gold_10g": round(low["gold_10g"] + ratio * (high["gold_10g"] - low["gold_10g"]), 2),
                "usd_inr": round(low["usd_inr"] + ratio * (high["usd_inr"] - low["usd_inr"]), 2),
                "petrol_litre": round(low["petrol_litre"] + ratio * (high["petrol_litre"] - low["petrol_litre"]), 2),
                "cinema_ticket": round(low["cinema_ticket"] + ratio * (high["cinema_ticket"] - low["cinema_ticket"]), 2),
                "salary_clerk": low.get("salary_clerk")
            }
    return benchmarks[-1]


def get_culture(year: int, culture_data: dict) -> dict:
    for era in culture_data.get("eras", []):
        if era["start_year"] <= year <= era["end_year"]:
            return era
    return culture_data.get("eras", [])[-1]


def get_local_events_and_luminaries(target_date_str: str, events_data: list, luminaries_data: list) -> dict:
    target_dt = datetime.strptime(target_date_str, "%Y-%m-%d")
    month, day = target_dt.month, target_dt.day

    # 1. Exact date events
    exact_events = [e for e in events_data if e["date"] == target_date_str]

    # 2. Exact date twin (born on that exact day)
    exact_twins = [l for l in luminaries_data if l["dob"] == target_date_str]

    # 3. Calendar twins (born on same month and day)
    calendar_twins = []
    for l in luminaries_data:
        ldt = datetime.strptime(l["dob"], "%Y-%m-%d")
        if ldt.month == month and ldt.day == day and l["dob"] != target_date_str:
            calendar_twins.append(l)

    return {
        "exact_events": exact_events,
        "exact_twins": exact_twins,
        "calendar_twins": calendar_twins
    }


def resolve_date(date_str: str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")

    # Load local JSON sources
    with open(LEADERSHIP_FILE, "r", encoding="utf-8") as f:
        leadership_data = json.load(f)
    with open(ECONOMICS_FILE, "r", encoding="utf-8") as f:
        econ_data = json.load(f)
    with open(CULTURE_FILE, "r", encoding="utf-8") as f:
        culture_data = json.load(f)
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        events_data = json.load(f)
    with open(LUMINARIES_FILE, "r", encoding="utf-8") as f:
        luminaries_data = json.load(f)
    # Resolve
    days_ago = (datetime.now() - dt).days
    day_name = dt.strftime("%A")
    moon = get_moon_phase(dt)
    leaders = get_leadership(date_str, leadership_data)
    econ = get_economics(dt.year, econ_data)
    cult = get_culture(dt.year, culture_data)
    local_data = get_local_events_and_luminaries(date_str, events_data, luminaries_data)

    print(f"\n================ TIME CAPSULE FOR {date_str} ================")
    print(f"🗓️ Day of Week : {day_name}")
    print(f"⏳ Days Elapsed: {days_ago:,} days ago")
    print(f"🌕 Moon Phase  : {moon}")
    print(f"🏛️ Leader ({leaders['role']}): {leaders['head_of_state']}")
    print(f"🇮🇳 President  : {leaders['president']}")

    print(f"\n🪙 NOSTALGIA PRICE INDEX ({dt.year}):")
    print(f"  • 10g Gold Price    : ₹{econ['gold_10g']:,.2f}")
    print(f"  • USD to INR Rate   : $1 = ₹{econ['usd_inr']:.2f}")
    print(f"  • 1L Petrol Price   : ₹{econ['petrol_litre']:.2f}")
    print(f"  • Cinema Ticket Avg : ₹{econ['cinema_ticket']:.2f}")
    print(f"  • Typical Clerk Pay : {econ['salary_clerk']}")

    print(f"\n🎬 POP CULTURE & CINEMA ({dt.year}):")
    print(f"  • Era Badge         : 🏷️  {cult['badge']}")
    print(f"  • Blockbuster Film  : 🍿 {cult['top_movie']}")
    print(f"  • Radio Hit Track   : 🎵 {cult['hit_song']}")
    print(f"  • Way of Life       : 📻 {cult['lifestyle']}")

    print(f"\n📰 HISTORIC MILESTONES ON THIS EXACT DATE:")
    if local_data["exact_events"]:
        for ev in local_data["exact_events"]:
            print(f"  ⭐ [{ev['category']}] {ev['title']}")
            print(f"     {ev['description']}")
    else:
        print(f"  • Peaceful day in national records. Cultural & economic era: {cult['badge']}.")

    print(f"\n🎯 EXACT DATE TWIN (Born on {date_str}):")
    if local_data["exact_twins"]:
        for p in local_data["exact_twins"]:
            print(f"  ⭐ {p['name']} ({p['field']}) — {p['bio']}")
    else:
        print("  • No celebrity exact-date twin recorded on this exact day.")

    print(f"\n🎂 CALENDAR BIRTHDAY TWINS (Born on {dt.strftime('%B %d')}):")
    if local_data["calendar_twins"]:
        for p in local_data["calendar_twins"]:
            print(f"  • {p['name']} (Born {p['dob']}) [{p['field']}] — {p['bio']}")
    else:
        print(f"  • No luminaries in current seed set for {dt.strftime('%B %d')}.")


if __name__ == "__main__":
    test_date = sys.argv[1] if len(sys.argv) > 1 else "1983-06-25"
    resolve_date(test_date)