import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load your dataset
df = pd.read_csv("Water Footprint Model/crop_water_data.csv")

# Features and target
X = df.drop("WaterFootprint", axis=1)
y = df["WaterFootprint"]

# Define columns
categorical_cols = ["CropType", "Region", "SoilType", "IrrigationMethod"]
numerical_cols = ["Rainfall", "Temperature", "Humidity"]

# Preprocessing
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols),
    ("num", StandardScaler(), numerical_cols)
])

# Define the parameter grid for Grid Search
param_grid = {
    'regressor__n_estimators': [50, 100, 200],
    'regressor__max_depth': [None, 10, 20, 30],
    'regressor__min_samples_split': [2, 5, 10],
    'regressor__min_samples_leaf': [1, 2, 4],
    'regressor__max_features': ['sqrt', 'log2']
}

# Model pipeline
model = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

# Create Grid Search object
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,  # 5-fold cross-validation
    scoring='neg_mean_squared_error',  # We'll use negative MSE as scoring
    n_jobs=-1,  # Use all available CPU cores
    verbose=2  # Print progress
)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Perform Grid Search
print("Starting Grid Search...")
grid_search.fit(X_train, y_train)

# Get the best parameters and best score
print("\nBest Parameters:", grid_search.best_params_)
print("Best Score (negative MSE):", grid_search.best_score_)

# Get the best model
best_model = grid_search.best_estimator_

# Evaluate on test set
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nTest Set Performance:")
print("MSE:", mse)
print("RMSE:", np.sqrt(mse))
print("R² Score:", r2)

# Save the best model
import joblib
joblib.dump(best_model, 'Water Footprint Model/Model/water_footprint_model.pkl')
print("\nModel saved as 'water_footprint_model.pkl'")
