import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# 1. Primeiro definimos os caminhos corretos (Tudo em minúsculo para padronizar)
base_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(base_dir, 'contratos.db')

# 2. Depois inicializamos a aplicação Flask configurando as pastas
app = Flask(__name__,
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))

# 3. Agora sim definimos a chave secreta com o app já criado
app.secret_key = "chave-secreta-para-sistema-financeiro-databill"


def init_db():
    """Garante que a tabela de dados está criada no SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_contrato TEXT NOT NULL,
            nome_cliente TEXT NOT NULL,
            email_notificacao TEXT NOT NULL,
            dia_faturamento INTEGER NOT NULL,
            dia_alerta INTEGER NOT NULL,
            possui_printwayy BOOLEAN NOT NULL,
            data_inicio TEXT NOT NULL,
            meses_duracao INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    """Entrega a pagina de faturamento index.html para o navegador"""
    return render_template('index.html')

@app.route('/api/contratos', methods=['GET'])
def listar_contratos():
    """Busca todos os contratos registrados no SQLite para listar na tabela"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contratos')
    linhas = cursor.fetchall()
    conn.close()

    contratos = []
    for r in linhas:
        contratos.append({
            'id': r[0],
            'numero_contrato': r[1],
            'nome_cliente': r[2],
            'email_notificacao': r[3],
            'dia_faturamento': r[4],
            'dia_alerta': r[5],
            'possui_printwayy': bool(r[6]),
            'data_inicio': r[7],
            'meses_duracao': r[8]
        })
    return jsonify(contratos)

@app.route('/api/contratos', methods=['POST'])
def adicionar_contrato():
    """Recebe o contrato enviado pelo HTML e salva fisicamente no SQLite"""
    dados = request.json
    hoje = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contratos (numero_contrato, nome_cliente, email_notificacao, dia_faturamento, dia_alerta, possui_printwayy, data_inicio, meses_duracao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dados['numero_contrato'],
        dados['nome_cliente'],
        dados['email_notificacao'],
        dados['dia_faturamento'],
        dados['dia_alerta'],
        dados['possui_printwayy'],
        hoje,
        dados['meses_duracao']
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

@app.route('/api/contratos/<int:id>', methods=['DELETE'])
def deletar_contrato(id):
    """Deleta uma linha de faturamento usando seu identificador ID no SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contratos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

# Inicializacao do servidor

@app.route('/api/contratos/<int:id>/enviar-alerta', methods=['POST'])
def enviar_alerta(id):
    """Simula o envio de um e-mail de alerta de faturamento para o cliente"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT numero_contrato, nome_cliente, email_notificacao, dia_faturamento FROM contratos WHERE id = ?', (id,))
    contrato = cursor.fetchone()
    conn.close()

    if not contrato:
        return jsonify({'status': 'erro', 'mensagem': 'Contrato não encontrado'}), 404

    numero_contrato, nome_cliente, email_notificacao, dia_faturamento = contrato

    # --- SIMULAÇÃO DE ENVIO DE E-MAIL (MOCK) ---
    print("\n" + "="*50)
    print("📧 [SIMULAÇÃO DE DISPARO DE E-MAIL]")
    print(f"Para: {email_notificacao}")
    print(f"Assunto: 🚨 ALERTA DATABILL - Faturamento Contrato Nº {numero_contrato}")
    print("-"*50)
    print(f"Olá, {nome_cliente},\n")
    print(f"Este é um lembrete automático do sistema DataBill.")
    print(f"O faturamento do seu contrato número {numero_contrato} está agendado para o dia {dia_faturamento}.")
    print("Por favor, verifique se a validação do PrintWayy foi concluída com sucesso.")
    print("\nAtenciosamente,\nEquipa de Faturamento DataBill")
    print("="*50 + "\n")
    # --------------------------------------------

    return jsonify({'status': 'sucesso', 'mensagem': f'E-mail simulado com sucesso para {email_notificacao}!'})


if __name__ == '__main__':
    init_db()
    print("Banco de dados local contratos.db pronto!")
    app.run(debug=True, port=5000)
