from rest_framework import serializers
from .models import YearSnapshot, HistoricalEvents, Luminary


class HistoricalEventSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = HistoricalEvents
        fields = ['id', 'date', 'title', 'description', 'category', 'category_display']


class LuminarySerializer(serializers.ModelSerializer):
    field_display = serializers.CharField(source='get_field_display', read_only=True)

    class Meta:
        model = Luminary
        fields = ['id', 'name', 'dob', 'field', 'field_display', 'bio']


class YearSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearSnapshot
        fields = [
            'year', 'gold_price', 'petrol_price', 'usd_inr_rate',
            'cinema_ticket_avg', 'typical_salary', 'era_badge', 'top_movie',
            'top_song', 'lifestyle_summary'
        ]