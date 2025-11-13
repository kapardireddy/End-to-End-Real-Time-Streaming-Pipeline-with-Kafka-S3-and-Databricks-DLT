from kafka import KafkaConsumer
import json, time, os
import pandas as pd
from datetime import datetime
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_FOLDER = os.getenv("S3_FOLDER", "/transactions/")

BOOTSTRAP = 'localhost:9092'
TOPIC = 'transaction_logs'
BATCH_SIZE = 100
BATCH_TIMEOUT = 30  # seconds

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='transaction-stream',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

os.makedirs('./out/transactions', exist_ok=True)

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

def upload_to_s3(local_path):
    """Uploads a file to S3 under /transactions/ and removes it locally."""
    filename = os.path.basename(local_path)
    key = f"{S3_FOLDER.strip('/')}/{filename}"

    try:
        s3.upload_file(local_path, S3_BUCKET_NAME, key)
        print(f"Uploaded {local_path} → s3://{S3_BUCKET_NAME}/{key}")
        os.remove(local_path)
    except Exception as e:
        print(f"Failed to upload {local_path}: {e}")

def flush_batch(batch_list):
    if not batch_list:
        return

    df = pd.DataFrame(batch_list)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    out_path = f'./out/transactions/transactions_{timestamp}.json'

    df.to_json(out_path, orient='records', lines=True)
    print(f'Wrote {len(df)} records → {out_path}')
    upload_to_s3(out_path)

batch = []
last_flush = time.time()

try:
    print(f"Consuming from Kafka topic: {TOPIC}")
    for msg in consumer:
        batch.append(msg.value)
        now = time.time()
        if len(batch) >= BATCH_SIZE or (now - last_flush) >= BATCH_TIMEOUT:
            flush_batch(batch)
            batch = []
            last_flush = now
except KeyboardInterrupt:
    print("Interrupted. Flushing remaining messages...")
    flush_batch(batch)
finally:
    consumer.close()
