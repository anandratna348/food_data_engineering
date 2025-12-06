import functions_framework
import requests
import os
from google.cloud import storage
from datetime import datetime
import uuid
import json

BUCKET = os.getenv("BUCKET")  # set when deploying

@functions_framework.http
def ingest_recipes(request):
    # simple param: q (search term)
    q = request.args.get("q", "chicken")
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={q}"
    r = requests.get(url, timeout=20)
    payload = r.json()

    client = storage.Client()
    bucket = client.bucket(BUCKET)
    name = f"raw/recipes_{q}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:6]}.json"
    blob = bucket.blob(name)
    blob.upload_from_string(json.dumps(payload), content_type="application/json")

    return (f"Uploaded raw data to gs://{BUCKET}/{name}", 200)
