import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib , os
# Sample data dictionary (you can replace this with your actual data)

df = pd.read_excel(os.path.join(os.getcwd(), "Plantmodel","realistic_plant1.xlsx"))

# Encode categorical features and target
df_encoded = pd.get_dummies(df, columns=["Soil Type"])
X = df_encoded.drop(columns=["Plant Type"])
y = df["Plant Type"]

#......Split the data......
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#......Train the Random Forest model......
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

#......Save the Model......
version = joblib.__version__
joblib.dump(rf,os.path.join(os.getcwd() , "Plantmodel","model_new{version}.pkl".format(version= version)))
# Get prediction probabilities for the test set

if __name__ == "__main__":
    probs = rf.predict_proba(X_test)

    # Get the class labels
    class_labels = rf.classes_

    # Find the top 5 predictions for each sample in the test set
    top_5_predictions = []
    str_ = " "
    for prob in probs:
        top_5_indices = np.argsort(prob)[-5:][::-1]
        top_5_plants = class_labels[top_5_indices]
        top_5_predictions.append(top_5_plants)
        str_ +=top_5_plants + " "


    print(top_5_predictions[0])
    # Display the first few samples of top 5 predictions
    for i, top_5 in enumerate(top_5_predictions[:5]):
        print(f"Sample {i+1}: {top_5}")
