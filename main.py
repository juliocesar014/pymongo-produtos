from bson import ObjectId
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Date

from config import SQLALCHEMY_DATABASE_URI, pedidos_collection

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
mysql = SQLAlchemy(app)

# Definindo as classes para Produtos, Clientes e Pedidos
# Definindo seus modelos de produto e cliente (SQL)
class Produtos(mysql.Model):
    id_produtos = mysql.Column(Integer, primary_key=True)
    nome = mysql.Column(String)
    descricao = mysql.Column(String)
    preco = mysql.Column(Float)
    categoria = mysql.Column(String)

    def serialize(self):
        return {
            "id": self.id_produtos,
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
# Aqui utilizados o Contrutor para definir os atributos da classe
class Pedidos:
    def __init__(self, id_cliente, id_produto, data_pedido, valor_pedido):
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.data_pedido = data_pedido
        self.valor_pedido = valor_pedido

    def serialize(self):
        return {
            "id_cliente": self.id_cliente,
            "id_produto": self.id_produto,
            "data_pedido": self.data_pedido,
            "valor_pedido": self.valor_pedido,
        }

# Rotas para CRUD de produtos (MySQL)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "API Online"}), 200

@app.route("/produtos", methods=["GET"])
def get_produtos():
    # Criando objeto que recebe os dados
    produtos = Produtos.query.all()
    # Serializa para JSON
    return jsonify([produto.serialize() for produto in produtos])

# Rotas para Create, Update e Delete de produtos)
@app.route("/produtos", methods=['POST'])
def set_produto():
    try:
        # Obtendo e cadastrando dados na tabela PRODUTOS
        dados = request.get_json()
        produto = Produtos(nome=dados["nome"],
                           descricao=dados['descricao'],
                           preco=dados["preco"],
                           categoria=dados["categoria"])
        mysql.session.add(produto)
        mysql.session.commit()
        return jsonify(produto.serialize()), 201
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao cadastrar Produto.", 400

@app.route("/produtos/<int:id>", methods=["PUT"])
def update_produto(id):
    try:
        # Retornando os dados em JSON para atualização
        dados = request.get_json()

        # Preparando os dados recebidos para ser dado o UPDATE
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

@app.route("/produtos/<int:id>", methods=["DELETE"])
def delete_produto(id):
    try:
        # Definindo o objeto para manipular o registro pelo ID
        produto = mysql.session.query(Produtos).get(id)
        mysql.session.delete(produto)
        mysql.session.commit()
        return "", 204
    except Exception as e:
        print(f"Erro: {e}")
        return "Produto não existe", 400

# Rotas para CRUD de clientes (MySQL)

@app.route("/clientes", methods=["GET"])
def get_clientes():
    clientes = Clientes.query.all()
    return jsonify([cliente.serialize() for cliente in clientes])

## Aqui definiremos as Rotas para Create, Update e Delete de clientes

@app.route("/clientes", methods=["POST"])
def set_cliente():
    try:
        dados = request.get_json()
        cliente = Clientes(nome=dados["nome"],
                            email=dados['email'],
                            cpf=dados["cpf"],
                            data_nascimento=dados["data_nascimento"])
        mysql.session.add(cliente)
        mysql.session.commit()
        return jsonify(cliente.serialize()), 201
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao cadastrar Cliente.", 400

@app.route("/clientes/<int:id>", methods=["PUT"])
def update_cliente(id):
    try:
        dados = request.get_json()
        cliente = mysql.session.query(Clientes).get(id)
        cliente.nome = dados["nome"]
        cliente.email = dados["email"]
        cliente.cpf = dados["cpf"]
        cliente.data_nascimento = dados["data_nascimento"]

        mysql.session.commit()
        return jsonify(cliente.serialize()), 201
    except Exception as e:
        print(f"Error: {e}")
        return "Erro ao alterar os dados", 400
    
    
@app.route("/clientes/<int:id>", methods=["DELETE"])
def delete_cliente(id):
    try:
        cliente = mysql.session.query(Clientes).get(id)
        mysql.session.delete(cliente)
        mysql.session.commit()
        return "", 204
    except Exception as e:
        print(f"Erro: {e}")
        return "Cliente não existe", 400
    


# Rotas para CRUD de Pedidos
# Rotas feitas para manipular os dados através do MongoDB


@app.route("/pedidos", methods=["GET"])
def get_pedidos():
    try:
        pedidos = pedidos_collection.find()

        lista_pedidos = [pedido for pedido in pedidos]

        for pedido in lista_pedidos:
            pedido["_id"] = str(pedido["_id"])

        return jsonify(lista_pedidos), 200

    except Exception as e:
        print(f"Erro: {e}")
        return f"Erro ao buscar pedidos: {e}", 500


# Rotas para Create, Update e Delete de pedidos)
@app.route("/pedidos", methods=["POST"])
def set_pedido():
    try:
        dados = request.get_json()
        novo_pedido = Pedidos(
            id_produto=dados["id_produto"],
            id_cliente=dados['id_cliente'],
            data_pedido=dados["data_pedido"],
            valor_pedido=dados["valor_pedido"]
        )
        resultado = pedidos_collection.insert_one(novo_pedido.serialize())
        if resultado.inserted_id:
            # Retorna o pedido recém-criado e o status 201
            novo_pedido.id_pedido = str(resultado.inserted_id)
            return jsonify(novo_pedido.serialize()), 201
        else:
            return "Erro ao inserir pedido.", 500
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao inserir pedido.", 400

@app.route("/pedidos/<pedido_id>", methods=['DELETE'])
def delete_pedido(pedido_id):
    try:
        if not ObjectId.is_valid(pedido_id):
            return "ID de pedido inválido.", 400

        resultado = pedidos_collection.delete_one({"_id": ObjectId(pedido_id)})

        # Verifica se o pedido foi encontrado e excluído
        if resultado.deleted_count == 1:
            return (f"Pedido com ID {pedido_id} excluído com sucesso."), 200
        else:
            return (f"Pedido com ID {pedido_id} não encontrado."), 404
    except Exception as e:
        return f"Erro ao excluir pedido: {e}", 500

@app.route("/pedidos/<pedido_id>", methods=["PUT"])
def update_pedido(pedido_id):
    try:
        if not ObjectId.is_valid(pedido_id):
            return "ID de pedido inválido.", 400

        # Obtém os novos dados do pedido do corpo da solicitação
        dados = request.get_json()

        # Atualiza o pedido no banco de dados
        resultado = pedidos_collection.update_one(
            {"_id": ObjectId(pedido_id)},
            {"$set": dados}  # Use $set para atualizar apenas os campos fornecidos
        )

        # Verifica se o pedido foi encontrado e atualizado
        if resultado.modified_count == 1:
            return f"Pedido com ID {pedido_id} atualizado com sucesso.", 200
        else:
            return f"Pedido com ID {pedido_id} não encontrado ou nenhum dado foi modificado.", 404
    except Exception as e:
        return f"Erro ao atualizar pedido: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

