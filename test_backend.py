import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    res = requests.get(BASE_URL)
    print("✅ Health Check:", res.json())

def test_upload():
    file_path = "sample.txt"  # create a small text file for testing
    files = {"file": open(file_path, "rb")}
    res = requests.post(f"{BASE_URL}/upload/file", files=files)
    print("✅ Upload Response:", res.json())

def test_query():
    payload = {"query": "What is the content of the document?"}
    res = requests.post(f"{BASE_URL}/chat/query", json=payload)
    print("💬 Chat Response:", res.json())

if __name__ == "__main__":
    print("\n🚀 Running Smart University Assistant Backend Tests\n")
    test_health()
    test_upload()
    test_query()