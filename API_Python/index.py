# MODULOS
# Para errores - pip install pylint

# Se llama al Framework y se inicializa
from flask import Flask, render_template

# Módulo para mysql - pip install mysqlclient
import MySQLdb

# Módulo para MongoDB - pip install pymongo
# import pymongo

# Credenciales 
# MySQL
# DB_HOST = '34.135.208.19' 
# DB_USER = 'root' 
# DB_PASS = 'dbace2p1' 
# DB_NAME = 'db2proyecto1' 

# Conexión con MySQL
def run_query(query=''): 
    # Credenciales
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
    
    conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
    
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    return data

# Conexión con MongoDB
def getDatabase():
    # Import inicial
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://bd-proyecto1:L2XNwzBGxhRGLChvwUfUdhG18ZfccuKQDoIdRZyPFWGgpSsDNvn9QsLu3wK3PQ9geyPRGSg1fywKZUuh2JO3YA==@bd-proyecto1.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@bd-proyecto1@"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['Clase7']

# Se designa que este es el archivo principal, el que va a arrancar la aplicación
# app va a ser la variable que permitirá crear las rutas del servidor, URL, etc
app = Flask(__name__)

# ------------------------- RUTAS -------------------------
# Para crear una ruta primero se utiliza un decorador @
@app.route('/')
def home():
    # Get the database
    dbname = getDatabase()

    # Get the collection
    collection_name = dbname["data"]

    # Dato a introducir
    item_3 =  {
    "nombre": "Sebastian",
    "comentario": "Tweet:5",
    "hashtags": [
        "tweet5"
    ],
    "upvotes": 30,
    "downvotes": 27
    }

    collection_name.insert_one(item_3)

    return 'Hola'
@app.route('/iniciarCarga')
def iniciarCarga():
    return render_template('iniciarCarga.html')
@app.route('/publicar')
def publicar():
    return render_template('about.html')
@app.route('/finalizarCarga')
def finalizarCarga():
    return render_template('about.html')

# ------------------------- MÉTODO PRINCIPAL -------------------------
if(__name__ == '__main__'):
    app.run(debug=True)