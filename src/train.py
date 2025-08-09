import yaml
import mlflow
import mlflow.sklearn
import sys
import os
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import utils, model  # keeping your utils/model for data loading

# Load config
with open("src/config.yaml") as f:
    config = yaml.safe_load(f)

# Load data
X_train, X_test, y_train, y_test = utils.load_data(
    test_size=config["test_size"], random_state=config["random_state"]
)

# Set MLflow experiment
mlflow.set_experiment("CaliforniaHousing")

results = []

# --- Train Linear Regression ---
with mlflow.start_run(run_name="LinearRegression") as run_lr:
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    mse_lr = mean_squared_error(y_test, lr.predict(X_test))

    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("mse", mse_lr)
    mlflow.sklearn.log_model(lr, "linear-regression-model")

    results.append(
        {
            "model": lr,
            "mse": mse_lr,
            "name": "LinearRegression",
            "run_id": run_lr.info.run_id,
        }
    )

# --- Train Decision Tree ---
with mlflow.start_run(run_name="DecisionTree") as run_dt:
    dt_params = {
        "max_depth": config.get("max_depth", None),
        "random_state": config["random_state"],
    }
    dt = DecisionTreeRegressor(**dt_params)
    dt.fit(X_train, y_train)
    mse_dt = mean_squared_error(y_test, dt.predict(X_test))

    mlflow.log_param("model_type", "DecisionTree")
    mlflow.log_param("max_depth", dt_params["max_depth"])
    mlflow.log_metric("mse", mse_dt)
    mlflow.sklearn.log_model(dt, "decision-tree-model")

    results.append(
        {
            "model": dt,
            "mse": mse_dt,
            "name": "DecisionTree",
            "run_id": run_dt.info.run_id,
        }
    )

# --- Select Best Model ---
best = min(results, key=lambda x: x["mse"])
print(f"Best model: {best['name']} with MSE={best['mse']}")

# Register the best model in MLflow
mlflow.register_model(
    model_uri=f"runs:/{best['run_id']}/{best['name'].lower().replace(' ', '-')}-model",
    name="CaliforniaHousingBestModel",
)
