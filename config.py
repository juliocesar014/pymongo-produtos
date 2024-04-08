from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

# Conexões com os bancos de dados MySQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sua_senha@localhost/nome_do_banco_de_dados'
# SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1:3306/banco_web'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/banco_web'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/banco_web'
# mysql = SQLAlchemy(app)


# Conexão com MongoDB
cliente = MongoClient("mongodb://localhost:27017") # conexão com servidor
mongodb = cliente["banco_web"] # selecionando BD
pedidos_collection = mongodb["pedidos"] # selecionando collection
