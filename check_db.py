import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecole.settings')
import django
django.setup()
from playground.models import Formati

# Check all formations
formations = Formati.objects.all()
print(f'Total formations: {formations.count()}')
print(f'Published formations: {formations.filter(publish=True).count()}')
print()

for f in formations:
    print(f'{f.name}')
    print(f'  Type: {f.formation_type}')
    print(f'  Publish: {f.publish}')
    print()
