import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

def train_view_predictor():
    df = pd.read_csv('Cleaned_Data/youtube_cleaned.csv')
    
    # Dynamic check: Fallback to 'Hour' if 'publish_hour' isn't generated yet
    if 'publish_hour' in df.columns:
        hour_feature = 'publish_hour'
    elif 'Hour' in df.columns:
        hour_feature = 'Hour'
    else:
        raise KeyError("Could not find an hour column ('publish_hour' or 'Hour') in the CSV. Please run data_cleaning.py first!")

    print(f"Using '{hour_feature}' as the time feature.")

    # Define system features and predictable targets
    features = ['likes', 'comment_count', hour_feature, 'category', 'country']
    target = 'views'
    
    X = df[features]
    y = df[target]
    
    # Encode categorical text values into mathematical matrices safely
    # added sparse_output=False for better compatibility with modern scikit-learn
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['category', 'country'])
        ], remainder='passthrough'
    )
    
    X_processed = preprocessor.fit_transform(X)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    
    # Initialize and Train Model
    print("Training Predictive View Engine (Random Forest)...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print("\n--- Model Performance Evaluation ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f} Views")
    print(f"R² Fit Score: {r2*100:.2f}%")
    
    # Save a baseline of predictions vs actuals for Power BI consumption
    comparison_df = pd.DataFrame({'Actual_Views': y_test, 'Predicted_Views': predictions})
    comparison_df.to_csv('Cleaned_Data/predictions_eval.csv', index=False)
    print("Prediction mapping dataset written to 'Cleaned_Data/predictions_eval.csv'")

if __name__ == "__main__":
    train_view_predictor()