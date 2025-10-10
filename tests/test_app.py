import pytest
from app.main import app


@pytest.fixture
def client():

    app.config['TESTING'] = True
    app.config['REDIS_MASTER_SERVICE_HOST'] = 'localhost'  # Master HOST
    app.config['REDIS_MASTER_SERVICE_PORT'] = 6379  # Master PORT
    with app.test_client() as client:
        yield client


def test_home_page_status(client):
    """Prueba que la página principal cargue correctamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Libro de Visitas Profesional" in response.data


def test_submit_email(client):
    """Prueba el envío del formulario de correo."""
    data = {'email': 'test@ci-cd.com'}
    response = client.post('/', data=data, follow_redirects=True)

    assert response.status_code == 200
    pass
