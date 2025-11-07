"""Download the embedding model before starting the server."""
from sentence_transformers import SentenceTransformer

print("Downloading embedding model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("Model downloaded successfully!")
print(f"Model saved to: {model._model_card_vars.get('model_id')}")
