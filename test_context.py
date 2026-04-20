import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecole.settings')
import django
django.setup()

from django.test import RequestFactory
from playground.views import HOMEView

# Create a mock request
factory = RequestFactory()
request = factory.get('/')

# Create the view and get context
view = HOMEView()
view.request = request
context = view.get_context_data()

print("Context passed to template:")
print(f"  formatis: {context.get('formatis')}")
print(f"  formatis count: {context.get('formatis').count() if context.get('formatis') else 'N/A'}")
print(f"  news_list: {context.get('news_list')}")
print(f"  contact_form: {context.get('contact_form')}")
print()

if context.get('formatis'):
    print("Formations in context:")
    for f in context.get('formatis'):
        print(f"  - {f.name} ({f.formation_type})")
else:
    print("No formatis in context!")
