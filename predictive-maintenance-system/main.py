import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import argparse


data = pd.read_csv("equipment_data.csv")


data = data.dropna()


scaler = StandardScaler()
X = data.drop("failure", axis=1)
X_scaled = scaler.fit_transform(X)
y = data["failure"]


X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))


param_grid = {
    "n_estimators": [50, 100, 200],
    "max_features": ["auto", "sqrt", "log2"],
    "max_depth": [4, 6, 8, 10, 12],
    "criterion": ["gini", "entropy"],
}
grid_search = GridSearchCV(
    estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2
)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_


y_pred_best = best_model.predict(X_test)
best_accuracy = accuracy_score(y_test, y_pred_best)
print("Best Model Accuracy:", best_accuracy)
print("Best Model Classification Report:\n", classification_report(y_test, y_pred_best))
print("Best Model Confusion Matrix:\n", confusion_matrix(y_test, y_pred_best))


joblib.dump(best_model, "best_model.pkl")
joblib.dump(scaler, "scaler.pkl")


def predict_failure(new_data):
    model = joblib.load("best_model.pkl")
    scaler = joblib.load("scaler.pkl")
    new_data_scaled = scaler.transform(new_data)
    predictions = model.predict(new_data_scaled)
    return predictions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict equipment failure")
    parser.add_argument(
        "--data", type=str, required=True, help="Path to the new data CSV file"
    )
    args = parser.parse_args()

    new_data = pd.read_csv(args.data)
    predictions = predict_failure(new_data)
    print("Predictions:", predictions)
