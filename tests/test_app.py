import pytest
from app.main import app


@pytest.fixture
def client():
    # E501, E261, W291 corregidos rompiendo la línea y usando 2 espacios
    app.config['TESTING'] = True
    app.config['REDIS_MASTER_SERVICE_HOST'] = 'localhost'  # Configuración segura
    app.config['REDIS_MASTER_SERVICE_PORT'] = 6379  # Configuración segura
    with app.test_client() as client:
        yield client


def test_home_page_status(client):
    """Prueba que la página principal cargue correctamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Libro de Visitas Profesional" in response.data


# Dos líneas vacías aquí (E302 corregido)
def test_submit_email(client):
    """Prueba el envío del formulario de correo."""
    data = {'email': 'test@ci-cd.com'}
    response = client.post('/', data=data, follow_redirects=True)
    
    # El status debe ser 200 después de la redirección
    assert response.status_code == 200
    pass
# Asegúrate de que no haya espacios en líneas vacías (W293)
