>>> import io
>>> from events.models import Event
>>> from events.serializers import EventSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> event = Event.objects.first()
>>> serializer = EventSerializer(event)
>>> print(serializer.data)
{'id': 2, 'title': 'warsztat 1', 'slug': 'warsztat-1', 'category_id': 3, 'organizer_id': 1, 'description': 'fajny', 'location': 'wszędzie', 'date': '2026-10-13T12:14:08Z', 'capacity': 2, 'price': '50.00', 'is_published': True, 'created_at': '2026-10-13T12:14:16.018584Z'}
>>> json_bytes = JSONRenderer().render(serializer.data)
>>> print(json_bytes)
b'{"id":2,"title":"warsztat 1","slug":"warsztat-1","category_id":3,"organizer_id":1,"description":"fajny","location":"wsz\xc4\x99dzie","date":"2026-10-13T12:14:08Z","capacity":2,"price":"50.00","is_published":true,"created_at":"2026-10-13T12:14:16.018584Z"}'
>>> from rest_framework.parsers import JSONParser
>>> from django.contrib.auth.models import User
>>> from events.models import Category
>>> stream = io.BytesIO(json_bytes)
>>> data = JSONParser().parse(stream)
>>> data['title'] = "Nowe Warsztaty Pythona"
>>> data['slug'] = "nowe-warsztaty-pythona"
>>> deserializer = EventSerializer(data=data)
>>> if deserializer.is_valid():
...     print("Dane są poprawne!")
...     print(deserializer.validated_data)
...     # Zapis nowego rekordu do bazy danych
...     new_event = deserializer.save()
...     print(f"Utworzono wydarzenie o id={new_event.id}")
... else:
...     print("Błędy walidacji:", deserializer.errors)
... 
Dane są poprawne!
{'title': 'Nowe Warsztaty Pythona', 'slug': 'nowe-warsztaty-pythona', 'category': <Category: Warsztaty>, 'organizer': <User: gilo>, 'description': 'fajny', 'location': 'wszędzie', 'date': datetime.datetime(2026, 10, 13, 12, 14, 8, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'capacity': 2, 'price': Decimal('50.00'), 'is_published': True}
Utworzono wydarzenie o id=5
>>> invalid_data = {
...     'title': '',
...     'capacity': -5
... }
>>> bad_serializer = EventSerializer(data=invalid_data)
>>> print("Czy poprawne?", bad_serializer.is_valid())  # False
Czy poprawne? False
>>> print("Błędy:", bad_serializer.errors)
Błędy: {'title': [ErrorDetail(string='This field may not be blank.', code='blank')], 'slug': [ErrorDetail(string='This field is required.', code='required')], 'category_id': [ErrorDetail(string='This field is required.', code='required')], 'organizer_id': [ErrorDetail(string='This field is required.', code='required')], 'description': [ErrorDetail(string='This field is required.', code='required')], 'location': [ErrorDetail(string='This field is required.', code='required')], 'date': [ErrorDetail(string='This field is required.', code='required')], 'capacity': [ErrorDetail(string='Ensure this value is greater than or equal to 1.', code='min_value')]}