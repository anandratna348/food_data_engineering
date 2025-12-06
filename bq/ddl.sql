CREATE SCHEMA IF NOT EXISTS `YOUR_PROJECT_ID.recipe_analytics`;

CREATE TABLE IF NOT EXISTS `YOUR_PROJECT_ID.recipe_analytics.recipes` (
  recipe_id INT64,
  name STRING,
  cuisine STRING,
  cook_time INT64,
  ingredients ARRAY<STRING>,
  scraped_at TIMESTAMP
) PARTITION BY DATE(scraped_at);
