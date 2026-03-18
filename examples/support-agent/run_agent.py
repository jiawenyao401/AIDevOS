import httpx

payload = {"message": "tool:text_to_image {\"prompt\": \"support badge\"}"}

resp = httpx.post("http://localhost:8000/stream", json=payload)
print(resp.text)
