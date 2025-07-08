from flask import Flask, request, render_template
import pandas as pd
import joblib
import os

app = Flask(__name__)
model = joblib.load(os.path.join(os.path.dirname(__file__), '../model/student_model.pkl'))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    parental_levels = ["associate's degree", "bachelor's degree", "high school", "master's degree", "some college", "some high school"]

    if request.method == "POST":
        data = request.form.to_dict()
        df_input = pd.DataFrame([data])
        df_input[['math score','reading score','writing score']] = df_input[['math score','reading score','writing score']].astype(float)
        df_input['average_score'] = df_input[['math score','reading score','writing score']].mean(axis=1)
        df_input['pass'] = (df_input['average_score'] >= 50).astype(int)
        df_input = pd.get_dummies(df_input)
        for col in model.feature_names_in_:
            if col not in df_input.columns:
                df_input[col] = 0
        df_input = df_input[model.feature_names_in_]
        prediction = "Pass" if model.predict(df_input)[0] else "Fail"

    return render_template("index.html", prediction=prediction, parental_levels=parental_levels)

if __name__ == "__main__":
    app.run(debug=True)
# This code is for a Flask web application that predicts student performance based on input data.
# It loads a pre-trained model, processes input data, and renders a template with the prediction