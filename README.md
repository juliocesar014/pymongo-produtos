# Bem-vindo a API de Produtos. Um CRUD de Produtos, Clientes e Pedidos
Este projeto foi desenvolvido ao longo das aulas de Modelagem de Banco de dados da Pós em ## Desenvolvimento Web Full Stack da UNIPÊ ##
O projeto lida com uma persistência poliglota, com dados em um banco relacional e um não relacional.

1. Relacional MySQL com as tabelas:
   - Produtos (que mantém): ID_produto, Nome, Descricao, Categoria e Preço
   - Clientes: ID_cliente, Nome, Email, CPF e Data de Nascimento
  
2. Não reacional MongoDB com a coleção:
   - Pedidos: ID_produto, ID_Cliente, Data_pedido, Valor_pedido
  
O projeto foi implementado em Python com uso do Flask. As dependências e pacotes utilizados estão no arquivo requirements.txt
