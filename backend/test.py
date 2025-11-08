from google import genai
client = genai.Client(api_key="AIzaSyBHOpG0RSTI_KVpOoHVaba7PXVuXfQi4M4")

for model in client.models.list():
    print(model.name)
