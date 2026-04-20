import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecole.settings')
import django
django.setup()
from playground.models import Formati

formations = Formati.objects.all()
print('All formations:')
for f in formations:
    print(f'  - {f.name}: formation_type="{f.formation_type}"')

# Check unique formation_type values
types = Formati.objects.values_list('formation_type', flat=True).distinct()
print('\nUnique formation types:')
for t in types:
    print(f'  - "{t}"')
