import json
import math
import sys
from datetime import datetime, date
from pathlib import Path
import urllib.request

def get_moon_phase(date: datetime) -> str:
    """
    Calculate the moon phase for a given date.

    Args:
        date (datetime): The date for which to calculate the moon phase."""

    year, month, day = date.year, date.month, date.day
    if month < 3:
        year -= 1
        month += 12
    days = 365.25 * year + 30.6 * (month + 1) + day - 694039.09
    days /= 29.5305882
    phase = days - math.floor(days)
    phase_index = round(phase * 8) % 8
    phase_names = [
        "New Moon(Amavasya)",
        "Waxing Crescent",
        "First Quarter",
        "Waxing Gibbous",
        "Full Moon(Purnima)",
        "Waning Gibbous",
        "Last Quarter",
        "Waning Crescent",
    ]
    return phase_names[phase_index]

def get_leadership(target_date:str, leadership_data:dict)->dict:
    """ Finds exact leaders in power on target_date(YYYY-MM-DD)."""
    target = datetime.strptime(target_date, "%Y-%m-%d").date()
    result = {"head_of_state":"N/A", "president":"N/A", "role":"Prime Minister"}

    # Check Viceroy (Pre-1947)
    if target < date(1947, 8, 15):
        result["role"] = "British Viceroy"
        for v in leadership_data.get("prime_ministers",[]):
            start = datetime.strptime(v["start"], "%Y-%m-%d").date()
            end = datetime.strptime(v["end"], "%Y-%m-%d").date()
            if start<=target<=end:
                result["head_of_state"] = v["name"]
                break
        result["president"] = "Pre-Republic (British Crown)"

        return result

    # Check Prime Minister
    for pm in leadership_data.get("prime_ministers",[]):
        start = datetime.strptime(pm["start"], "%Y-%m-%d").date()
        end = datetime.strptime(pm["end"], "%Y-%m-%d").date()
        if start<=target<=end:
            result["head_of_state"]=f"{pm['name']}({pm['party']})"
            break

    # Check President
    for pres in leadership_data.get("presidents",[]):
        start = datetime.strptime(pres["start"], "%Y-%m-%d").date()
        end = datetime.strptime(pres["end"], "%Y-%m-%d").date()
        if start<=target<=end:
            result["president"] = pres["name"]
            break

    return result

def query_wikidata(sparql_query: str) -> list:
    """Helper to execute SPARQL queries against Wikidata."""
    endpoint_url = "https://query.wikidata.org/sparql"
    params = urllib.parse.urlencode({"query": sparql_query, "format": "json"})
    url = f"{endpoint_url}?{params}"
    headers = {"User-Agent": "KaalPatraApp/1.0 (aman@kaalpatra.org; portfolio project)"}
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            return data.get("results", {}).get("bindings", [])
    except Exception as e:
        print(f"⚠️ Wikidata query error: {e}")
        return []

