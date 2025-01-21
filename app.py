from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
 # Para devolver los resultados como diccionarios
    return conn

# Crear la tabla si no existe
def init_db():
    with get_db_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        """)
    print("Base de datos inicializada")

# Página principal: Listar registros
@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

# Crear un nuevo registro
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            return "El nombre es obligatorio.", 400

        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# Editar un registro
@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()

    if not item:
        return f"Registro con id {id} no encontrado.", 404

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        conn.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update.html', item=item)

# Eliminar un registro
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 

