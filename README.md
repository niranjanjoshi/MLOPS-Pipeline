![](./images/BITS_banner.png)

#  S2-24_AIMLCZG523 - MLOps | BITS Pilani WILP

## Group No. - 120

| Name | StudentID | Contribution % |
|------|-----------|----------------|
| JOSHI NIRANJAN SURYAKANT  | 2023AC05011 | 100% |
| PRATEEK RALHAN | 2023AC05673 | 100% |
| KESHARKAR SURAJ SANJAY | 2023AD05004 | 100% |
| SAURABH SUNIT JOTSHI | 2023AC05565 | 100%  |

---

#### ✅ Problem statement: *"Build, Track, Package, Deploy and Monitor an ML Model using MLOps Best Practices"*

## 🏠 California Housing Price Prediction [![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
### End-to-End MLOps Pipeline

This project demonstrates a fully functional MLOps pipeline using a regression model trained on the California Housing dataset. It includes model training, model tracking, data/model versioning, API based deployments, and performance monitoring.

---

👉 [🎬 Video Demo🔗](https://wilpbitspilaniacin0-my.sharepoint.com/:v:/g/personal/2023ac05011_wilp_bits-pilani_ac_in/EdPJpibOGxhFuMTmqLI3gJQB5k0xFw2tzZB1LUBy0keiMA?e=eCEfB)

👉 [📝 Architecture Summary Document](./docs/summary.pdf)

---

## 🔧 Tech Stack

| Task                | Tool(s)              |
| ------------------- | -------------------- |
| Version Control     | Git + GitHub         |
| Data Versioning     | DVC                  |
| Experiment Tracking | MLflow               |
| API Deployment      | FastAPI + Docker     |
| CI/CD               | GitHub Actions       |
| Monitoring (Logging module)         | Prometheus + Grafana |

---

## 📂 Project Structure

```
.
├── data/
│   └── housing.csv              # California housing dataset
├── models/
│   └── ridge_model.pkl          # Trained model (auto-generated)
├── src/
│   ├── config.yaml              # Model training config
│   ├── model.py                 # Model training and evaluation logic
│   └── utils.py                 # Data loading functions
├── train.py                     # Script to train and log model to MLflow
├── app.py                       # FastAPI app with predict & metrics endpoints
├── Dockerfile
├── docker-compose.yml
├── prometheus/
│   └── prometheus.yml           # Prometheus scrape config
├── .github/
│   └── workflows/ci.yml         # GitHub Actions for CI/CD
├── requirements.txt
└── README.md
```

---

## 🚀 Setup Instructions

### 1. 📦 Clone and Setup Environment

```bash
git clone https://github.com/your-username/housing-mlops.git
cd housing-mlops

# Create virtual env
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. 📁 Prepare Dataset (via DVC)

```bash
dvc init
dvc add data/housing.csv
git add data/housing.csv.dvc .gitignore
git commit -m "Add dataset via DVC"
```

---

## 🧠 Train and Track Model with MLflow

```bash
python train.py
```

- Logs experiment under MLflow's UI.
- Trained model saved in `models/`.
- View MLflow UI locally:

```bash
mlflow ui --port 5000
```

Navigate to [http://localhost:5000](http://localhost:5000)

---

## 🧪 Sample `config.yaml` (src/config.yaml)

```yaml
alpha: 0.5
test_size: 0.2
random_state: 42
```

| MLFLow Experiments tracking | MLFlow Metrics (MSE) |
|------|-----------|
| ![](./images/ml_flow_1st_experiment_logs.png)  | ![](./images/mlflow_mse_results.png) |
| ![](./images/ml_flow_2nd_experiment_logs.png) | ![](./images/mlflow_experiments_tracking.png) |

---

## 📈 Model Serving via FastAPI + Docker

### 1. 🐳 Build & Run Services

```bash
docker-compose up --build
```

* Live public docker image on dockerhub can be found [here.🔗](https://hub.docker.com/r/niranjanjoshi14/housing-api)
* [niranjanjoshi14/housing-api:latest -> manifest digest](https://hub.docker.com/layers/niranjanjoshi14/housing-api/latest/images/sha256-63f94dc9da8f6ba82d4eac995097e238d2d74aa0d903b086bd412b33e681def3)

| Published Image Overview | Published Image - Manifest Digest | Docker desktop - testing local image |
|------|-----------|----------------|
| ![](./images/docker_image_overview.PNG)  | ![](./images/docker_image_mainfest_latest.PNG) | ![](./images/docker_desktop_local_image.png)  |

Services exposed:

- 🧪 API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
- 📊 Prometheus: [http://localhost:9090](http://localhost:9090)
- 📉 Grafana: [http://localhost:3000](http://localhost:3000) (Default login: `admin/admin`)

---

## 📬 Making Predictions

### Example Input (Swagger UI or `curl`):

```json
{
  "MedInc": 8.3252,
  "HouseAge": 41.0,
  "AveRooms": 6.9841,
  "AveBedrms": 1.0238,
  "Population": 322.0,
  "AveOccup": 2.5556,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

### Output:

```json
{
  "prediction": 4.534
}
```

| FastAPI endpoints & config |
|------|
| ![](./images/fastapi_master_config.png) |
| ![](./images/fastapi_config.png) |
| ![](./images/fastapi_prediction_results.png) |

---

## 📊 Monitoring with Prometheus + Grafana

### ✅ FastAPI `/metrics` Endpoint Fix

Ensure your FastAPI code exposes Prometheus metrics like this:

```python
from fastapi import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

### ✅ prometheus.yml (in `prometheus/prometheus.yml`)

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "fastapi-ml-api"
    static_configs:
      - targets: ["api:8000"]
```

Check if Prometheus sees your API at [http://localhost:9090/targets](http://localhost:9090/targets)

| Grafana logs | Grafana logs |
|------|-----------|
| ![](./images/grafana_logs_four.png)  | ![](./images/grafana_logs_three.png) |
| ![](./images/grafana_logs_two.png) | ![](./images/grafana_logs_one.png) |

---

## 🔄 CI/CD with GitHub Actions

In `.github/workflows/ci.yml`, set up a job to:

- Install dependencies
- Run `train.py`
- Validate model behavior
- Optionally: Push Docker image to registry

Example CI step:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: pip install -r requirements.txt
      - run: python train.py
```

![](./images/ci_cd_github_actions.png)

---

## 🛑 Shutdown Instructions

```bash
# Stop all containers
docker-compose down
```

Or if running in foreground, press `Ctrl + C`.

---

## 📎 Notes

- Ensure `models/ridge_model.pkl` exists after training before running Docker.
- Prometheus may throw `Content-Type` errors if `/metrics` returns JSON — fix using `Response(generate_latest(), ...)`.

---

## Citations and References

* DVC Docs: https://dvc.org/doc
* Grafana Docs: https://grafana.com/docs/
* Prometheus Docs: https://prometheus.io/docs/introduction/overview/
* Docker and Dockerhub: https://docs.docker.com/reference/cli/docker/
* Github Actions Docs: https://docs.github.com/en/actions
* MLflow Docs: https://mlflow.org/docs/latest/
* FastAPI Docs: https://fastapi.tiangolo.com/

---

## Appendix:

#### System architecture (Mermaid diagram):

[![](https://mermaid.ink/img/pako:eNqVV4lu4zYQ_RVCQIsWURIrsbOp0C5gy1eKpPXGRoK2Lha0RFtsJFElqex6j3_vDEXLzLGJagShKT2Sw_fm8mcvFgnzQm-diQ9xSqUmi-GyWBbffUd--cbHvBxSTckVLeiG5azQ5Htyw6TiouDF5pXV_b-W3ovLvb_J4eHbL4hRTIckFZWC50exuv95Jd8ObyKyFpLcNyvwab_SIqeaJSTBvTNBE3jzhQzgtCu4Y0aG7J5lorTnLSTl9jS8r6pWG0nLlPSDp-YZDIFPP6DwNqIZBwMKTsm0No1YW9GQc7JmVFeSKWfZCjcFuw9r4uxlSSQKLUXmAOPd6TNesowXjPCCKBkfV5pn6qjcOtgEsJciphmZayHBVnJA8BAtaXy3u5o1GxlFO-wY2zFZFqyAf307byP9i2y-vLpheRC0kQVtHxjKr6pM8zJjpJ9thOQ6zRVyfXntw_qYGzIXkjGfXPMEiLhmGxAAHzsboQh_9K8ukfY134AY023JZEklzZkGSRws6rCzhcxjyUttZND4DGR46HL1TeYsY7FGU364mo9-dHZLmtvOmeTgPp9g0Qe4BvlVrDK-cqAMHQyg5F0FOL0NySADOX0yzugdO_fJTLLDWOQ51y5HRr-B1Xdg9YWD7ciszgM7N0MER40-AgPckL-wbgMq1LYCiVxpubUh8ppfPLNVW3eIgv9jCl45qt3iEvPWHg7sQlYgYQ8-DhSFnzUq--SKaclj-NKXmq9prBW5FJsNS5w1cSPZ7mxQgiltI968cuCo8PzdJdeMDMAYIBuCsQ7O5hDX-FoAq1dk9YqaeIzs3AxD2Ls_u3gUKUNWZmLbpKfX9Xlxi5ZCDYM2tuAdh0agMVUa4dej-YKMiqQUvNAmdI9LyRIea58c5zs5jiUz8eVsYqTbJrTQPCYXRVlpcgNxATneje1hnTcFEC-JyRWHSmNCHFQ8SxxYsodNqxW5yAEUkoJLWvwDf0KlPOge24JzSEseZhDg6sG1ak2sdEMr3bCRbmjnZhgZLyo45OfanX9fKfBRuuIY2y2Fe2GDlrKNgtftwNuNjGgzKUCSlFVqFykhKmYFA97fS_ZvBayo91pomvkESSpid5_VPh5mzTqMMuWAULSJpGsotFAXVboSVCaKhKedTseBmdjSsoqxqiYmVN0KMbKSjKwkIyvJqJFkZOdmGGOCvTiOhk2JbSnDo0UtqR8HT86DwjPhGv2vb2jZUzI2_C8kh2QkVUhmlUoh42OVw54gSmmxYS58tasWUcriO1FBOM22OgWq50xXpYNEri8KiIoMS24JvIBinClIUxGNU5fQsWHcLUL19u7BbB9IJsbApWYVlDKVOqB1k0ObUvpM8I6DDSaVppguwLMemlPrO7b6jq2-Y1vdwBg7ru24sbqP7dwME0PAWkJGsq6EYSDjFI6Te4te94NXNmnpF5OgnT3IwMS4haU7EnkpFPsmFF2iayohjxn4EKRfbBp2Ie0TG3FQBk31dJbWPgI1soCy9RvTH4Q0ZfWAzIR06tfEOMgMm1ilsQLciKzKmQuoJZtYySZWskkTkhM7N8P0SdNrvaG9KN9c3lKOafCCDdi230TN7aa1HNBp77AhSe7joy3NMwdkev5dpG2bJiU0tvoE48uv2xvlrDKFDPuUHAJGYdV70hJPDf27tuK53ylTy__U8j-1_E8b_qd23obbW3AD4yktubwF63Zr0PPADfc3vDVEO90DmLFvaR8nmtsTtw_HugqsHzz23NtTQO0zC-KeyfAG2a1Fsd2K2fFBWO2RvYcl05jZ1MWDXRTt8WeAv677F8Tfw69DCD3n3obx25N6OK2Hbj306uHMiuP53kbyxAshMzDfy8EZKE69z7jX0gMbcrA0hK8JlXdLb1l8hTUlLf4UIt8tk6LapF64ppmCWVUCOWzIKWi0h6BzykhUhfbC7k9mCy_87H30wrPg9CjonXQ73TfnvaB3duJ7W8CcH52_6X31vU_moA7OoFh3Trvn553eadD9-h8RBQ_0?type=png)](https://mermaid.live/edit#pako:eNqVV4lu4zYQ_RVCQIsWURIrsbOp0C5gy1eKpPXGRoK2Lha0RFtsJFElqex6j3_vDEXLzLGJagShKT2Sw_fm8mcvFgnzQm-diQ9xSqUmi-GyWBbffUd--cbHvBxSTckVLeiG5azQ5Htyw6TiouDF5pXV_b-W3ovLvb_J4eHbL4hRTIckFZWC50exuv95Jd8ObyKyFpLcNyvwab_SIqeaJSTBvTNBE3jzhQzgtCu4Y0aG7J5lorTnLSTl9jS8r6pWG0nLlPSDp-YZDIFPP6DwNqIZBwMKTsm0No1YW9GQc7JmVFeSKWfZCjcFuw9r4uxlSSQKLUXmAOPd6TNesowXjPCCKBkfV5pn6qjcOtgEsJciphmZayHBVnJA8BAtaXy3u5o1GxlFO-wY2zFZFqyAf307byP9i2y-vLpheRC0kQVtHxjKr6pM8zJjpJ9thOQ6zRVyfXntw_qYGzIXkjGfXPMEiLhmGxAAHzsboQh_9K8ukfY134AY023JZEklzZkGSRws6rCzhcxjyUttZND4DGR46HL1TeYsY7FGU364mo9-dHZLmtvOmeTgPp9g0Qe4BvlVrDK-cqAMHQyg5F0FOL0NySADOX0yzugdO_fJTLLDWOQ51y5HRr-B1Xdg9YWD7ciszgM7N0MER40-AgPckL-wbgMq1LYCiVxpubUh8ppfPLNVW3eIgv9jCl45qt3iEvPWHg7sQlYgYQ8-DhSFnzUq--SKaclj-NKXmq9prBW5FJsNS5w1cSPZ7mxQgiltI968cuCo8PzdJdeMDMAYIBuCsQ7O5hDX-FoAq1dk9YqaeIzs3AxD2Ls_u3gUKUNWZmLbpKfX9Xlxi5ZCDYM2tuAdh0agMVUa4dej-YKMiqQUvNAmdI9LyRIea58c5zs5jiUz8eVsYqTbJrTQPCYXRVlpcgNxATneje1hnTcFEC-JyRWHSmNCHFQ8SxxYsodNqxW5yAEUkoJLWvwDf0KlPOge24JzSEseZhDg6sG1ak2sdEMr3bCRbmjnZhgZLyo45OfanX9fKfBRuuIY2y2Fe2GDlrKNgtftwNuNjGgzKUCSlFVqFykhKmYFA97fS_ZvBayo91pomvkESSpid5_VPh5mzTqMMuWAULSJpGsotFAXVboSVCaKhKedTseBmdjSsoqxqiYmVN0KMbKSjKwkIyvJqJFkZOdmGGOCvTiOhk2JbSnDo0UtqR8HT86DwjPhGv2vb2jZUzI2_C8kh2QkVUhmlUoh42OVw54gSmmxYS58tasWUcriO1FBOM22OgWq50xXpYNEri8KiIoMS24JvIBinClIUxGNU5fQsWHcLUL19u7BbB9IJsbApWYVlDKVOqB1k0ObUvpM8I6DDSaVppguwLMemlPrO7b6jq2-Y1vdwBg7ru24sbqP7dwME0PAWkJGsq6EYSDjFI6Te4te94NXNmnpF5OgnT3IwMS4haU7EnkpFPsmFF2iayohjxn4EKRfbBp2Ie0TG3FQBk31dJbWPgI1soCy9RvTH4Q0ZfWAzIR06tfEOMgMm1ilsQLciKzKmQuoJZtYySZWskkTkhM7N8P0SdNrvaG9KN9c3lKOafCCDdi230TN7aa1HNBp77AhSe7joy3NMwdkev5dpG2bJiU0tvoE48uv2xvlrDKFDPuUHAJGYdV70hJPDf27tuK53ylTy__U8j-1_E8b_qd23obbW3AD4yktubwF63Zr0PPADfc3vDVEO90DmLFvaR8nmtsTtw_HugqsHzz23NtTQO0zC-KeyfAG2a1Fsd2K2fFBWO2RvYcl05jZ1MWDXRTt8WeAv677F8Tfw69DCD3n3obx25N6OK2Hbj306uHMiuP53kbyxAshMzDfy8EZKE69z7jX0gMbcrA0hK8JlXdLb1l8hTUlLf4UIt8tk6LapF64ppmCWVUCOWzIKWi0h6BzykhUhfbC7k9mCy_87H30wrPg9CjonXQ73TfnvaB3duJ7W8CcH52_6X31vU_moA7OoFh3Trvn553eadD9-h8RBQ_0)
