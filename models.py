import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Carteira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), default='Cold')
    # Relacionamento: permite acessar transações de uma carteira facilmente
    transacoes = db.relationship('Transacao', backref='carteira', lazy=True)

    @property
    def saldo_total(self):
        """Soma a quantidade total de BTC acumulada na carteira."""
        return sum(t.quantidade_btc for t in self.transacoes)
    
    @property
    def valor_investido_total(self):
        """Calcula o custo total de aquisição em BRL (Custo Histórico)."""
        return sum(t.quantidade_btc * t.preco_unitario_fiat for t in self.transacoes)

    @property
    def preco_medio(self):
        """Preço Médio = Total Gasto / Quantidade Acumulada."""
        total_btc = self.saldo_total
        if total_btc == 0:
            return 0
        return self.valor_investido_total / total_btc

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantidade_btc = db.Column(db.Float, nullable=False)
    preco_unitario_fiat = db.Column(db.Float, nullable=False) 
    carteira_id = db.Column(db.Integer, db.ForeignKey('carteira.id'), nullable=False)



