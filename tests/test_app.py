import pytest
from app.main import app

@pytest.fixture
def client():
    # Configura la app para testing 
    app.config['TESTING'] = True
    app.config['REDIS_MASTER_SERVICE_HOST'] = 'localhost' 
    app.config['REDIS_MASTER_SERVICE_PORT'] = 6379 
    with app.test_client() as client:
        yield client

def test_home_page_status(client):
    """Prueba que la página principal cargue correctamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Libro de Visitas Profesional" in response.data
