from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import joblib

def train_model(X_train, y_train, alpha):
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    return mean_squared_error(y_test, preds)

def save_model(model, path="models/ridge_model.pkl"):
    joblib.dump(model, path)

def load_model(path="models/ridge_model.pkl"):
    return joblib.load(path)