def fetch_indian_luminaries(year: int, month: int, day: int) -> dict:
    """
    1. Fetches exact date twins (same year, month, day).
    2. Fetches famous Indian calendar twins (same month & day across history, ranked by notability).
    """
    # Query 1: Exact Date Twins (Born on that exact day in that specific year)
    exact_sparql = f"""
    SELECT DISTINCT ?person ?personLabel ?dob ?sitelinks (SAMPLE(?occLabel) AS ?occupation) WHERE {{
      ?person wdt:P31 wd:Q5 ;
              wdt:P569 ?dob ;
              wikibase:sitelinks ?sitelinks .
      {{ ?person wdt:P27 wd:Q668 . }} UNION {{ ?person wdt:P27 wd:Q129286 . }}
      FILTER(YEAR(?dob) = {year} && MONTH(?dob) = {month} && DAY(?dob) = {day})
      OPTIONAL {{
        ?person wdt:P106 ?occ .
        ?occ rdfs:label ?occLabel .
        FILTER(LANG(?occLabel) = "en")
      }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    GROUP BY ?person ?personLabel ?dob ?sitelinks
    ORDER BY DESC(?sitelinks)
    LIMIT 5
    """
    # Query 2: Top Calendar Twins (Ranked by Wikipedia notability sitelinks)
    calendar_sparql = f"""
    SELECT DISTINCT ?person ?personLabel ?dob ?sitelinks (SAMPLE(?occLabel) AS ?occupation) WHERE {{
      ?person wdt:P31 wd:Q5 ;
              wdt:P569 ?dob ;
              wikibase:sitelinks ?sitelinks .
      {{ ?person wdt:P27 wd:Q668 . }} UNION {{ ?person wdt:P27 wd:Q129286 . }}
      FILTER(MONTH(?dob) = {month} && DAY(?dob) = {day})
      OPTIONAL {{
        ?person wdt:P106 ?occ .
        ?occ rdfs:label ?occLabel .
        FILTER(LANG(?occLabel) = "en")
      }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    GROUP BY ?person ?personLabel ?dob ?sitelinks
    ORDER BY DESC(?sitelinks)
    LIMIT 12
    """
    exact_raw = query_wikidata(exact_sparql)
    calendar_raw = query_wikidata(calendar_sparql)
    def parse_bindings(bindings):
        results = []
        for b in bindings:
            name = b.get("personLabel", {}).get("value", "")
            dob = b.get("dob", {}).get("value", "")[:10]
            occ = b.get("occupation", {}).get("value", "Notable Indian Personality")
            sitelinks = int(b.get("sitelinks", {}).get("value", "0"))
            if name and not name.startswith("Q"):
                results.append({"name": name, "dob": dob, "occupation": occ, "score": sitelinks})
        return results
    return {
        "exact_twins": parse_bindings(exact_raw),
        "calendar_twins": parse_bindings(calendar_raw)
    }


def resolve_date(date_str: str):

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    leadership_path = Path(__file__).resolve().parent / "leadership.json"
    with open(leadership_path, "r", encoding="utf-8") as f:
        leadership_data = json.load(f)

    # Calender calculations
    days_ago = (datetime.now() - dt).days
    day_name = dt.strftime("%A")
    moon = get_moon_phase(dt)

    # Leadership Lookup
    leaders = get_leadership(date_str, leadership_data)

    print(f"\n================ TIME CAPSULE FOR {date_str} ================")
    print(f"🗓️ Day of Week : {day_name}")
    print(f"⏳ Days Elapsed: {days_ago:,} days ago")
    print(f"🌕 Moon Phase  : {moon}")
    print(f"🏛️ Leader ({leaders['role']}): {leaders['head_of_state']}")
    print(f"🇮🇳 President  : {leaders['president']}")

    # 3. Query Wikidata
    print(f"\n📡 Querying Wikidata (ranked by national prominence)...")
    luminary_data = fetch_indian_luminaries(dt.year, dt.month, dt.day)
    # 4. Display Exact Date Twins
    print(f"\n🎯 EXACT DATE TWIN (Born on the exact date {date_str}):")
    if luminary_data["exact_twins"]:
        for p in luminary_data["exact_twins"]:
            print(f"  ⭐ {p['name']} ({p['occupation']}) — Born on {p['dob']} [Notability Score: {p['score']}]")
    else:
        print("  • No celebrity exact-date twin recorded for this exact day.")
    # 5. Display Calendar Twins
    print(f"\n🎂 TOP INDIAN CALENDAR TWINS (Born on {dt.strftime('%B %d')} across history):")
    calendar_twins = [p for p in luminary_data["calendar_twins"] if p['dob'] != date_str]
    for p in calendar_twins[:8]:
        print(f"  • {p['name']} (Born {p['dob']}) — {p['occupation']} [Score: {p['score']}]")

if __name__ == "__main__":
    test_date = sys.argv[1] if len(sys.argv) > 1 else "1983-06-25"
    resolve_date(test_date)