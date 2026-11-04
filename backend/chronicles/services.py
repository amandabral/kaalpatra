import json
import math
from datetime import datetime
from pathlib import Path

class TimeCapsuleService:
    def __init__(self):
        pipeline_dir  = Path(__file__).resolve().parent.parent / "data_pipeline"
        with open(pipeline_dir / "leadership.json","r", encoding="utf-8") as f:
            self.leadership_data = json.load(f)

    @staticmethod
    def calculate_moon_phase(dt:datetime):
        year, month, day = dt.year, dt.month, dt.day
        if month < 3:
            year -= 1
            month += 12
        days = (365.25 * year) + (30.6 * (month + 1)) + day - 694039.09
        days /= 29.5305882
        phase = days - math.floor(days)
        idx = int(round(phase * 8)) % 8
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
        return phases[idx]

    def get_leadership(self, target_date) -> dict:
        result = {"head_of_state": "N/A", "president": "N/A", "role": "Prime Minister"}
        if target_date < datetime.strptime("1947-08-15", "%Y-%m-%d").date():
            result["role"] = "British Viceroy"
            for v in self.leadership_data.get("viceroys_pre_1947", []):
                start = datetime.strptime(v["start"], "%Y-%m-%d").date()
                end = datetime.strptime(v["end"], "%Y-%m-%d").date()
                if start <= target_date <= end:
                    result["head_of_state"] = v["name"]
                    break
            result["president"] = "Pre-Republic (British Crown)"
            return result
        for pm in self.leadership_data.get("prime_ministers", []):
            start = datetime.strptime(pm["start"], "%Y-%m-%d").date()
            end = datetime.strptime(pm["end"], "%Y-%m-%d").date()
            if start <= target_date <= end:
                result["head_of_state"] = f"{pm['name']} ({pm['party']})"
                break
        for pres in self.leadership_data.get("presidents", []):
            start = datetime.strptime(pres["start"], "%Y-%m-%d").date()
            end = datetime.strptime(pres["end"], "%Y-%m-%d").date()
            if start <= target_date <= end:
                result["president"] = pres["name"]
                break
        return result
        