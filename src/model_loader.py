import joblib
from google.cloud import storage
import tempfile
import os

def load_model_from_gcs(gcs_path):
    bucket_name, blob_path = gcs_path.replace("gs://", "").split("/", 1)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    temp_dir = tempfile.mkdtemp()
    local_path = os.path.join(temp_dir, "model.pkl")

    blob.download_to_filename(local_path)

    return joblib.load(local_path)
