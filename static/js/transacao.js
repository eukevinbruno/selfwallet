document.addEventListener("DOMContentLoaded", function () {
  // 1. Definir a data/hora local atual no input de forma precisa
  const inputData = document.getElementById("data_compra");
  if (inputData) {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");

    inputData.value = `${year}-${month}-${day}T${hours}:${minutes}`;
  }

  // 2. Validação e Feedback ao Usuário
  const form = (id = document.getElementById("form-transacao"));
  form.addEventListener("submit", function (e) {
    const qtd = parseFloat(document.getElementById("quantidade").value);
    const preco = parseFloat(document.getElementById("preco_unitario").value);

    if (qtd <= 0 || preco <= 0) {
      e.preventDefault();
      alert("⚠️ Os valores de quantidade e preço devem ser maiores que zero.");
      return;
    }

    // Feedback visual no botão para evitar cliques duplos
    const btn = form.querySelector("button");
    btn.innerText = "REGISTRANDO...";
    btn.style.opacity = "0.7";
    btn.style.pointerEvents = "none";
  });
});
