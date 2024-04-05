from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Date

from config import SQLALCHEMY_DATABASE_URI, mongodb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
mysql = SQLAlchemy(app)
pedidos_collection = mongodb["pedidos"] # selecionando collection

# Definindo as classes para Produtos, Clientes e Pedidos
# Defina seus modelos de produto e cliente (SQL)
class Produtos(mysql.Model):
    id_produto = mysql.Column(Integer, primary_key=True)
    nome = mysql.Column(String)
    descricao = mysql.Column(String)
    preco = mysql.Column(Float)
    categoria = mysql.Column(String)

    def serialize(self):
        return {
            "id": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "categoria": self.categoria
        }

class Clientes(mysql.Model):
    id_clientes = mysql.Column(Integer, primary_key=True)
    nome = mysql.Column(String)
    email = mysql.Column(String)
    cpf = mysql.Column(String)
    data_nascimento = mysql.Column(Date)

    def serialize(self):
        return {
            "id_clientes": self.id_clientes,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento
        }
# Definindo a classe PEDIDOS
# Será persistida no MongoDB
class Pedidos:
    def __init__(self, id_pedido, id_cliente, id_produto, data_pedido, valor_pedido):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.data_pedido = data_pedido
        self.valor_pedido = valor_pedido

    def serialize(self):
        return {
            "id_pedido": self.id_pedido,
            "id_cliente": self.id_cliente,
            "id_produto": self.id_produto,
            "data_pedido": self.data_pedido,
            "valor_pedido": self.valor_pedido,
        }

# Rotas para CRUD de produtos (MySQL)

@app.route("/produtos", methods=["GET"])
def get_produtos():
    # Criando objeto que recebe os dados
    produtos = Produtos.query.all()
    # Serializa para JSON
    return jsonify([produto.serialize() for produto in produtos])

# Rotas para Create, Update e Delete de produtos)
@app.route("/produtos/", methods=['POST'])
def set_produto():
    # Obtendo e cadastrando dados na tabela PRODUTOS
    dados = request.get_json()
    produto = Produtos(nome=dados["nome"],
                       descricao=dados['descricao'],
                       preco=dados["preco"],
                       categoria=dados["categoria"])
    mysql.session.add(produto)
    mysql.session.commit()
    return jsonify(produto.serialize()), 201

@app.route("/produto/<int:id>", methods=["PUT"])
def update_produto(id):
    try:
        dados = request.get_json()

        produto = mysql.session.query(Produtos).get(id)
        produto.nome = dados["nome"]
        produto.descricao = dados["descricao"]
        produto.preco = dados["preco"]
        produto.categoria = dados["categoria"]

        mysql.session.commit()
        return jsonify(produto.serialize()), 201
    except Exception as e:
        print(f"Error: {e}")
        return "Erro ao alterar os dados", 400

@app.route("/produto/<int:id>", methods=["DELETE"])
def delete_produto(id):
    try:
        produto = mysql.session.query(Produtos).get(id)
        mysql.session.delete(produto)
        mysql.session.commit()
        return jsonify({'Excluido com sucesso.'}), 204
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao excluir produto", 400

# Rotas para CRUD de clientes (MySQL)

@app.route("/clientes", methods=["GET"])
def get_clientes():
    clientes = Clientes.query.all()
    return jsonify([cliente.serialize() for cliente in clientes])

# Rotas para Create, Update e Delete de clientes

# Rotas para CRUD de Pedidos (MongoDB)

@app.route("/pedidos", methods=["GET"])
def get_pedidos():
    pedidos = pedidos_collection.find()
    return jsonify([dict(pedido) for pedido in pedidos])

# Rotas para Create, Update e Delete de pedidos)
@app.route("/pedido", methods=["POST"])
def set_pedido():
    try:
        dados = request.get_json()
        pedido = Pedidos(dados["id_produto"],dados['id_cliente'],dados["data_pedido"],dados["valor_pedido"])
        pedidos_collection.insert_one(pedido.serialize())
        return jsonify(pedido.serialize()), 201
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao inserir pedido.", 400

if __name__ == "__main__":
    app.run(debug=True)
