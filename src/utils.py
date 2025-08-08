from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split


def load_data(test_size=0.2, random_state=42):
    data = fetch_california_housing(as_frame=True)
    X = data.data
    y = data.target
    df = data.frame
    df["MedHouseVal"] = data.target
    df.to_csv("data/housing.csv", index=False)
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
