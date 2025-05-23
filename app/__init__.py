import os
from flask import Flask, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_por_defecto_para_dev')

from app import routes

@app.context_processor
def inject_user():
    return dict(user=session.get('user'))
