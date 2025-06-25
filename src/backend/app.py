from flask import Flask, request, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Dummy rubric data
rubric = pd.read_excel("backend/Product_Analytics_Maturity_Assessment.xlsx", sheet_name="Maturity Rubric")

@app.route("/rubric")
def get_rubric():
    return rubric.to_json(orient="records")

@app.route("/")
def home():
    return open("frontend/index.html").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)