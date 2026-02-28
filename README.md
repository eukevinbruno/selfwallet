# ₿ SelfWallet - Private Bitcoin Tracker

**SelfWallet** é uma ferramenta soberana e privada para acompanhamento de portfólio de Bitcoin. Esqueça planilhas complexas ou aplicativos que espionam seus dados. Aqui, suas informações ficam no **seu** computador.

## 🚀 Funcionalidades Principais

- **Gestão por Carteiras Estratégicas**: Organize seus satoshis entre "Receita Federal", "Negação Plausível" e "HODL".
- **Cálculo de Preço Médio (Breakeven)**: Saiba exatamente qual o seu custo médio de compra para tomar decisões inteligentes.
- **Modo Ghost (Privacidade)**: Esconda seus saldos com um clique para poder usar o app em locais públicos.
- **Conversão SATS/BTC**: Alterne a visualização entre frações de Bitcoin ou unidades inteiras de Satoshis.
- **Exportação Inteligente**: Gere extratos em Excel (.xlsx) de cada carteira para conferência ou backup manual.
- **Operação Offline**: O sistema armazena o último preço conhecido. Se estiver sem internet, seus dados continuam lá.

## 🛠️ Como Usar (Versão Executável)

1.  Extraia o conteúdo do arquivo `.zip` para uma pasta de sua preferência.
2.  Execute o arquivo `SelfWallet_Pro.exe`.
3.  O navegador abrirá automaticamente no endereço `http://127.0.0.1:5000`.
4.  **Importante**: A pasta `instance` que será criada contém o seu banco de dados (`carteira.db`). **Nunca a delete** se quiser manter seu histórico.

## 📁 Estrutura do Projeto (Desenvolvimento)

Para rodar via código fonte:

```bash
.
├── app.py              # Lógica principal e rotas
├── models.py           # Definição do banco de dados e cálculos
├── static/             # CSS, JS (Chart.js) e Imagens
├── templates/          # Páginas HTML (Jinja2)
└── instance/           # Banco de dados e configurações (criado ao rodar)
```
