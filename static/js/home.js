/**
 * SelfWallet v1.0 - Motor JS Definitivo
 */

let currentUnit = "BTC";
let privacyMode = false;
let meuGrafico = null;
let carteiraAbertaAtualmente = null;

const formatBRL = (v) =>
  Number(v).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
    minimumFractionDigits: 2,
  });

// 1. SINCRONIZAÇÃO TOTAL (TOP CARDS + GRÁFICO)
async function inicializarDashboard() {
  try {
    const [confRes, alocRes] = await Promise.all([
      fetch("/api/config"),
      fetch("/api/alocacao"),
    ]);

    const config = await confRes.json();
    const data = await alocRes.json();

    currentUnit = config.unit || "BTC";
    privacyMode = config.privacy || false;
    document.body.classList.toggle("privacy-on", privacyMode);

    // ATUALIZA OS CARDS DO TOPO PELO ID (saldo-1, saldo-2, saldo-3)
    data.values_btc.forEach((valor, index) => {
      const idNum = index + 1;
      const el = document.getElementById(`saldo-${idNum}`);
      const label = document.getElementById(`unit-${idNum}`);

      if (el) {
        el.setAttribute("data-btc", valor);
        el.setAttribute("data-sats", Math.round(valor * 100000000));

        if (currentUnit === "SATS") {
          el.innerText = Math.round(valor * 100000000).toLocaleString("pt-BR");
          if (label) label.innerText = "SATS";
        } else {
          el.innerText = parseFloat(valor).toFixed(8);
          if (label) label.innerText = "BTC";
        }
      }
    });

    // Atualiza Consolidado
    const totalBRL = data.values.reduce((a, b) => a + b, 0);
    const btcGeral = data.total_btc_global;
    const investidoGeral = data.investimentos.reduce((a, b) => a + b, 0);

    document.getElementById("total-geral-brl").innerText = formatBRL(totalBRL);
    document.getElementById("total-geral-medio").innerText = formatBRL(
      btcGeral > 0 ? investidoGeral / btcGeral : 0,
    );

    renderizarGrafico(data);
  } catch (err) {
    console.error("Erro no refresh:", err);
  }
}

// 2. GESTÃO DE DETALHES E DELEÇÃO
async function mostrarDetalhes(id) {
  carteiraAbertaAtualmente = id;
  document.getElementById("placeholder-msg").style.display = "none";
  document.getElementById("conteudo-detalhes").style.display = "block";

  const res = await fetch(`/api/carteira/${id}`);
  const data = await res.json();

  document.getElementById("detalhe-nome").innerText = data.nome;
  document.getElementById("detalhe-investido").innerText = formatBRL(
    data.investido,
  );
  document.getElementById("detalhe-medio").innerText = formatBRL(data.medio);
  document.getElementById("detalhe-fiat").innerText = formatBRL(data.atual);

  const tbody = document.getElementById("detalhe-lista-transacoes");
  tbody.innerHTML = data.transacoes
    .map(
      (t) => `
        <tr>
            <td>${t.data}</td>
            <td style="font-family: 'JetBrains Mono'">${parseFloat(t.qtd).toFixed(8)}</td>
            <td>${formatBRL(t.preco)}</td>
            <td style="text-align: right;">
                <button class="btn-delete" onclick="executarDelecao(${t.id})">🗑️</button>
            </td>
        </tr>`,
    )
    .join("");
}

async function executarDelecao(id) {
  if (!confirm("⚠️ Confirmar exclusão?")) return;
  const res = await fetch(`/deletar_transacao/${id}`, { method: "POST" });
  if (res.ok) {
    if (carteiraAbertaAtualmente)
      await mostrarDetalhes(carteiraAbertaAtualmente);
    await inicializarDashboard();
  }
}

// 3. AUXILIARES
function renderizarGrafico(data) {
  const ctx = document.getElementById("graficoAlocacao").getContext("2d");
  if (meuGrafico) meuGrafico.destroy();
  meuGrafico = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.values,
          backgroundColor: ["#f7931a", "#1e3a8a", "#7f1d1d"],
          borderWidth: 0,
        },
      ],
    },
    options: { cutout: "80%", plugins: { legend: { display: false } } },
  });
}

async function toggleUnit() {
  currentUnit = currentUnit === "BTC" ? "SATS" : "BTC";
  await fetch("/api/config", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ unit: currentUnit, privacy: privacyMode }),
  });
  inicializarDashboard();
}

async function togglePrivacy() {
  privacyMode = !privacyMode;
  document.body.classList.toggle("privacy-on", privacyMode);
  await fetch("/api/config", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ unit: currentUnit, privacy: privacyMode }),
  });
}

document.addEventListener("DOMContentLoaded", inicializarDashboard);
