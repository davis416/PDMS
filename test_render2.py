import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdms_config.settings'); django.setup();
from django.template import Template, Context
try:
    print('T1:', Template('{{ val|default:"0.00"|floatformat:2 }}').render(Context({'val': 5})))
    print('T2:', Template('{{ val|default:"0.00"|floatformat:2 }}').render(Context({'val': None})))
    print('T3:', Template('{{ campaign.collected|default:"0.00"|floatformat:2 }}').render(Context({'campaign': {'collected': None}})))
except Exception as e:
    print('ERROR:', e)
