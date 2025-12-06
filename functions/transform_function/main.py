import json
from google.cloud import storage, bigquery
from datetime import datetime
import os

BUCKET = os.getenv("BUCKET")
BQ_DATASET = os.getenv("BQ_DATASET", "recipe_analytics")
BQ_PROJECT = os.getenv("PROJECT", None)

def normalize_mealdb_payload(payload):
    rows = []
    for meal in payload.get("meals") or []:
        ingredients = []
        for i in range(1, 21):
            ingr = meal.get(f"strIngredient{i}")
            if ingr and ingr.strip():
                ingredients.append(ingr.strip())
        rows.append({
            "recipe_id": int(meal.get("idMeal", 0)),
            "name": meal.get("strMeal"),
            "cuisine": meal.get("strArea"),
            "cook_time": None,
            "ingredients": ingredients,
            "scraped_at": datetime.utcnow().isoformat()
        })
    return rows

def gcs_to_bq(rows, client_bq):
    # Insert rows into BigQuery table: recipe_analytics.recipes
    table_id = f"{client_bq.project}.{BQ_DATASET}.recipes"
    errors = client_bq.insert_rows_json(table_id, rows)
    return errors

def process_blob(data, context):
    client = storage.Client()
    bq_client = bigquery.Client(project=BQ_PROJECT) if BQ_PROJECT else bigquery.Client()
    bucket_name = data["bucket"]
    name = data["name"]
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(name)
    content = blob.download_as_bytes()
    try:
        payload = json.loads(content)
    except Exception as e:
        print("Not JSON:", e)
        return

    rows = normalize_mealdb_payload(payload)
    # write processed file
    processed_name = name.replace("raw/", "processed/").rsplit(".json",1)[0] + ".json"
    proc_blob = bucket.blob(processed_name)
    proc_blob.upload_from_string(json.dumps(rows), content_type="application/json")
    print(f"Wrote processed file: gs://{bucket_name}/{processed_name}")

    # optionally load to BigQuery (if dataset/table exists)
    try:
        errs = gcs_to_bq(rows, bq_client)
        if errs:
            print("BQ insert errors:", errs)
    except Exception as e:
        print("BQ insert skipped/failed:", e)
