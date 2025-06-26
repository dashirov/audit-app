import pandas as pd
from flask import Flask
from models import db
from models.core import Subject, MaturityRubric
from config import Config
import uuid

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def load_rubric_only():
    df_rubric = pd.read_excel("Product_Analytics_Maturity_Assessment.xlsx", sheet_name="Maturity Rubric")

    with app.app_context():
        subjects = Subject.query.all()
        subject_name_to_id = {s.name.strip(): s.id for s in subjects}

        for _, row in df_rubric.iterrows():
            category = row["Category"].strip()
            subject_id = subject_name_to_id.get(category)

            if not subject_id:
                print(f"❌ Subject not found for category: {category}")
                continue

            rubric = MaturityRubric(
                id=str(uuid.uuid4()),
                subject_id=subject_id,
                score=int(row["Score"]),
                description=row["Description"]
            )
            db.session.add(rubric)

        db.session.commit()
        print("✅ Maturity rubric loaded successfully.")

if __name__ == "__main__":
    load_rubric_only()