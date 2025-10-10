import pytest
from app.main import app


@pytest.fixture  # E302 corregido: dos líneas vacías arriba
def client():
    # Configura la app para testing (W291: asegurar que no haya espacio al final de esta línea)
    app.config['TESTING'] = True
    app.config['REDIS_MASTER_SERVICE_HOST'] = 'localhost' # W291: asegurar que no haya espacio al final
    app.config['REDIS_MASTER_SERVICE_PORT'] = 6379 # W291: asegurar que no haya espacio al final
    with app.test_client() as client:
        yield client


def test_home_page_status(client):  # E302 corregido: dos líneas vacías arriba
    """Prueba que la página principal cargue correctamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Libro de Visitas Profesional" in response.data

def test_submit_email(client):
    """Prueba el envío del formulario de correo."""
    data = {'email': 'test@ci-cd.com'}
    response = client.post('/', data=data, follow_redirects=True)
    
    # El status debe ser 200 después de la redirección
    assert response.status_code == 200
    pass
