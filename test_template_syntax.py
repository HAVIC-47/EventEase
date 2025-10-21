#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.template.loader import get_template
from django.template import TemplateDoesNotExist, TemplateSyntaxError

try:
    template = get_template('venues/venue_detail.html')
    print("✅ Template syntax is valid!")
except TemplateSyntaxError as e:
    print(f"❌ Template syntax error: {e}")
    print(f"Error location: {e.template_debug}")
except TemplateDoesNotExist as e:
    print(f"❌ Template not found: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")