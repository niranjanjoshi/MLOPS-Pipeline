import yaml
import mlflow
import mlflow.sklearn
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import utils, model

with open("src/config.yaml") as f:
    config = yaml.safe_load(f)

X_train, X_test, y_train, y_test = utils.load_data(
    test_size=config["test_size"], random_state=config["random_state"]
)

mlflow.set_experiment("CaliforniaHousing")

with mlflow.start_run():
    reg = model.train_model(X_train, y_train, alpha=config["alpha"])
    mse = model.evaluate_model(reg, X_test, y_test)
    model.save_model(reg)

    mlflow.log_param("alpha", config["alpha"])
    mlflow.log_metric("mse", mse)
    mlflow.sklearn.log_model(reg, "ridge-model")
