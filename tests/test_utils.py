from fastapi.testclient import TestClient
from jsonpath_ng import parse
from src.api import api
from typing import Any, Optional

client = TestClient(api)


def get_json_val(json: Any, path: str) -> Optional[Any]:
    query = parse(path)
    match = query.find(json)
    return match[0].value if match else None
