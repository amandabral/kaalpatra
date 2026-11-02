from django.db import models

# Create your models here.
class YearSnapshot(models.Model):
    """ Annual economic, cultural, and political markers."""
    year = models.PositiveIntegerField(unique=True, db_index=True)
    gold_price =  models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    petrol_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    usd_inr_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    cinema_ticket_avg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    typical_salary =  models.CharField(max_length=100, blank=True)
    era_badge = models.CharField(max_length=150, blank=True)
    top_movie = models.CharField(max_length=250, blank=True)
    top_song = models.CharField(max_length=100, blank=True)
    lifestyle_summary = models.TextField(blank=True)

    class Meta:
        ordering = ['year']

    def __str__(self) -> str:
        return f"{self.year} - {self.era_badge}"

class HistoricalEvents(models.Model):
    """ Nation defining events on calender date"""

    CATEGORY_CHOICES = [
        ('POLITICS', 'Politics & Freedom'),
        ('SPORTS', 'Sports and Games'),
        ('SCIENCE', 'Science and Space'),
        ('ARTS', 'Cinema & Arts'),
        ('WAR_PEACE', 'Defence & Security'),
        ('GENERAL', 'General Headline')
    ]

    date = models.DateField(db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return f"{self.date}- {self.title}"

class Luminary(models.Model):
    """ Notable Indian Personalities for birthday twin matches"""
    FIELD_CHOICES = [
        ('FREEDOM_FIGHTER', 'Freedom Fighter / Leader'),
        ('SCIENCE', 'Scientist / Innovator'),
        ('ARTS', 'Cinema / Music / Dance'),
        ('SPORTS', 'Sports Icon'),
        ('LITERATURE', 'Author / Poet'),
        ('PHILOSOPHY', 'Philosopher / Thinker'),
        ('POLITICS', 'Statesman / Politics'),
    ]

    name = models.CharField(max_length=150)
    dob = models.DateField(db_index=True)
    birth_month = models.PositiveSmallIntegerField(db_index=True)
    birth_day = models.PositiveSmallIntegerField(db_index=True)
    field = models.CharField(max_length=30, choices = FIELD_CHOICES, default='ARTS')
    bio = models.TextField()

    def save(self, *args, **kwargs):
        if self.dob:
            self.birth_month = self.dob.month
            self.birth_day = self.dob.day
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Luminaries"
        indexes = [
            models.Index(fields=['birth_month','birth_day'])
        ]

    def __str__(self) -> str:
        return f"{self.name}({self.dob})"