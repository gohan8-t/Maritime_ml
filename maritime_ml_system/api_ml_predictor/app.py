from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)
model = joblib.load("co2_predictor_model.pkl")
features = joblib.load("co2_model_features.pkl")

@app.route("/predict_co2", methods=["POST"])
def predict_co2():
    data = request.get_json()
    df = pd.DataFrame([data])
    df = pd.get_dummies(df)
    for col in features:
        if col not in df.columns:
            df[col] = 0
        df = df[features]
    prediction = model.predict(df)[0]
    return jsonify({
        "predicted_co2_kgph": round(prediction, 2),
        "note": "Predicted CO₂ emission per hour using ML model."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)