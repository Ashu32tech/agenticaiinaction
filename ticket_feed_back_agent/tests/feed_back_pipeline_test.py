import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from feed_back_pipeline import run
from dotenv import load_dotenv

load_dotenv(override=True)

def test_feed_back_agent():
    payload = {
        "review_id": 1,
        "review_text": "App crashes on login"
    }

    res = run(payload)

    assert isinstance(res, dict)
    assert "category" in res
    assert "priority" in res

    print(res)

if __name__ == "__main__":
    test_feed_back_agent()