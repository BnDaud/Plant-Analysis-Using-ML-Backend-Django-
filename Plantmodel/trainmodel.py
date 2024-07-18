import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
import joblib , os
# Load the dataset
df = pd.read_excel(os.path.join(os.getcwd(), "Plantmodel","realistic_plant1.xlsx"))

# Display the first few rows of the dataset
print(df.head())



# Separate features and target
X = df.drop("Plant Type", axis=1)
y = df["Plant Type"]

# Encode the target variable
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Preprocess the features
numeric_features = ["Sunlight (hours/day)", "Wind (m/s)", "pH", "Temperature (°C)", "Water (mm/month)", "Carbon Dioxide (ppm)", "Minerals (%)"]
categorical_features = ["Soil Type"]

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)




# Create a pipeline with preprocessing and the model
rf_model = make_pipeline(preprocessor, RandomForestClassifier(n_estimators=100, random_state=42 , oob_score = True))

# Train the model
rf_model.fit(X_train, y_train)

# Predict and evaluate
y_pred_rf = rf_model.predict(X_test)
print("Random Forest Classification Report:\n", classification_report(y_test, y_pred_rf, target_names=label_encoder.classes_))
print(X_test)

version = joblib.__version__
joblib.dump(rf_model,os.path.join(os.getcwd() , "Plantmodel","model_new{version}.pkl".format(version= version)))