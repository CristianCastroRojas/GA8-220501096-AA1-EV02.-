from flask import Flask, render_template, request, redirect, jsonify
from flask_pymongo import PyMongo, ObjectId
import json

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/autovenz'
mongo = PyMongo(app)

# Ruta para la página principal (opcional para mostrar información)
@app.route('/')
def index():
    """
    Página principal de la aplicación.
    """
    return render_template('index.html')

# Ruta para el formulario de registro
@app.route('/registrar_cliente', methods=['POST'])
def registrar_cliente():
    """
    Endpoint para registrar un nuevo cliente.
    Método: POST
    Parámetros (form data):
    - nombre
    - apellido
    - nombreComercial
    - correoElectronico
    - telefono
    - ciudad
    - comentarios
    """
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        nombre_comercial = request.form['nombreComercial'].strip()
        correo = request.form['correoElectronico'].strip()
        telefono = request.form['telefono'].strip()
        ciudad = request.form['ciudad'].strip()
        comentarios = request.form['comentarios']

        # Crea un documento con los datos del cliente
        cliente_data = {
            'nombre': nombre,
            'apellido': apellido,
            'nombre_comercial': nombre_comercial,
            'correo': correo,
            'telefono': telefono,
            'ciudad': ciudad,
            'comentarios': comentarios
        }

        # Inserta el documento en la colección 'clientes'
        mongo.db.clientes.insert_one(cliente_data)

        # Redirige al usuario a la página de agradecimiento
        return redirect('/thanks')

# Ruta para obtener la lista de clientes como JSON
@app.route('/api/clientes', methods=['GET'])
def obtener_clientes():
    """
    Endpoint para obtener la lista de clientes.
    Método: GET
    Respuesta:
    - Lista de clientes en formato JSON.
    """
    # Obtiene todos los clientes de la colección 'clientes' y los convierte a un formato JSON
    clientes = mongo.db.clientes.find()

    # Convierte el objeto ObjectId a cadena antes de serializar a JSON
    clientes_json = json.dumps([{
        '_id': str(cliente['_id']),
        'nombre': cliente['nombre'],
        'apellido': cliente['apellido'],
        'nombre_comercial': cliente['nombre_comercial'],
        'correo': cliente['correo'],
        'telefono': cliente['telefono'],
        'ciudad': cliente['ciudad'],
        'comentarios': cliente['comentarios']
    } for cliente in clientes])

    return clientes_json

# Ruta para la página de agradecimiento
@app.route('/thanks')
def agradecimiento():
    """
    Página de agradecimiento.
    """
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
