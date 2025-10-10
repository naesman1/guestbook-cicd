import os
from flask import Flask, render_template, request, redirect, url_for
from redis import Redis

app = Flask(__name__)

# Configuración de Redis: usa las variables de entorno que K8s provee
redis_host = os.environ.get('REDIS_MASTER_SERVICE_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_MASTER_SERVICE_PORT', 6379))
redis_client = Redis(host=redis_host, port=redis_port)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Captura el correo del formulario
        email = request.form.get('email')
        
        if email:
            # Guarda el correo en Redis usando una lista (como el Guestbook original)
            redis_client.lpush('guestbook', email)
            return redirect(url_for('index'))

    # Obtiene la lista de correos para mostrar (máximo 10). La línea larga E501 se rompe aquí:
    guest_emails = [e.decode('utf-8') 
                    for e in redis_client.lrange('guestbook', 0, 9)]
    
    return render_template('index.html', guest_emails=guest_emails)


if __name__ == '__main__':
    # Ejecuta Flask en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
# Asegúrate de que haya una línea vacía al final de este archivo (W292)
