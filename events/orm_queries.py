from events.models import Category, Event
from decimal import Decimal

published_events = Event.objects.filter(is_published=True).order_by('date')
for event in published_events:
    print(f"{event.title} - {event.date}")

large_events = Event.objects.filter(capacity__gte=50)
for event in large_events:
    print(f"{event.title} - {event.capacity} miejsc")

free_events_count = Event.objects.filter(price=Decimal('0.00')).count()
print(f"Ilość darmowych wydarzeń: {free_events_count}")

event = Event.objects.filter(is_published=True).first()
if event:
    event.is_published = False
    event.save()
    print(f"Zaktualizowano wydarzenie '{event.title}': is_published = {event.is_published}")