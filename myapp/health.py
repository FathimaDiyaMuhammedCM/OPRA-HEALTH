import pandas as pd
import joblib
import numpy as np

np.random.seed(42)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Load and preprocess the data
df = pd.read_excel('synthetic_health_dataset_with_diet.xlsx')

# Fill NaNs with 'None'
df['medical_conditions'] = df['medical_conditions'].fillna('None')

# Parse blood_pressure into systolic and diastolic
df[['systolic_bp', 'diastolic_bp']] = df['blood_pressure'].str.split('/', expand=True).astype(int)
df.drop('blood_pressure', axis=1, inplace=True)

# Add synthetic diet columns (since not present in original dataset)
meals = ['Oatmeal with fruits', 'Salad with chicken', 'Grilled fish', 'Vegetable soup', 'Yogurt parfait', 'Quinoa bowl',
         'Steamed veggies', 'Lentil curry']
df['morning_diet'] = np.random.choice(meals, size=len(df))
df['noon_diet'] = np.random.choice(meals, size=len(df))
df['evening_diet'] = np.random.choice(meals, size=len(df))
df['night_diet'] = np.random.choice(meals, size=len(df))

# Define features and targets
# Features: All columns except user_id, name, and the 4 diet targets
feature_cols = [col for col in df.columns if
                col not in ['user_id', 'name', 'morning_diet', 'noon_diet', 'evening_diet', 'night_diet']]
target_cols = ['morning_diet', 'noon_diet', 'evening_diet', 'night_diet']

X = df[feature_cols]
y = df[target_cols]

# Identify categorical and numerical features
cat_features = X.select_dtypes(include=['object']).columns.tolist()
num_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Label encode the targets
le_dict = {}
for col in target_cols:
    le = LabelEncoder()
    y[col] = le.fit_transform(y[col])
    le_dict[col] = le

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
    ])

# Multi-output RandomForest classifier pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42)))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Evaluate (optional - since synthetic, expect low accuracy)
y_pred = model.predict(X_test)
for i, col in enumerate(target_cols):
    print(f"\n{col}:")
    print(classification_report(y_test.iloc[:, i], y_pred[:, i], target_names=le_dict[col].classes_))

# Save the model and label encoders
joblib.dump(model, 'diet_rf_predictor.pkl')
joblib.dump(le_dict, 'diet_rf_label_encoders.pkl')
joblib.dump({'feature_cols': feature_cols, 'target_cols': target_cols}, 'diet_rf_metadata.pkl')
print("\nRandomForest model for diet prediction trained and saved!")

# Prediction Function
# Load the saved model and encoders (run after training)
model = joblib.load('diet_rf_predictor.pkl')
le_dict = joblib.load('diet_rf_label_encoders.pkl')
metadata = joblib.load('diet_rf_metadata.pkl')
feature_cols = metadata['feature_cols']
target_cols = metadata['target_cols']


def predict_diet_plan_rf(input_data):
    """
    Predict the daily diet plan using RandomForest.

    Args:
    input_data (dict): Dictionary with keys matching feature_cols.
                       For blood pressure, provide 'systolic_bp' and 'diastolic_bp' as integers.

    Returns:
    dict: Predicted values for the 4 diet columns.
    """
    # Create DataFrame from input
    input_df = pd.DataFrame([input_data])

    # Ensure all feature columns are present
    for col in feature_cols:
        if col not in input_df.columns:
            if col in cat_features:
                input_df[col] = 'None'
            else:
                input_df[col] = 0  # Default for numeric

    # Predict encoded values
    pred_encoded = model.predict(input_df)[0]

    # Inverse transform to get original labels
    predictions = {}
    for i, col in enumerate(target_cols):
        predictions[col] = le_dict[col].inverse_transform([int(pred_encoded[i])])[0]

    return predictions


# Example Usage:
example_input = {
    'age': 38,
    'gender': 'Male',
    'height': 193,
    'weight': 66,
    'target_weight': 67,
    'activity_level': 'Low',
    'dietary_preference': 'Vegetarian',
    'smoking_status': 'Non-Smoker',
    'alcohol_consumption': 'Never',
    'average_sleep_hours': 8.6,
    'daily_water_intake_liters': 1.1,
    'stress_level': 'Low',
    'calories_intake': 1572,
    'protein_intake_g': 116,
    'carbs_intake_g': 206,
    'fat_intake_g': 89,
    'systolic_bp': 100,
    'diastolic_bp': 68,
    'cholesterol_level_mg_dl': 159,
    'blood_sugar_mg_dl': 98,
    'medical_conditions': 'Heart Disease',
    'allergies': 'Lactose',
    'favorite_foods': 'Fruits',
    'disliked_foods': 'None',
    'current_medications': 'None'
}

# Make prediction
prediction = predict_diet_plan_rf(example_input)
print("\nPredicted Health Plan (RandomForest):")
for key, value in prediction.items():
    print(f"{key}: {value}")