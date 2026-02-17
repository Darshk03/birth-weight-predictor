# Birth Weight Predictor

A production-minded Flask application that predicts newborn birth weight using a scikit-learn model — full pipeline, API, tests, and cloud deployment.

Live demo: https://birth-weight-predictor-dt90.onrender.com

---

## Project Snapshot (for HR / Recruiters)
- Role demonstrated: Backend & ML Engineer — built end-to-end product from data to deployed API.
- Business value: fast, explainable birth-weight estimates for triage or analytic workflows.
- Production focus: type-safe request handling, pandas-based pipeline, model serialization, API docs, tests, and cloud deployment (Render + Gunicorn). 

---

## Tech Stack
- Python 3.10+
- Flask (app & UI)
- Flask-RESTx (recommended for OpenAPI/Swagger)
- pandas, NumPy
- scikit-learn (model training and inference)
- pickle (model artifact serialization)
- pytest (unit/integration tests)
- Postman & Swagger for API testing & docs
- Gunicorn (WSGI server for production)
- Nginx (recommended reverse proxy / TLS termination)
- Render (deployed live), Heroku (alternative), GitHub (repo)
- Virtual environment: `venv`, `requirements.txt`

---

## Purpose & Highlights
- Convert raw input (form or JSON) to a cleaned `pandas.DataFrame` and produce a robust birth-weight prediction.
- Clear separation: request validation → data cleaning (`get_cleaned_data`) → model inference → formatted response.
- Deployment-ready: Gunicorn WSGI command included, runs behind Nginx or Render's platform.

---

## Endpoints (current & recommended)
- `GET /` — renders `index.html` (interactive UI).
- `POST /predict` — accepts form-data (current) and can accept JSON; returns predicted birth weight.

Recommended extensions for full CRUD and production:
- `POST /datasets` — upload dataset (Create)
- `GET /predictions/{id}` — read saved predictions (Read)
- `PUT /models/{version}` — update / replace model (Update)
- `DELETE /models/{version}` — delete model versions (Delete)

Response examples (recommended JSON format):

Success (200):
```
{
  "prediction": 3.25,
  "units": "kg",
  "input": {"gestation":39.0, "parity":0, "age":28, "height":165.0, "weight":60.0, "smoke":0}
}
```

Validation error (400):
```
{ "error": "missing field: weight" }
```

---

## Request Handling & File Handling
- The app accepts form fields (current `app.py`) and should also accept JSON (`request.get_json()`); `get_cleaned_data` casts fields to `float`/`int` and returns a dict converted to a one-row `pandas.DataFrame`.
- Model artifact `model.pkl` is loaded as a binary file using `open('model.pkl','rb')` and `pickle.load()`.
- For file uploads (datasets/models): handle with `request.files`, save to a secure artifact directory, validate MIME/type, scan size limits, and sanitize filenames.

Security note: do not unpickle untrusted inputs. For multi-tenant production, use signed model artifacts or an artifact store.

---

## Dataset: columns & EDA summary
Features used by the model (input):
- `gestation` — pregnancy length (weeks) — continuous
- `parity` — number of prior births — integer
- `age` — mother's age (years) — integer
- `height` — mother's height (cm) — continuous
- `weight` — mother's weight (kg) — continuous
- `smoke` — binary (0/1) maternal smoking indicator — categorical/binary

Target:
- `birth_weight` — continuous target (kg or grams depending on dataset).

EDA performed (in repo):
- Distribution histograms for all continuous variables
- Correlation heatmap identifying top predictors of birth weight
- Missing-value handling strategy and outlier treatment used during training

Modeling summary:
- Algorithm: scikit-learn regression model (see training notebook/script in repo)
- Serialization: `model.pkl` via `pickle`

Explainability:
- Produce feature importance / coefficients to justify predictions for stakeholders.

---

## Authentication & Authorization (API Security)
Recommended patterns implemented or ready to add:
- Authentication: JWT Bearer tokens (stateless) — issued by an auth service.
- Authorization: Role-based access (e.g., `admin` for model upload/retrain; `user` for prediction).
- Transport security: HTTPS enforced at reverse proxy (Nginx / Render TLS).
- Additional: rate limiting, input validation, sanitization, logging, secret management (no secrets in repo).

Supported auth types you can add:
- API keys (simple), JWT (recommended), OAuth2 (enterprise integration)

---

## Testing & Documentation
- Unit tests: `pytest` for `get_cleaned_data`, edge cases, and model interface.
- Integration tests: test `POST /predict` for status codes and JSON schema.
- Postman collection: manual API tests and pre-configured scenarios for demo.
- Swagger/OpenAPI: generate using `Flask-RESTx` decorators to provide interactive docs.

Example test run:
```bash
pip install -r requirements.txt
pytest
```

---

## Deployment (Local → Production)
Local development (Windows):
```powershell
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Production (Gunicorn + Nginx):
```bash
# Gunicorn example
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# On Render: configure start command to run Gunicorn similarly
```

Heroku (alternative): add `Procfile`:
```
web: gunicorn app:app
```

Notes: run the WSGI server behind Nginx to handle TLS, static files, and buffering.

---

## CI / CD & Observability
- Add GitHub Actions to run `pytest` and lint on push/PR.
- On successful tests, push artifacts or trigger Render deploys.
- Add health-check endpoints and basic metrics/logging for monitoring.

---

## Quick API example (cURL)
```bash
curl -X POST "https://birth-weight-predictor-dt90.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"gestation":39.0,"parity":0,"age":28,"height":165.0,"weight":60.0,"smoke":0}'
```

---

## Where to look in this repo
- Main app: `app.py` (request handling, `get_cleaned_data`, and `/predict` flow)
- Model artifact: `model.pkl`
- Templates: `templates/index.html` (UI)
- Tests: `tests/` (if present) — run via `pytest`

---

## Live Demo & Source
- Live: https://birth-weight-predictor-dt90.onrender.com
- Repo: https://github.com/Darshk03/birth-weight-predictor

---

