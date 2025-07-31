from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'alumnos.db'

# Crear tabla si no existe
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumno")
    alumnos = cursor.fetchall()
    conn.close()
    return render_template('index.html', alumnos=alumnos)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alumno (nombre, apellido, edad) VALUES (?, ?, ?)",
                       (nombre, apellido, edad))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        cursor.execute("UPDATE alumno SET nombre = ?, apellido = ?, edad = ? WHERE id = ?",
                       (nombre, apellido, edad, id))
        conn.commit()
        conn.close()
        return redirect('/')
    cursor.execute("SELECT * FROM alumno WHERE id = ?", (id,))
    alumno = cursor.fetchone()
    conn.close()
    return render_template('edit.html', alumno=alumno)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alumno WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
