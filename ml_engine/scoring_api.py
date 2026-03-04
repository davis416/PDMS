import os
import joblib
import pandas as pd
from django.http import JsonResponse
from core_app.models import Donor
from .feature_engineering import extract_rfm

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'propensity_model.joblib')

def predict_propensity_score(donor_id):
    """
    Executes the trained model to generate 
    a Propensity Score (0-1) for a given donor.
    Updates the database with the new score.
    """
    # 1. Extract features
    rfm_data = extract_rfm(donor_id)
    features = pd.DataFrame([{
        'recency': rfm_data['recency'],
        'frequency': rfm_data['frequency'],
        'monetary': rfm_data['monetary']
    }])
    
    # 2. Load trained model
    if not os.path.exists(MODEL_PATH):
        print("Model file not found. Please train the model first.")
        return 0.0
        
    model = joblib.load(MODEL_PATH)
    
    # 3. Predict probability (propensity score)
    # predict_proba returns [[prob_0, prob_1]]
    score = model.predict_proba(features)[0][1]
    
    # 4. Save score back to Donor model
    # Using specific field update to minimize transaction blocking
    Donor.objects.filter(pk=donor_id).update(Propensity_Score=score)
    
    return score

def api_get_propensity_score(request, donor_id):
    """
    HTTP endpoint wrapper for the scoring API.
    """
    score = predict_propensity_score(donor_id)
    return JsonResponse({
        'donor_id': donor_id,
        'propensity_score': score
    })
    
def score_all_donors():
    """
    Utility function to run scoring on all donors.
    """
    donors = Donor.objects.all()
    for donor in donors:
        predict_propensity_score(donor.DonorID)
    print("All donors scored successfully.")
