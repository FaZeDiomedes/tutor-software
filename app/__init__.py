from flask import Flask, session

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_aqui"  # Para sesiones

from app import routes

# Context processor para inyectar 'user' en todos los templates automáticamente
@app.context_processor
def inject_user():
    return dict(user=session.get('user'))
