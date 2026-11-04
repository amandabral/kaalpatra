from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import YearSnapshot, HistoricalEvents, Luminary
from .serializers import YearSnapshotSerializer, HistoricalEventSerializer, LuminarySerializer
from .services import TimeCapsuleService


class TimeCapsuleAPIView(APIView):
    """
    Returns complete time capsule data for an Indian birth date.
    Query param: ?date=YYYY-MM-DD
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TimeCapsuleService()

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response(
                {"error": "Query parameter 'date' (YYYY-MM-DD) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Please use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (1925 <= target_date.year <= 2026):
            return Response(
                {"error": "KaalPatra currently supports birth years between 1925 and 2026."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Calendar metadata
        days_ago = (datetime.now().date() - target_date).days
        calendar_info = {
            "date": target_date.strftime("%Y-%m-%d"),
            "formatted_date": target_date.strftime("%B %d, %Y"),
            "day_of_week": target_date.strftime("%A"),
            "days_ago": days_ago,
            "moon_phase": self.service.calculate_moon_phase(target_date)
        }

        # 2. Leadership lookup
        leadership_info = self.service.get_leadership(target_date)

        # 3. Year Snapshot (Economics + Culture)
        year_snapshot = YearSnapshot.objects.filter(year=target_date.year).first()
        snapshot_data = YearSnapshotSerializer(year_snapshot).data if year_snapshot else None

        # 4. Exact Dated Events
        exact_events = HistoricalEvents.objects.filter(date=target_date)
        events_data = HistoricalEventSerializer(exact_events, many=True).data

        # 5. Luminaries (Exact Twins + Calendar Twins)
        exact_twins = Luminary.objects.filter(dob=target_date)
        calendar_twins = Luminary.objects.filter(
            birth_month=target_date.month,
            birth_day=target_date.day
        ).exclude(dob=target_date)

        return Response({
            "calendar": calendar_info,
            "leadership": leadership_info,
            "annual_snapshot": snapshot_data,
            "exact_events": events_data,
            "exact_twins": LuminarySerializer(exact_twins, many=True).data,
            "calendar_twins": LuminarySerializer(calendar_twins, many=True).data
        })