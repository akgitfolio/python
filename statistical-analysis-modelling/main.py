import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import cross_val_score, GridSearchCV


np.random.seed(0)
n_samples = 1000


square_footage = np.random.normal(2000, 500, n_samples)
bedrooms = np.random.randint(1, 6, n_samples)
bathrooms = np.random.randint(1, 4, n_samples)
latitude = np.random.uniform(40.5, 41, n_samples)
longitude = np.random.uniform(-74.3, -73.7, n_samples)
crime_rate = np.random.uniform(0, 1, n_samples)
school_quality = np.random.uniform(0, 10, n_samples)


price = np.exp(np.random.normal(13, 0.5, n_samples))


neighborhoods = np.random.choice(["A", "B", "C"], n_samples)
types = np.random.choice(["apartment", "house"], n_samples)


data = pd.DataFrame(
    {
        "square_footage": square_footage,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "latitude": latitude,
        "longitude": longitude,
        "crime_rate": crime_rate,
        "school_quality": school_quality,
        "price": price,
        "neighborhood": neighborhoods,
        "type": types,
    }
)


data = data.dropna()
data["price"] = np.log1p(data["price"])


center_latitude = np.mean(data["latitude"])
center_longitude = np.mean(data["longitude"])
data["distance_city_center"] = np.sqrt(
    (data["latitude"] - center_latitude) ** 2
    + (data["longitude"] - center_longitude) ** 2
)
data = pd.get_dummies(data, columns=["type", "neighborhood"])


X = data[
    [
        "square_footage",
        "bedrooms",
        "bathrooms",
        "distance_city_center",
        "crime_rate",
        "school_quality",
    ]
]
y = data["price"]


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_scaled)


model = LinearRegression()
model.fit(X_poly, y)


y_pred = model.predict(X_poly)
print(f"R-squared: {model.score(X_poly, y)}")


cv_scores = cross_val_score(model, X_poly, y, cv=5)
print(f"Cross-validated R-squared: {np.mean(cv_scores)}")


ridge = Ridge()
lasso = Lasso()


param_grid = {"alpha": [0.1, 1, 10, 100]}
ridge_cv = GridSearchCV(ridge, param_grid, cv=5)
lasso_cv = GridSearchCV(lasso, param_grid, cv=5)

ridge_cv.fit(X_poly, y)
lasso_cv.fit(X_poly, y)

print(f"Best Ridge alpha: {ridge_cv.best_params_['alpha']}")
print(f"Best Lasso alpha: {lasso_cv.best_params_['alpha']}")


school_latitude = np.random.uniform(40.6, 40.9)
school_longitude = np.random.uniform(-74.2, -73.8)

distances = np.linalg.norm(
    data[["latitude", "longitude"]] - np.array([school_latitude, school_longitude]),
    axis=1,
)
data["distance_school"] = distances


plt.figure(figsize=(10, 6))
plt.scatter(
    data["longitude"], data["latitude"], c=data["price"], cmap="coolwarm", alpha=0.6
)
plt.colorbar(label="Price")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Geospatial Distribution of Housing Prices")
plt.show()
