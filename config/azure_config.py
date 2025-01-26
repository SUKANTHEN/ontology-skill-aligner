from openai import AzureOpenAI

AZURE_OPENAI_ENDPOINT = "https://openaibrdev-sc.openai.azure.com"
AZURE_OPENAI_API_KEY = "1SsseBj50Rttfc7ycrpz7l6MHKEEHetUVh54dLbTuUWHo6Gk8ejaJQQJ99AKACfhMk5XJ3w3AAABACOGh1dq"

# Initialize AzureOpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-08-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

MODEL_NAME = "text-embedding-ada-002"

def get_embedding_from_text(text, model="text-embedding-ada-002"):
    try:
        embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
        return embedding
    except Exception as error:
        return []
