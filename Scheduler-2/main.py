import os
import pandas as pd
import json
from google.cloud import pubsub_v1, storage
from datetime import datetime, timedelta
from io import BytesIO

# Configuration
BUCKET_NAME = '<bucket_name>'
CSV_FILE_NAME = 'hsr_layout_police_radio_chatter_dataset.csv'
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
    window_start = now - timedelta(minutes=10)
    records = area_df[(area_df['DateTime'] >= window_start) & (area_df['DateTime'] <= now)]
    message_dict = {
        'RecentData': records.to_dict('records')
    }
    future = publisher.publish(topic_path, json.dumps(message_dict, default=json_serial).encode('utf-8'))
    print(f'published message id {future.result()}')

def main():
    df = load_csv_from_gcs(BUCKET_NAME, CSV_FILE_NAME)
    publisher = pubsub_v1.PublisherClient()
    area_df = df.sort_values('DateTime')
    publish_area_batch(publisher, TOPIC_PATH, area_df)

# Entry point for cloud function
def publish_radio_to_pubsub(request):
    main()
    return 'Done', 200