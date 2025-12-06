🍽️ Serverless Food Data Engineering Pipeline (GCP – Free Tier, No Docker)

This repository contains a complete serverless data engineering pipeline designed for Google Cloud Platform (GCP) using Cloud Functions, Cloud Storage, BigQuery, and a static dashboard, all without requiring Docker or paid cloud services.
Although GCP deployment is pending (due to billing verification), the entire cloud-ready codebase is included and can be deployed immediately once a GCP project is active.

⭐ Project Overview

This project demonstrates how to build a scalable, serverless data pipeline for collecting, processing, and visualizing recipe and food data from a public API. The pipeline follows a clean ETL architecture:

Extract: A Cloud Function fetches recipes from TheMealDB API and stores raw JSON files in a GCS bucket.

Transform: A second Cloud Function triggers on new files, cleans and normalizes the recipe data, and outputs processed JSON. It also prepares a consistent file (recipes_processed.json) for the dashboard.

Load (optional): The processed data can be loaded into a partitioned BigQuery table for analytics.

Visualize: A static HTML dashboard hosted on Cloud Storage fetches processed data and displays interactive charts using Chart.js.

This codebase mirrors a real-world data engineering workflow using serverless components on GCP.

📁 Repository Structure
food_data_engineering/
├── functions/
│   ├── ingest_function/
│   │   ├── main.py
│   │   └── requirements.txt
│   └── transform_function/
│       ├── main.py
│       └── requirements.txt
├── web/
│   └── index.html
├── bq/
│   └── ddl.sql
└── README.md

🧩 Key Features

100% serverless, no Docker required

Real API ingestion from TheMealDB

Raw → processed data flow using Cloud Storage triggers

BigQuery-ready data schema

Public, lightweight dashboard using Chart.js

Follows industry-standard ETL pipeline patterns

Designed to run entirely in GCP free tier

🚀 How It Works (Conceptual Flow)

User or scheduler triggers:

/ingest_recipes?q=chicken


Cloud Function fetches recipes → saves to:

gs://<bucket>/raw/...


Storage event triggers transform function → normalized data saved to:

gs://<bucket>/processed/recipes_processed.json


Dashboard loads processed data → displays cuisines & recipe stats

Optional: Data inserted into BigQuery for extended analytics

📊 BigQuery Schema (DDL)

Located in: bq/ddl.sql

CREATE SCHEMA IF NOT EXISTS `<PROJECT_ID>.recipe_analytics`;

CREATE TABLE IF NOT EXISTS `<PROJECT_ID>.recipe_analytics.recipes` (
  recipe_id INT64,
  name STRING,
  cuisine STRING,
  cook_time INT64,
  ingredients ARRAY<STRING>,
  scraped_at TIMESTAMP
) PARTITION BY DATE(scraped_at);

🔧 Deployment (Pending until GCP Account Activation)

Once GCP account is active, deploy like this:

Deploy ingestion function:
gcloud functions deploy ingest_recipes \
  --runtime=python311 \
  --trigger-http \
  --allow-unauthenticated \
  --source=functions/ingest_function \
  --set-env-vars BUCKET=<your-bucket>

Deploy transformation function:
gcloud functions deploy transform_on_finalize \
  --runtime=python311 \
  --trigger-resource=<your-bucket> \
  --trigger-event=google.storage.object.finalize \
  --source=functions/transform_function \
  --set-env-vars BUCKET=<your-bucket>

Deploy static dashboard:
gsutil cp web/index.html gs://<your-bucket>/index.html
gsutil web set -m index.html gs://<your-bucket>

📝 Current Status

🔧 Deployment to GCP is pending due to payment verification failure.
However, the entire serverless pipeline codebase is included, fully functional, and ready for deployment once the account becomes active.
