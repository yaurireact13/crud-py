from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directorio para guardar las imágenes
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista para almacenar los contactos
contactos = []

@app.route('/')
def index():
    return render_template('index.html', contactos=contactos)

@app.route('/agregar', methods=['POST'])
def agregar_contacto():
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    imagen = request.files.get('imagen')  # Obtener la imagen

    if nombre and telefono and imagen:
        # Guardar la imagen en la carpeta "uploads"
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Guardar el contacto con la imagen
        contactos.append({
            "nombre": nombre,
            "telefono": telefono,
            "imagen": filename  # Guardar el nombre de la imagen
        })
    return redirect(url_for('index'))

@app.route('/actualizar/<int:index>', methods=['POST'])
def actualizar_contacto(index):
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    imagen = request.files.get('imagen')  # Obtener la imagen para actualizarla si es necesario

    if 0 <= index < len(contactos) and nombre and telefono:
        contacto = contactos[index]
        contacto["nombre"] = nombre
        contacto["telefono"] = telefono

        if imagen:
            # Guardar la nueva imagen
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            contacto["imagen"] = filename  # Actualizar la imagen del contacto

    return redirect(url_for('index'))

@app.route('/eliminar/<int:index>')
def eliminar_contacto(index):
    if 0 <= index < len(contactos):
        contactos.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
