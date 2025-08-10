import yaml
import mlflow
import mlflow.sklearn
import sys
import os
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import utils

mlflow.set_tracking_uri("http://mlflow-server:5555")

with open("src/config.yaml") as f:
    config = yaml.safe_load(f)

X_train, X_test, y_train, y_test = utils.load_data(
    test_size=config["test_size"], random_state=config["random_state"]
)

mlflow.set_experiment("CaliforniaHousing")

best_model_name = None
best_mse = float("inf")
best_run_id = None
best_artifact_path = None

# Train Linear Regression
with mlflow.start_run() as lr_run:
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    mse_lr = mean_squared_error(y_test, lr.predict(X_test))

    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("mse", mse_lr)
    mlflow.sklearn.log_model(lr, "linear-model")

    if mse_lr < best_mse:
        best_mse = mse_lr
        best_model_name = "LinearRegression"
        best_run_id = lr_run.info.run_id
        best_artifact_path = "linear-model"

# Train Decision Tree
with mlflow.start_run() as dt_run:
    dt = DecisionTreeRegressor(random_state=config["random_state"])
    dt.fit(X_train, y_train)
    mse_dt = mean_squared_error(y_test, dt.predict(X_test))

    mlflow.log_param("model_type", "DecisionTree")
    mlflow.log_metric("mse", mse_dt)
    mlflow.sklearn.log_model(dt, "decisiontree-model")

    if mse_dt < best_mse:
        best_mse = mse_dt
        best_model_name = "DecisionTree"
        best_run_id = dt_run.info.run_id
        best_artifact_path = "decisiontree-model"

print(f"Best model: {best_model_name} with MSE={best_mse}")

# Register best model
mlflow.register_model(
    model_uri=f"runs:/{best_run_id}/{best_artifact_path}", name="BestHousingModel"
)
