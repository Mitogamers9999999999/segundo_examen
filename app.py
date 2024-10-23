from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Inicializa los productos en la sesión
@app.before_request
def iniciar_sesion():
    if 'productos' not in session:
        session['productos'] = []

# Ruta principal para mostrar los productos
@app.route('/')
def gestion_productos():
    return render_template('productos.html', productos=session['productos'])

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    id_unico = len(session['productos']) + 1
    nombre = request.form['nombre']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    fecha_vencimiento = request.form['fecha_vencimiento']
    categoria = request.form['categoria']
    
    nuevo_producto = {
        'id': id_unico,
        'nombre': nombre,
        'cantidad': cantidad,
        'precio': precio,
        'fecha_vencimiento': fecha_vencimiento,
        'categoria': categoria
    }
    
    productos = session['productos']
    productos.append(nuevo_producto)
    session['productos'] = productos
    
    return redirect(url_for('gestion_productos'))

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    productos = session['productos']
    productos = [producto for producto in productos if producto['id'] != id]
    session['productos'] = productos
    return redirect(url_for('gestion_productos'))

# Ruta para editar un producto (mostrar formulario de edición)
@app.route('/editar/<int:id>')
def editar_producto(id):
    productos = session['productos']
    producto = next((producto for producto in productos if producto['id'] == id), None)
    return render_template('editar.html', producto=producto)

# Ruta para guardar los cambios al editar un producto
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_producto(id):
    productos = session['productos']
    for producto in productos:
        if producto['id'] == id:
            producto['nombre'] = request.form['nombre']
            producto['cantidad'] = int(request.form['cantidad'])
            producto['precio'] = float(request.form['precio'])
            producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
            producto['categoria'] = request.form['categoria']
            break
    session['productos'] = productos
    return redirect(url_for('gestion_productos'))

if __name__ == '__main__':
    app.run(debug=True)
