# ₿ SelfWallet Pro - Private Edition

> **Sua soberania financeira em uma interface de elite.**

O **SelfWallet** é um ecossistema de gestão financeira offline, focado em privacidade, agilidade e controle total. Esqueça trackers que vendem seus dados; aqui, o único dono da informação é você.

---

## 🚀 Diferenciais da Versão Desktop

- **Interface Nativa**: Janela dedicada e independente, sem necessidade de abrir o navegador.
- **Sem Vazamentos**: Persistência de dados local via banco de dados SQLite LOCAL.
- **Privacidade Total**: Seus dados financeiros e arquivos nunca saem da sua máquina.
- **Portabilidade Suprema**: Um único arquivo `.exe` que carrega todo o poder do sistema.
- **Gestão de Cartões**: Controle de parcelas e vencimentos com projeção de faturas futuras.

---

## 🛠️ Como Utilizar

Você não precisa instalar Python, bibliotecas ou bancos de dados. O SelfWallet Pro é entregue como um executável pronto para o combate.

1.  **Download**: Obtenha o arquivo `SelfWallet.exe`.
2.  **Localização**: Coloque-o em uma pasta de sua preferência (ex: `C:\Software\SelfWallet`).
3.  **Execução**: Dê um duplo clique no arquivo.
    - _Nota: Na primeira execução, o sistema criará automaticamente as pastas `/instance` e `/static/uploads` ao lado do executável para garantir a persistência dos seus dados._

---

## 🔑 Acesso Inicial (Configuração de Fábrica)

Ao abrir o app pela primeira vez, utilize as credenciais padrão do sistema:

- **Usuário**: `admin`
- **Senha**: `admin`

> **⚠️ IMPORTANTE**: Recomendamos alterar seu nome de usuário e senha imediatamente na aba **"Usuário"** para garantir sua segurança pessoal.

---

## 📂 Estrutura de Diretórios

Para que o software funcione corretamente e não perca informações, mantenha a seguinte estrutura:

- 📂 **SelfWallet/**
  - 📄 `SelfWallet.exe` (O coração do sistema)
  - 📂 `instance/` (Contém seu banco de dados `carteira.db` — **NÃO DELETA**)
  - 📂 `instance/config.json` (Armazena suas preferências como a visualização em Sats ou em BTC)

---

## 🛡️ Segurança e Backup

Como o SelfWallet sé **100% offline**, o backup é responsabilidade sua:

1.  Para fazer backup, basta copiar a pasta `instance` para um pendrive ou nuvem segura.
2.  Se precisar trocar de computador, basta levar o `.exe` e a pasta `instance` junto. Tudo estará lá exatamente como você deixou.

---

_Desenvolvido para quem entende que privacidade não é apenas um recurso, é um direito fundamental._ 🥂
