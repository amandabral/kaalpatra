import json
from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand
from chronicles.models import YearSnapshot, HistoricalEvents, Luminary


class Command(BaseCommand):
    help = "Seeds PostgreSQL database with 100 years of economic, cultural, and luminary records"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent / "data_pipeline"
        seeds_dir = base_dir / "seeds"

        self.stdout.write(self.style.NOTICE("🌱 Starting KaalPatra database seed..."))

        # 1. Seed Historical Events
        with open(seeds_dir / "events.json", "r", encoding="utf-8") as f:
            events_data = json.load(f)

        created_events = 0
        for ev in events_data:
            obj, created = HistoricalEvents.objects.update_or_create(
                date=ev["date"],
                title=ev["title"],
                defaults={
                    "description": ev["description"],
                    "category": ev.get("category", "GENERAL")
                }
            )
            if created:
                created_events += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Historical Events seeded: {len(events_data)} total ({created_events} new)"))

        # 2. Seed Luminaries
        with open(seeds_dir / "luminaries.json", "r", encoding="utf-8") as f:
            lums_data = json.load(f)

        created_lums = 0
        for l in lums_data:
            dt = datetime.strptime(l["dob"], "%Y-%m-%d").date()
            obj, created = Luminary.objects.update_or_create(
                name=l["name"],
                dob=dt,
                defaults={
                    "birth_month": dt.month,
                    "birth_day": dt.day,
                    "field": l.get("field", "ARTS"),
                    "bio": l["bio"]
                }
            )
            if created:
                created_lums += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Luminaries seeded: {len(lums_data)} total ({created_lums} new)"))

        # 3. Seed 100-Year Snapshots (1925 - 2025)
        with open(base_dir / "economics.json", "r", encoding="utf-8") as f:
            econ_data = json.load(f)
        with open(base_dir / "culture.json", "r", encoding="utf-8") as f:
            cult_data = json.load(f)

        benchmarks = sorted(econ_data.get("benchmarks", []), key=lambda x: x["year"])
        eras = cult_data.get("eras", [])

        created_snapshots = 0
        for yr in range(1925, 2026):
            # Interpolate Economics
            if yr <= benchmarks[0]["year"]:
                econ = benchmarks[0]
            elif yr >= benchmarks[-1]["year"]:
                econ = benchmarks[-1]
            else:
                for i in range(len(benchmarks) - 1):
                    low, high = benchmarks[i], benchmarks[i + 1]
                    if low["year"] <= yr <= high["year"]:
                        r = (yr - low["year"]) / (high["year"] - low["year"])
                        econ = {
                            "gold_10g": round(low["gold_10g"] + r * (high["gold_10g"] - low["gold_10g"]), 2),
                            "usd_inr": round(low["usd_inr"] + r * (high["usd_inr"] - low["usd_inr"]), 2),
                            "petrol_litre": round(low["petrol_litre"] + r * (high["petrol_litre"] - low["petrol_litre"]), 2),
                            "cinema_ticket": round(low["cinema_ticket"] + r * (high["cinema_ticket"] - low["cinema_ticket"]), 2),
                            "salary_clerk": low.get("salary_clerk")
                        }
                        break

            # Find Era
            cult = next((e for e in eras if e["start_year"] <= yr <= e["end_year"]), eras[-1])

            obj, created = YearSnapshot.objects.update_or_create(
                year=yr,
                defaults={
                    "gold_price": econ["gold_10g"],
                    "usd_inr_rate": econ["usd_inr"],
                    "petrol_price": econ["petrol_litre"],
                    "cinema_ticket_avg": econ["cinema_ticket"],
                    "typical_salary": econ.get("salary_clerk", ""),
                    "era_badge": cult["badge"],
                    "top_movie": cult["top_movie"],
                    "top_song": cult["hit_song"],
                    "lifestyle_summary": cult["lifestyle"],
                }
            )
            if created:
                created_snapshots += 1

        self.stdout.write(self.style.SUCCESS(f"✅ 100-Year Snapshots seeded: 101 years generated ({created_snapshots} new)"))
        self.stdout.write(self.style.SUCCESS("🎉 Database seeding complete!"))