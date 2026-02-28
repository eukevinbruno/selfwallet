from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
from models import db, Carteira, Transacao
from datetime import datetime
import os
import pandas as pd
import io
import json
import requests

app = Flask(__name__)

# --- CONFIGURAÇÃO DE CAMINHOS (Compatível com PyInstaller) ---
basedir = os.path.abspath(os.path.dirname(__file__))
INSTANCE_PATH = os.path.join(basedir, 'instance')
CONFIG_PATH = os.path.join(INSTANCE_PATH, 'config.json')
DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_PATH, 'carteira.db')

if not os.path.exists(INSTANCE_PATH):
    os.makedirs(INSTANCE_PATH)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- INICIALIZAÇÃO DO BANCO ---
with app.app_context():
    db.create_all()
    carteiras_obrigatorias = [
        {'nome': 'Receita Federal', 'tipo': 'Cold'},
        {'nome': 'Negação Plausível', 'tipo': 'Hot'},
        {'nome': 'Carteira Hold', 'tipo': 'Cold'}
    ]
    for c_info in carteiras_obrigatorias:
        if not Carteira.query.filter_by(nome=c_info['nome']).first():
            db.session.add(Carteira(nome=c_info['nome'], tipo=c_info['tipo']))
    db.session.commit()

# --- LÓGICA DE CONFIGURAÇÃO E COTAÇÃO ---
def carregar_config():
    if not os.path.exists(CONFIG_PATH) or os.path.getsize(CONFIG_PATH) == 0:
        default = {"unit": "BTC", "privacy": False, "last_price": 550000.0}
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default, f)
        return default
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except:
        return {"unit": "BTC", "privacy": False, "last_price": 550000.0}

def pegar_cotacao():
    try:
        response = requests.get('https://api.coinbase.com/v2/prices/BTC-BRL/spot', timeout=3)
        preco = float(response.json()['data']['amount'])
        config = carregar_config()
        config['last_price'] = preco
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f)
        return preco
    except:
        config = carregar_config()
        return config.get('last_price', 0.0)

# --- ROTAS ---
@app.route('/')
def home():
    preco_atual = pegar_cotacao()
    todas_carteiras = Carteira.query.all()
    return render_template('home.html', carteiras=todas_carteiras, preco=preco_atual)

@app.route('/api/config', methods=['GET', 'POST'])
def gerenciar_config():
    if request.method == 'POST':
        data = request.get_json()
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f)
        return jsonify({"status": "sucesso"})
    return jsonify(carregar_config())

@app.route('/api/alocacao')
def api_alocacao():
    carteiras = Carteira.query.all()
    preco_atual = pegar_cotacao()
    nomes, valores_atuais, valores_btc, investimentos = [], [], [], []
    total_btc = 0
    
    for c in carteiras:
        nomes.append(c.nome)
        # Importante: enviar o valor fiat para o gráfico e o btc para os cards
        valores_atuais.append(float(c.saldo_total * preco_atual)) 
        valores_btc.append(float(c.saldo_total)) # <--- ADICIONADO PARA O TOPO
        investimentos.append(float(c.valor_investido_total))
        total_btc += float(c.saldo_total)

    return jsonify({
        'labels': nomes,
        'values': valores_atuais,
        'values_btc': valores_btc, # <--- ESSA LINHA CURA O ERRO DO GRÁFICO
        'investimentos': investimentos,
        'total_btc_global': total_btc
    })

@app.route('/api/carteira/<int:id>')
def api_carteira(id):
    c = Carteira.query.get_or_404(id)
    preco_atual = pegar_cotacao()
    return jsonify({
        'nome': c.nome,
        'investido': c.valor_investido_total,
        'medio': c.preco_medio,
        'atual': c.saldo_total * preco_atual,
        'transacoes': [{
            'id': t.id,
            'data': t.data_compra.strftime('%d/%m/%Y %H:%M'),
            'qtd': t.quantidade_btc,
            'preco': t.preco_unitario_fiat
        } for t in c.transacoes]
    })

@app.route('/deletar_transacao/<int:id>', methods=['POST'])
def deletar_transacao(id):
    t = Transacao.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"status": "sucesso"})

@app.route('/nova_transacao', methods=['GET', 'POST'])
def nova_transacao():
    if request.method == 'POST':
        nova_t = Transacao(
            quantidade_btc=float(request.form.get('quantidade')),
            preco_unitario_fiat=float(request.form.get('preco_unitario')),
            data_compra=datetime.strptime(request.form.get('data_compra'), '%Y-%m-%dT%H:%M') if request.form.get('data_compra') else datetime.utcnow(),
            carteira_id=request.form.get('carteira_id')
        )
        db.session.add(nova_t)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('transacao.html', carteiras=Carteira.query.all())

@app.route('/exportar/<int:id>')
def exportar_excel(id):
    c = Carteira.query.get_or_404(id)
    df = pd.DataFrame([{
        'Data': t.data_compra.strftime('%d/%m/%Y'),
        'Quantidade (BTC)': float(t.quantidade_btc),
        'Preço Unitário (BRL)': round(float(t.preco_unitario_fiat), 2),
        'Custo Total (BRL)': round(float(t.quantidade_btc * t.preco_unitario_fiat), 2)
    } for t in c.transacoes])
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Transacoes')
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=f"extrato_{c.nome.lower()}.xlsx")

@app.route('/backup-db')
def backup_db():
    return send_file(os.path.join(INSTANCE_PATH, 'carteira.db'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)