from flask import render_template, request, Blueprint, jsonify
from models.db import cursor, conn
from datetime import datetime

cliente = Blueprint(
    "cliente",
    __name__
)

@cliente.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@cliente.route("/pedidos", methods=["GET"])
def pedidos():
    return render_template('pedidos.html')

@cliente.route("/buscar_pedidos", methods=["GET"])
def buscar_pedidos():
    try:
        cursor.execute("""
    SELECT id, cliente, produto, entregue
    FROM pedidosclientes
    WHERE data::date = CURRENT_DATE
      AND entregue = FALSE
""")

        resultados = cursor.fetchall()
        pedidos = [{"id": r[0], "cliente": r[1], "produto": r[2], "entregue": r[3]} for r in resultados]
        return jsonify(pedidos)
    except Exception as e:
        conn.rollback()
        print("Erro ao buscar pedidos:", e)
        return jsonify({"erro": "Erro ao buscar pedidos"}), 500

@cliente.route("/pedir", methods=["POST"])
def pedir():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400
    nome = dados.get("nome")
    produto = dados.get("produto")
    data = datetime.now()
    if not nome or not produto:
        return jsonify({"erro": "Dados incompletos"}), 400
    try:
        cursor.execute("""
            INSERT INTO pedidosclientes (cliente, produto, data)
            VALUES (%s, %s, %s)
        """, (nome, produto, data))
        conn.commit()
        return jsonify({"status": "ok"})
    except Exception as e:
        conn.rollback()
        print("Erro no banco:", e)
        return jsonify({"erro": "Erro ao salvar pedido"}), 500

@cliente.route("/marcar_entregue", methods=["POST"])
def marcar_entregue():
    dados = request.get_json()
    if not dados or "id" not in dados:
        return jsonify({"erro": "ID do pedido necessário"}), 400
    pedido_id = dados["id"]
    try:
        cursor.execute("""
            UPDATE pedidosclientes
            SET entregue = TRUE
            WHERE id = %s
        """, (pedido_id,))
        conn.commit()
        return jsonify({"status": "ok"})
    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar pedido:", e)
        return jsonify({"erro": "Erro ao atualizar pedido"}), 500

@cliente.route("/pagamento", methods=["POST"])
def pagamento():
    dados = request.get_json()

    cliente = dados.get("nome")
    montante = dados.get("montante")
    
    try:
        cursor.execute(""" 
            INSERT INTO pagamentos (cliente,montante)
            VALUES (%s , %s)
            RETURNING id
        """, (cliente,montante))
        pagamento_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({
            "status" : "ok",
            "id_pag" : pagamento_id
            })
    except Exception as e:
            conn.rollback()
            print("Erro ao inserir o pagamento no banco:", e)
            return jsonify({"erro": "Erro ao inserir o pagamento no banco"}), 500
        

