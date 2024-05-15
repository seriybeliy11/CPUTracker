from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_get_cpu(monkeypatch):
    response = client.get('/cpu/')
    assert response.status_code == 401

    monkeypatch.setattr('psutil.cpu_percent', lambda percpu: [50] * 12)
    response = client.get('/cpu/', auth=('admin', 'admin'))
    assert response.status_code == 200
    assert response.json() == {'cpu': [50] * 12}

    response = client.get('/cpu/?cpu_id=2',  auth=('admin', 'admin'))
    assert response.status_code == 200
    assert response.json() == {'cpu3': 50}
