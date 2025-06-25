from flask import Flask, request, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Dummy categories data
subject = pd.read_excel("backend/Product_Analytics_Maturity_Assessment.xlsx", sheet_name="Subject")
# Dummy rubric data
rubric = pd.read_excel("backend/Product_Analytics_Maturity_Assessment.xlsx", sheet_name="Maturity Rubric")

@app.route("/subject")
def get_subject():
    # Only include Category, Objective, Activities for each entry
    cols = ["Category", "Objective", "Activities"]
    filtered = subject[cols] if all(col in subject.columns for col in cols) else subject
    return filtered.to_json(orient="records")

@app.route("/rubric")
def get_rubric():
    return rubric.to_json(orient="records")

@app.route("/")
def home():
    return open("frontend/index.html").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)