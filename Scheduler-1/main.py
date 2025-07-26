import os
import pandas as pd
import json
from google.cloud import pubsub_v1, storage
from datetime import datetime, timedelta
from io import BytesIO

# Configuration
BUCKET_NAME = '<bucket_name>'
CSV_FILE_NAME = 'historical_network_quality_nov2024_dec2025.csv'
TOPIC_PATH = '<topic_path>'

def json_serial(obj):
    if isinstance(obj, (datetime, pd.Timestamp)):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def load_csv_from_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_bytes()
    return pd.read_csv(BytesIO(data), parse_dates=['DateTime'])

def publish_area_batch(publisher, topic_path, area_df):
    now = area_df['DateTime'].max()
    window_start = now - timedelta(hours=24)
    records = area_df[(area_df['DateTime'] >= window_start) & (area_df['DateTime'] <= now)]
    latest = records[records['DateTime'] == now].iloc[0].to_dict()
    message_dict = {
        'Area': latest['Area'],
        'history': records.to_dict('records'),
        'latest': latest,
    }
    future = publisher.publish(topic_path, json.dumps(message_dict, default=json_serial).encode('utf-8'))
    print(f'published message id {future.result()}')
def main():
    df = load_csv_from_gcs(BUCKET_NAME, CSV_FILE_NAME)
    publisher = pubsub_v1.PublisherClient()
    for area in df['Area'].unique():
        area_df = df[df['Area'] == area].sort_values('DateTime')
        publish_area_batch(publisher, TOPIC_PATH, area_df)

# Entry point for cloud function
def publish_to_pubsub(request):
    main()
    return 'Done', 200
