from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    # Tenta conectar ao serviço 'db' definido no docker-compose
    while True:
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'db'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'fiap_tech'),
                database=os.getenv('DB_NAME', 'dimdim_db')
            )
            return conn
        except mysql.connector.Error:
            # Aguarda o banco de dados estar pronto (Health Check)
            time.sleep(2)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chamados ORDER BY id DESC")
    chamados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', chamados=chamados)

@app.route('/registrar', methods=['POST'])
def registrar():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chamados (titulo, descricao) VALUES (%s, %s)", (titulo, descricao))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chamados WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)