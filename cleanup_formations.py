import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecole.settings')
import django
django.setup()
from playground.models import Formati

# Delete Alexandre Leroy (should not be a formation)
deleted = Formati.objects.filter(name='Alexandre Leroy').delete()
print(f'Deleted Alexandre Leroy: {deleted}')

# Keep only unique formations by name, delete duplicates
print('\nCleaning duplicates...')
seen = set()
for f in Formati.objects.all():
    if f.name in seen:
        print(f'  Deleting duplicate: {f.name}')
        f.delete()
    else:
        seen.add(f.name)

# Show what's left
print('\nRemaining formations:')
for f in Formati.objects.all():
    print(f'  - {f.name} ({f.formation_type}) - Published: {f.publish}')
