import pandas as pd
import json
from datetime import datetime

STUDENT_DATA_PATH = "backend/data/student_dataset.csv"


def load_df():
    return pd.read_csv(STUDENT_DATA_PATH)


def save_df(df):
    df.to_csv(STUDENT_DATA_PATH, index=False)


def upsert_student(data: dict):
    df = load_df()

    data["skills"] = json.dumps(data["skills"])
    data["methodologies"] = ",".join(data["methodologies"])
    data["last_updated"] = datetime.utcnow().isoformat()

    if data["student_id"] in df["student_id"].values:
        df.loc[df["student_id"] == data["student_id"], :] = data
    else:
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    save_df(df)


def list_students():
    return load_df().to_dict(orient="records")
