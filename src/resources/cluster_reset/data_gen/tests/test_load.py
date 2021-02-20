import pytest
import requests
from data_gen.generate.fake import fake_data
from data_gen.load import load_data
from pathlib import Path


def test_load_data(manager, monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: {"status_code": 200})
    data_dir = Path("tmp/test/load_data")

    fake_data(manager, data_dir)
    response = load_data(manager, data_dir)
    assert response
