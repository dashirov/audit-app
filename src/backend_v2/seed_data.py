import pandas as pd
from app import create_app
from models import db
from models.core import Role

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    df_roles = pd.read_csv("data/roles.csv")
    # df_areas = pd.read_csv("data/subject_areas.csv")
    # df_categories = pd.read_csv("data/subject_categories.csv")
    # df_questions = pd.read_excel("seed_data.xlsx", sheet_name="InterviewQuestions")
    # df_answers = pd.read_excel("seed_data.xlsx", sheet_name="Answers")
    # df_rubric = pd.read_excel("seed_data.xlsx", sheet_name="RubricLevels")

    # Seed roles
    roles_map = {}
    for _, row in df_roles.iterrows():
        role = Role(title=row["title"])
        db.session.add(role)
        roles_map[role.title] = role
        print(f"-> Added Role {role.title}")

    # # Seed subject areas
    # areas_map = {}
    # for _, row in df_areas.iterrows():
    #     area = SubjectArea(name=row["name"])
    #     db.session.add(area)
    #     areas_map[area.name] = area

    db.session.commit()
    #
    # # Seed categories
    # categories_map = {}
    # for _, row in df_categories.iterrows():
    #     if row.get("subject_area") is None:
    #         raise "Record does not have a subject area defined"
    #     if areas_map.get(row["subject_area"]) is None:
    #         raise "{} is not a valid subject area".format( row["subject_area"])
    #     area = areas_map[row["subject_area"]]
    #     cat = SubjectCategory(
    #         subject_area_id=area.id,
    #         name=row["name"],
    #         objective=row["objective"],
    #         activities=row["activities"]
    #     )
    #     db.session.add(cat)
    #     categories_map[cat.name] = cat
    #
    # db.session.commit()
    #
    # # Seed rubric levels
    # for _, row in df_rubric.iterrows():
    #     category = categories_map[row["category_name"]]
    #     level = RubricLevel(
    #         category_id=category.id,
    #         score=int(row["score"]),
    #         description=row["description"]
    #     )
    #     db.session.add(level)
    #
    # # Seed questions
    # for _, row in df_questions.iterrows():
    #     category = categories_map[row["category_name"]]
    #     role = roles_map[row["role_title"]]
    #     q = InterviewQuestion(
    #         category_id=category.id,
    #         role_id=role.id,
    #         text=row["text"]
    #     )
    #     db.session.add(q)
    #
    # # Seed answers
    # for _, row in df_answers.iterrows():
    #     a = InterviewAnswer(
    #         score=int(row["score"]),
    #         text=row["text"]
    #     )
    #     db.session.add(a)
    #
    # db.session.commit()

    print("✅ Seeded data from Excel.")