import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

features = [
    "Program Studi",
    "Berapa rata-rata pengeluaran Anda per kunjungan?",
    "Menu apa yang paling sering Anda pesan?"
]

target = "Tenant mana yang sering anda kunjungi?"

def train_and_save_model(csv_path="Hasil survey.csv"):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip() # membersihkan spasi di header kolom
    data = df[features + [target]].dropna()
    encoders = {}
    for col in data.columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        encoders[col] = le
    X = data[features]
    y = data[target]

    # split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)

    # hitung akurasi
    y_pred = model.predict(X_test)
    akurasi = accuracy_score(y_test, y_pred)
    print(f"Akurasi Model: {akurasi:.2f}")
    joblib.dump(model, "tenant_recommendation_model.pkl")
    joblib.dump(encoders, "label_encoders.pkl")

    print("Model & encoder berhasil disimpan")
if __name__ == "__main__":
    train_and_save_model()

def load_model():
    model = joblib.load("tenant_recommendation_model.pkl")
    encoders = joblib.load("label_encoders.pkl")
    return model, encoders

def predict_tenant(model, encoders, prodi, budget, jenis_makanan):
    input_df = pd.DataFrame([{
        "Program Studi": encoders["Program Studi"].transform([prodi])[0],
        "Berapa rata-rata pengeluaran Anda per kunjungan?": encoders["Berapa rata-rata pengeluaran Anda per kunjungan?"].transform([budget])[0],
        "Menu apa yang paling sering Anda pesan ? ": encoders["Menu apa yang paling sering Anda pesan ? "].transform([jenis_makanan])[0]
    }])
    proba = model.predict_proba(input_df)[0]
    nama_tenant = encoders[target].classes_
    result = pd.DataFrame({
        "Tenant": nama_tenant,
        "Probabilitas": proba
    }).sort_values(by="Probabilitas", ascending=False)
    return result.head(3)