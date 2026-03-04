import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdms_config.settings'); django.setup();
from django.template.loader import render_to_string
from core_app.models import Campaign
from django.db import models
campaigns = Campaign.objects.annotate(collected=models.Sum('donations__Amount')).all()
html = render_to_string('campaign_dashboard.html', {'campaigns': campaigns})
for line in html.split('\n'):
    if 'campaign.Name' in line or '{' in line:
        print(line.strip())
