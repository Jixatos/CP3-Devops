import os
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configura as variáveis de ambiente para conexão com o banco de dados
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]
AUTH_PLUGIN = os.environ["AUTH_PLUGIN"]

# Cria a conexão com o banco de dados
connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    auth_plugin=AUTH_PLUGIN,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Cria a tabela 'tbl_cadastro' no banco de dados, caso ainda não exista
with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_cadastro (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            password VARCHAR(255) NOT NULL
        )
    """)

@app.route("/")
def index():
    return "API is running!"

@app.route("/tbl_cadastro", methods=["GET"])
def get_tbl_cadastro():
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM tbl_cadastro')
            records = cursor.fetchall()
            data = [{'id': record[0], 'username': record[1], 'password': record[2]} for record in records]
            return jsonify(data)
    except Error as e:
        print(e)
        return jsonify({'message': 'Erro ao buscar registros da tabela tbl_cadastro.'}), 500

@app.route("/tbl_cadastro", methods=["POST"])
def create_tbl_cadastro():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tbl_cadastro (username, password)
                VALUES (%s, %s)
            """, (username, password))
            connection.commit()

        return jsonify({"message": "Registro inserido com sucesso!"}), 201
    except Error as e:
        print(e)
        return jsonify({'message': 'Erro ao inserir registro na tabela tbl_cadastro.'}), 500

@app.route("/tbl_cadastro/<int:id>", methods=["PUT"])
def update_tbl_cadastro(id):
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE tbl_cadastro
                SET username=%s, password=%s
                WHERE id=%s
            """, (username, password, id))
            connection.commit()

        return jsonify({"message": "Registro atualizado com sucesso!"})
    except Error as e:
        print(e)
        return jsonify({'message': 'Erro ao atualizar registro na tabela tbl_cadastro.'}), 500

@app.route("/tbl_cadastro/<int:id>", methods=["DELETE"])
def delete_tbl_cadastro(id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM tbl_cadastro
                WHERE id=%s
            """, (id,))
            connection.commit()
        return jsonify({"message": "Registro deletado com sucesso!"})
    except Error as e:
        print(e)
        return jsonify({'message': 'Erro ao deletar registro na tabela tbl_cadastro.'}), 500

@app.route("/test_insert", methods=["GET"])
def test_insert():
    username = "testuser"
    password = "testpassword"

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tbl_cadastro (username, password)
                VALUES (%s, %s)
            """, (username, password))
            connection.commit()

        return jsonify({"message": "Registro de teste inserido com sucesso!"}), 201
    except Error as e:
        print(e)
        return jsonify({'message': 'Erro ao inserir registro de teste na tabela tbl_cadastro.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)