# --------------------------------------------- MODULOS ---------------------------------------------
# Para errores - pip install pylint

# Se llama al Framework y se inicializa
from flask import Flask, request, render_template

# Módulo para mysql
import MySQLdb

# --------------------------------------------- FUNCIONES ---------------------------------------------
# Conexión con MySQL
def GetMySQL(query=''): 
    # Credenciales
    DB_HOST = '35.238.36.76' 
    DB_USER = 'root' 
    DB_PASS = 'dbsopes1' 
    DB_NAME = 'sopes1data'
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
    
    # Se conecta a la DB y se crea un cursor
    conn = MySQLdb.connect(*datos)
    cursor = conn.cursor()

    # Se ejecuta una consulta
    cursor.execute(query)

    # Si es un select se traen todos los resultados, de lo contrario es una escritura de datos
    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()
    else: 
        conn.commit()
        data = None 
    
    # Se cierra el cursor y la conexión
    cursor.close()
    conn.close()

    return data

# Conexión con MongoDB, aquí se utiliza el módulo MongoDB pip install pymongo - pip install dnspython
def GetMongo():
    # Import inicial
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://bd-proyecto1:L2XNwzBGxhRGLChvwUfUdhG18ZfccuKQDoIdRZyPFWGgpSsDNvn9QsLu3wK3PQ9geyPRGSg1fywKZUuh2JO3YA==@bd-proyecto1.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@bd-proyecto1@"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example
    return client['Clase7']

# Se designa que este es el archivo principal, el que va a arrancar la aplicación
# app va a ser la variable que permitirá crear las rutas del servidor, URL, etc
app = Flask(__name__)

# --------------------------------------------- RUTAS ---------------------------------------------
# Para crear una ruta primero se utiliza un decorador @
@app.route('/')
def home():
    return 'Hola'
@app.route('/iniciarCarga', methods=["POST"])
def iniciarCarga():
    # Se decodifica el JSON recibido, get_json() hace un parsing
    jsonres = request.get_json()

    # ----------------------------- MONGO -----------------------------
    # Get the database
    dbname = GetMongo()

    # Get the collection
    collection_name = dbname["data"]

    # Se realiza la inserción en la conexión correspondiente
    collection_name.insert_one(jsonres)

    # ----------------------------- MYSQL -----------------------------
    # Se prepara el primer query y se llama a la función de inserción de usuario y tweet
    query = "CALL PROC2('{0}', '{1}', CURDATE(), {2}, {3});".format(jsonres["nombre"], jsonres["comentario"], jsonres["upvotes"], jsonres["downvotes"])
    data1 = GetMySQL(query)

    # Se prepara el segundo query y se llama a la función de selección del último tweet
    query2 = "SELECT Id_tweet FROM Tweet ORDER BY Id_tweet DESC LIMIT 1;"
    idretornado = GetMySQL(query2)

    # Se hará una inserción por cada dato de la lista en el json
    for i in range (0, len(jsonres["hashtags"])):
        # Se prepara el tercer query y se llama a la función de inserción de hashtag
        query3 = "CALL PROC1({0}, '{1}');".format(idretornado[0][0], jsonres['hashtags'][i])
        inhashtag = GetMySQL(query3)

    return 'Carga completada'
@app.route('/publicar')
def publicar():
    return 'Publicar'
    # return render_template('publicar.html')
@app.route('/finalizarCarga')
def finalizarCarga():
    return 'Finalizar Carga'
    # return render_template('about.html')

# ------------------------- MÉTODO PRINCIPAL -------------------------
if(__name__ == '__main__'):
    app.run(debug=True)
