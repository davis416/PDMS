import os
import django
from datetime import datetime
from django.db.models import Sum, Count, Max
from django.utils import timezone

def extract_rfm(donor_id):
    """
    Extract Recency, Frequency, and Monetary (RFM) values
    from the Donation table for a given donor.
    """
    from core_app.models import Donation, Donor
    
    donor = Donor.objects.get(pk=donor_id)
    donations = Donation.objects.filter(DonorID=donor, Status='COMPLETED')
    
    if not donations.exists():
        return {
            'donor_id': donor_id,
            'recency': 9999, # Large number if no donations
            'frequency': 0,
            'monetary': 0.0
        }
        
    # Calculate Recency (days since last donation)
    last_donation_date = donations.aggregate(Max('Date'))['Date__max']
    recency = (timezone.now() - last_donation_date).days
    
    # Calculate Frequency (total number of donations)
    frequency = donations.count()
    
    # Calculate Monetary (total amount donated)
    monetary = float(donations.aggregate(Sum('Amount'))['Amount__sum'] or 0.0)
    
    return {
        'donor_id': donor_id,
        'recency': recency,
        'frequency': frequency,
        'monetary': monetary
    }

def get_all_rfm_data():
    """
    Extract RFM data for all donors. Used for model training.
    """
    from core_app.models import Donor
    
    data = []
    donors = Donor.objects.all()
    for donor in donors:
        # Generate a label (1 if they donated in the last 6 months, 0 otherwise) as a proxy
        # for whether they are likely to donate in the next campaign (propensity).
        rfm = extract_rfm(donor.DonorID)
        
        # We need a target variable (Y). If we pretend anyone with Recency < 180 is a "1" (will donate),
        # but to make the model learn something, we will use a synthetic rule just for the stub.
        # Let's say high frequency (>2) or high monetary (>500) makes them likely.
        # This is purely for the stub to have a classification target.
        target = 1 if rfm['frequency'] > 2 or rfm['monetary'] > 500 else 0
        
        rfm['target'] = target
        data.append(rfm)
        
    import pandas as pd
    return pd.DataFrame(data)
