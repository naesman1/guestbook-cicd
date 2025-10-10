import pytest
from app.main import app


@pytest.fixture
def client():
    # Eliminar el comentario E501, E261, W291 para tener solo código limpio o hacerlo corto.
    app.config['TESTING'] = True
    # E501 corregido haciendo el comentario corto
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