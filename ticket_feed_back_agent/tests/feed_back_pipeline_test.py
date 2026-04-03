import requests

def test_mcp():
    payload = {
        "row": {
            "review_id": 1,
            "review_text": "App crashes on login"
        }
    }

    res = requests.post(
        "http://localhost:8000/tools/process_feedback",
        json=payload
    )

    assert res.status_code == 200
    print(res.json())

if __name__ == "__main__":
    test_mcp()