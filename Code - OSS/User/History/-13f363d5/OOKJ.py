import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Inicializando a aplicacao Flask
app = Flask(__name__, template_folder='.')
app.secret_key = "chave-secreta-para-sistema-financeiro-databill"

# Define o caminho do arquivo do banco de dados SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'contratos.db')

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
if __name__ == '__main__':
    init_db()
    print("Banco de dados local contratos.db pronto!")
    app.run(debug=True, port=5000)