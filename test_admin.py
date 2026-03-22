import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdms_config.settings'); django.setup();
from django.template.loader import render_to_string
from django.contrib.auth.models import User
admins = User.objects.filter(is_staff=True)
html = render_to_string('admin_user_dashboard.html', {'admins': admins})
for line in html.split('\n'):
    if '{' in line or 'odumbedavis' in line:
        print(line.strip())
