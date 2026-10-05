/* O visor da escada: uma família por tela. Trilha no alto, hash pelo id da
   seção, setas do teclado, e as perguntas (previsão e recuperação) com a
   resposta que explica onde a aposta divergiu. Sem biblioteca. */
(function () {
  "use strict";
  var secs = [].slice.call(document.querySelectorAll(".tela"));
  var N = secs.length;
  var est = __TRILHA__;
  var trilha = document.getElementById("trilha");
  var ant = document.getElementById("ant"), prox = document.getElementById("prox"), pos = document.getElementById("pos");
  var atual = 0;

  function desenharTrilha(k) {
    var h = "";
    for (var i = 0; i < est.length; i++) {
      var cls = i < k ? "passado" : (i === k ? "atual" : "futuro");
      var cor = est[i].cor ? ' style="--fam:' + est[i].cor + '"' : "";
      h += '<div class="est ' + cls + '" data-i="' + i + '"' + cor + '><span class="tok">' + est[i].tok + '</span><span class="nome">' + est[i].nome + '</span></div>';
    }
    trilha.innerHTML = h;
    var a = trilha.querySelector(".atual");
    if (a && a.scrollIntoView) { try { a.scrollIntoView({ block: "nearest", inline: "center" }); } catch (e) {} }
  }
  function ir(k, foco) {
    if (k < 0 || k >= N) return;
    atual = k;
    secs.forEach(function (s, i) { s.hidden = (i !== k); });
    desenharTrilha(k);
    pos.textContent = k === 0 ? "antes de tudo" : (k === N - 1 ? "o fecho" : "família " + k + " de " + (N - 2));
    ant.disabled = (k === 0); ant.querySelector("span").textContent = k > 0 ? secs[k - 1].dataset.nome : "";
    prox.disabled = (k === N - 1); prox.querySelector("span").textContent = k < N - 1 ? secs[k + 1].dataset.nome : "";
    try { if (location.hash !== "#" + secs[k].id) history.replaceState(null, "", "#" + secs[k].id); } catch (e) {}
    try { localStorage.setItem("escada-tela", String(k)); } catch (e) {}
    if (window.ESCADA_MONTAR) window.ESCADA_MONTAR();   // monta o instrumento da tela que acabou de aparecer
    if (foco) window.scrollTo({ top: 0, behavior: "auto" });
  }
  ant.addEventListener("click", function () { ir(atual - 1, true); });
  prox.addEventListener("click", function () { ir(atual + 1, true); });
  trilha.addEventListener("click", function (e) { var t = e.target.closest && e.target.closest(".est"); if (t) ir(+t.dataset.i, true); });
  document.addEventListener("keydown", function (e) {
    if (e.target && /^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(e.target.tagName)) return;
    if (e.key === "ArrowRight") ir(atual + 1, true);
    if (e.key === "ArrowLeft") ir(atual - 1, true);
  });
  function porHash() {
    var a = -1; secs.forEach(function (s, i) { if ("#" + s.id === location.hash) a = i; });
    return a;
  }
  window.addEventListener("hashchange", function () { var a = porHash(); if (a >= 0 && a !== atual) ir(a, true); });

  // as perguntas: aposta antes do instrumento, recuperação no fim. A resposta
  // diz ONDE a aposta divergiu, nunca só "errado"; nada trava o próximo.
  [].forEach.call(document.querySelectorAll(".pergunta"), function (sec) {
    var certa = +sec.dataset.certa, botao = sec.querySelector("button.ver"), porque = sec.querySelector(".porque");
    var nome = botao.dataset.pergunta;
    try { var guardada = localStorage.getItem("escada-" + nome); if (guardada !== null) { var r = sec.querySelector('input[value="' + guardada + '"]'); if (r) r.checked = true; } } catch (e) {}
    botao.addEventListener("click", function () {
      var esc = sec.querySelector("input:checked");
      var labels = sec.querySelectorAll("label");
      [].forEach.call(labels, function (l, i) { l.classList.toggle("certa", i === certa); l.classList.toggle("errada", esc && i === +esc.value && i !== certa); });
      var b = porque.querySelector("b");
      if (!esc) b.textContent = "Você não apostou. A resposta é a marcada:";
      else if (+esc.value === certa) b.textContent = "Acertou:";
      else b.textContent = "Você escolheu “" + labels[+esc.value].textContent.trim() + "”; a resposta é “" + labels[certa].textContent.trim() + "”, porque";
      porque.hidden = false;
      try { if (esc) localStorage.setItem("escada-" + nome, esc.value); } catch (e) {}
    });
  });

  var k0 = porHash();
  if (k0 < 0) { try { var s = localStorage.getItem("escada-tela"); if (s !== null) k0 = Math.min(N - 1, +s); } catch (e) {} }
  ir(k0 < 0 ? 0 : k0, false);
})();
