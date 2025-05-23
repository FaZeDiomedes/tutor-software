from flask import render_template, request, redirect, url_for, session, flash
from app import app
import re  # Importamos módulo para expresiones regulares

# Simulación de usuarios en memoria
usuarios = {
    'admin@itc.edu.co': {'password': 'admin123', 'rol': 'admin', 'progreso': {}}
}

# Lista simulada para almacenar lecciones
lecciones = []

@app.route('/')
def index():
    if 'user' in session:
        if session.get('rol') == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('menu'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = usuarios.get(email)
        if user and user['password'] == password:
            session['user'] = email
            session['rol'] = user.get('rol', 'estudiante')
            if session['rol'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('menu'))
        else:
            return render_template('login.html', error='Credenciales inválidas')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validar que el correo sea institucional
        if not re.match(r'^[\w\.-]+@itc\.edu\.co$', email):
            return render_template('register.html', error='Solo se permiten correos institucionales (@itc.edu.co)')

        if email in usuarios:
            return render_template('register.html', error='Usuario ya existe')

        usuarios[email] = {'password': password, 'progreso': {}, 'rol': 'estudiante'}
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/menu')
def menu():
    if 'user' not in session or session.get('rol') != 'estudiante':
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/lecciones')
def lecciones_estudiante():
    if 'user' not in session or session.get('rol') != 'estudiante':
        return redirect(url_for('login'))
    return render_template('lecciones.html')

@app.route('/quiz')
def quiz():
    if 'user' not in session or session.get('rol') != 'estudiante':
        return redirect(url_for('login'))
    return render_template('quiz.html')

@app.route('/perfil')
def perfil():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('perfil.html')

@app.route('/feedback')
def feedback():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feedback.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('rol', None)
    return redirect(url_for('login'))

# --- Rutas administrativas ---

@app.route('/admin')
def admin_dashboard():
    if 'user' not in session or session.get('rol') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html')

@app.route('/admin/lecciones/agregar', methods=['GET', 'POST'])
def admin_agregar_leccion():
    if 'user' not in session or session.get('rol') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']

        # Agregar la nueva lección a la lista simulada
        lecciones.append({'titulo': titulo, 'contenido': contenido})

        return redirect(url_for('admin_listar_lecciones'))

    return render_template('admin/agregar_leccion.html')

@app.route('/admin/lecciones')
def admin_listar_lecciones():
    if 'user' not in session or session.get('rol') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin/listar_lecciones.html', lecciones=lecciones)

@app.route('/admin/lecciones/eliminar/<int:index>', methods=['POST'])
def admin_eliminar_leccion(index):
    if 'user' not in session or session.get('rol') != 'admin':
        return redirect(url_for('login'))
    if 0 <= index < len(lecciones):
        lecciones.pop(index)
    return redirect(url_for('admin_listar_lecciones'))

# --- Gestión de usuarios ---

@app.route('/admin/usuarios')
def admin_listar_usuarios():
    if session.get("rol") != "admin":
        return redirect(url_for("login"))
    return render_template("admin/listar_usuarios.html", usuarios=usuarios)

@app.route('/admin/usuarios/agregar', methods=['GET', 'POST'])
def admin_agregar_usuario():
    if session.get("rol") != "admin":
        return redirect(url_for("login"))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        rol = request.form.get('rol')

        if email in usuarios:
            flash('El usuario ya existe.', 'error')
            return redirect(url_for('admin_agregar_usuario'))

        usuarios[email] = {'password': password, 'rol': rol, 'progreso': {}}
        flash('Usuario agregado con éxito.', 'success')
        return redirect(url_for('admin_listar_usuarios'))

    return render_template("admin/agregar_usuario.html")

@app.route('/admin/usuarios/eliminar/<path:email>', methods=['POST'])
def admin_eliminar_usuario(email):
    if session.get("rol") != "admin":
        return redirect(url_for("login"))

    if email in usuarios:
        del usuarios[email]
        flash('Usuario eliminado con éxito.', 'success')

    return redirect(url_for('admin_listar_usuarios'))


