# KANDEP: Canteen Tenant Recommendation Website for Kalbis University

## Overview

KANDEP is a tenant recommendation website for the canteen in front of Universitas Kalbis, helping students choose a tenant that matches their preferences. This project was built as a final exam (UAS) assignment.

The system uses survey data collected from Universitas Kalbis students (`Hasil survey.csv`) to train a machine learning model that works as a recommendation/search engine. Users simply enter their study program, budget, and preferred type of food, and the system shows the tenants with the highest relevance.


## Features

- **Top 3 Tenant Recommendations**: shows the three best tenants along with a relevance percentage (model probability).
- **Preference-based input**:
  - Study program (Program Studi)
  - Spending budget per visit (slider from Rp5,000 to Rp50,000, grouped into price ranges)
  - Most frequently ordered menu
- **Navigation pages**: Beranda (Home) and Tentang Kami (About Us), accessible from the sidebar.
- **Pre-trained model**: the model and encoders are loaded from `.pkl` files, so predictions are fast.
- **Unrecognized input handling**: shows a clear error message when the input does not match the training data.
- **Custom UI**: a custom color theme and components styled with CSS.

## Tech Stack

| Category | Technology |
| --- | --- |
| Language | Python |
| Web framework | Streamlit |
| UI navigation | streamlit-option-menu |
| Data processing | pandas |
| Machine learning | scikit-learn (`RandomForestClassifier`, `LabelEncoder`) |
| Model persistence | joblib |
| Dataset | Universitas Kalbis student survey (CSV) |

## Getting Started

Using a virtual environment is recommended (not required) to avoid conflicts with other Python packages:

```bash
python -m venv venv
.venv\Scripts\activate # Windows
# source venv/bin/activate
# macOS / Linux
pip install -r requirements
.txt
streamlit run main.py
```

To retrain the model from the survey data:

```bash
python model.py
```

## Project Structure

```
├── main.py                              # Streamlit app (UI)
├── model.py                             # Model training & prediction
├── Hasil survey.csv                     # Survey dataset
├── tenant_recommendation_model.pkl      # Trained RandomForest model
├── label_encoders.pkl                   # Label encoders for each column
└── requirements.txt
```

## Team

1. Michelle Hiu (2023105488)
2. Najla Melinda Kiasati (2023105534)
3. Benediktus Nikolistyawan (2023105489)
4. Catur Bakti Prajna (2023105533)
