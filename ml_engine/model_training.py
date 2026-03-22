import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
from .feature_engineering import get_all_rfm_data

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'propensity_model.joblib')

def train_model():
    """
    Implement a Supervised Classification algorithm (Random Forest).
    Trains on historical RFM data to predict Propensity Score.
    """
    # 1. Load Data
    df = get_all_rfm_data()
    
    if len(df) < 10:
        print("Not enough data to train the model. Seed the database first.")
        return False
        
    # 2. Prepare Features and Target
    X = df[['recency', 'frequency', 'monetary']]
    y = df['target']
    
    # 3. Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Initialize and Train Model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # 5. Evaluate Model
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    
    print(f"Model trained successfully.")
    print(f"Accuracy: {accuracy:.2f} (Target: >0.85)")
    print(f"Precision: {precision:.2f} (Target: >0.70)")
    
    # 6. Save Model
    joblib.dump(clf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    return True
