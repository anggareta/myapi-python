from flask import Flask, request, jsonify
import requests
import pandas as pd
import pyodbc


app = Flask(__name__)

server = '127.0.0.1'  # contoh: 'localhost\SQLEXPRESS'
database = 'Emp'
username = 'sa'
password = 'P@ssw0rd'

connstr = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Membuat koneksi
try:
    connection = pyodbc.connect(connstr)
    print("Koneksi berhasil!")
except Exception as e:
    print("Koneksi gagal:", e)

@app.route("/")
def hello_world():
    return "<h1>Hello World!</h1>"


@app.route("/baca")
def baca():
    conn = pyodbc.connect(connstr)
    query = "SELECT * FROM Employees order by ID"
    df = pd.read_sql_query(query, conn)

    json_data = df.to_json(orient='records')
    return jsonify(eval(json_data))

@app.route("/bacasatu/<path:id>", methods=['GET'])
def bacasatu(id):
    print(id)
    conn = pyodbc.connect(connstr)
    query = f"SELECT * FROM Employees where ID = {id}"
    df = pd.read_sql_query(query, conn)

    json_data = df.to_json(orient='records')
    return jsonify(eval(json_data)[0])

@app.route("/tulis", methods=['POST'])
def tulis():
    data = request.get_json()
    # print(data)
    try:
        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        cursor.execute(f"EXEC [usp_InsertEmployeeTest] @Name = ?, @Location = ?", data['Name'], data['Location'])
        r = 0
        column = cursor.description[r][0]
        value = cursor.fetchone()[r]
        conn.commit()
    except pyodbc.Error as e:
        print("Error executing stored procedure:", e)
    finally:
        cursor.close()
        conn.close()

    return {column: value}