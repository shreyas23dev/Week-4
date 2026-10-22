# Week 4 Capstone Presentation — Slide Outline

Use this outline to present the project; the accompanying `presentation.pdf` contains these slides.

1. **Title** — Titanic Survival Prediction API; AI Pioneers Internship, Week 4.
2. **Problem and objective** — Demonstrate a complete ML workflow that estimates survival from passenger attributes and serves predictions through an API.
3. **Dataset and features** — 891 rows; age, family counts, fare, class, sex, and port; binary survival target. State historical-data and responsible-use limitations.
4. **End-to-end architecture** — CSV → train/test split → preprocessing pipeline → Random Forest → Joblib artifact → FastAPI → browser form / JSON client.
5. **Preprocessing and training** — Training-only median/mode imputers, standard scaling, one-hot encoding, stratified 80/20 split, fixed seed.
6. **Testing and evaluation** — Held-out accuracy, precision, recall, F1, ROC AUC, and confusion matrix; API validation and automated tests.
7. **Demo** — Start the local ASGI server, use the web form, and show the `/docs` API page or `POST /predict` response.
8. **Deployment and limitations** — Local app is runnable; public cloud hosting requires choosing a target and credentials. Historical data means estimates are educational only.
9. **Conclusion and next steps** — Improve validation, monitor service behavior, document model versioning, and investigate model fairness before any further use.
