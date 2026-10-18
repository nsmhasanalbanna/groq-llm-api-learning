from config.settings import settings

def get_voyage_header():
    headers={
                    "Authorization": f"Bearer {settings.voyage_api_key}",
                    "Content-Type": "application/json"
                }
    return headers

def get_voyage_url():
    return "https://api.voyageai.com/v1/embeddings"

def get_voyage_model():
    return "voyage-4-lite"