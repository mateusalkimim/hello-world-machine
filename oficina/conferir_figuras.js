#!/usr/bin/env node
/* Confere as figuras do seminário: cada circuito pronto da bancada (EXAMPLES), colocado
   como o modo figura coloca, passa na tabela-verdade da própria missão (runSteps). Para a
   máquina de binário, liga as lâmpadas de 79 e confere que a leitura é 79. Controle
   negativo: um circuito com um transistor a menos tem de REPROVAR. Lê a fonte
   bancada/bancada.html; roda sem navegador. Sai 1 em qualquer falha. */
const fs = require("fs"), path = require("path"), vm = require("vm");
const AQUI = path.dirname(__filename);
const fonte = fs.readFileSync(path.join(AQUI, "..", "bancada", "bancada.html"), "utf8");
const js = fonte.match(/<script>([\s\S]*)<\/script>/)[1];
const ini = js.indexOf("const EXAMPLES="), fim = js.indexOf("/* ================= state");
if (ini < 0 || fim < 0) { console.error("ABORTADO: não achei EXAMPLES ou o bloco de estado na fonte"); process.exit(1); }
const motor = js.slice(ini, fim);
const ctx = { console, sim: null };
vm.createContext(ctx);
vm.runInContext(motor + "\nthis.Sim=Sim; this.runSteps=runSteps; this.missions=missions; this.EXAMPLES=EXAMPLES;", ctx);
const { Sim, missions, EXAMPLES } = ctx;

function montar(mission, ex) {               // a mesma colocação do botão "Ver exemplo" e do modo figura
  const sim = new Sim(mission.cols, mission.rows);
  let minX = 1e9, maxX = -1, minY = 1e9, maxY = -1;
  for (const it of ex) { minX = Math.min(minX, it.x); maxX = Math.max(maxX, it.x); minY = Math.min(minY, it.y); maxY = Math.max(maxY, it.y); }
  const bw = maxX - minX + 1, bh = maxY - minY + 1; let regionH = sim.H;
  if (mission.binary) { const lines = mission.numMode === "float" ? 3 : (mission.outputs.length > 8 ? 3 : 2); regionH = mission.monitorY - (lines === 3 ? 2.7 : 2.1) / 2; }
  const ox = Math.floor((sim.W - bw) / 2) - minX, oy = Math.max(0, Math.round((regionH - bh) / 2)) - minY;
  for (const it of ex) { const x = it.x + ox, y = it.y + oy; if (x >= 0 && y >= 0 && x < sim.W && y < sim.H) sim.cells[y][x] = { t: it.t, r: it.r || 0, on: false, lbl: it.lbl || "" }; }
  return sim;
}
function roda(mission, sim) { ctx.sim = sim; return vm.runInContext("runSteps(missions.find(m=>m.id===" + JSON.stringify(mission.id) + "))", ctx); }

let falhas = 0, feitas = 0;
const FIGURAS = ["tut", "t1", "g-and", "g-or", "g-not", "add", "reg", "clk", "ins"];   // as nove do seminário
for (const id of FIGURAS) {
  const m = missions.find(x => x.id === id), ex = EXAMPLES[id];
  if (!m || !ex) { console.log(`REPROVADO ${id}: missão ou exemplo ausente`); falhas++; continue; }
  let ok, nota;
  if (m.steps) { const r = roda(m, montar(m, ex)); ok = r && r.all && !r.missing; nota = r.missing ? r.missing : r.rows.length + " linhas da tabela-verdade"; }
  else {                                   // o tutorial não tem tabela: a chave A acende a lâmpada, e só ela
    const sim = montar(m, ex); const [lx, ly] = sim.find("lamp", "")[0]; const sws = sim.find("sw", "A");
    sim.solve(); const apagada = !sim.lampLit(lx, ly);
    for (const [x, y] of sws) sim.cells[y][x].on = true; sim.solve(); const acesa = sim.lampLit(lx, ly);
    ok = apagada && acesa; nota = "chave A desligada: apagada; ligada: acesa";
  }
  console.log(`${ok ? "ok      " : "REPROVADO"} ${id.padEnd(6)} ${m.title}  (${nota})`);
  if (!ok) falhas++; feitas++;
}
// os circuitos só de chaves da estação 2 (oficina/figuras/extras.json), pela tabela da missão-base
{
  const extras = JSON.parse(fs.readFileSync(path.join(AQUI, "figuras", "extras.json"), "utf8"));
  for (const [id, ex] of Object.entries(extras)) {
    if (id === "_") continue;
    const m = missions.find(x => x.id === ex.base); const r = roda(m, montar(m, ex.cells)); const ok = r && r.all && !r.missing;
    console.log(`${ok ? "ok      " : "REPROVADO"} ${id.padEnd(6)} só chaves, conferido pela tabela de ${m.title}  (${r.missing ? r.missing : r.rows.length + " linhas"})`);
    if (!ok) falhas++; feitas++;
  }
}
// a máquina de binário com 79 aceso: as lâmpadas 64, 8, 4, 2 e 1
{
  const m = missions.find(x => x.id === "bin"), sim = montar(m, EXAMPLES.bin);
  for (const tok of ["64", "8", "4", "2", "1"]) for (const [x, y] of sim.find("lamp", tok)) { const c = sim.cell(x, y + 1); if (c && c.t === "sw") c.on = true; }
  sim.solve(); let v = 0;
  for (const l of ["128", "64", "32", "16", "8", "4", "2", "1"]) { const [x, y] = sim.find("lamp", l)[0]; if (sim.lampLit(x, y)) v += Number(l); }
  const ok = v === 79; console.log(`${ok ? "ok      " : "REPROVADO"} bin    A máquina de binário com 64+8+4+2+1 lê ${v}`); if (!ok) falhas++; feitas++;
}
// controle negativo: a porta E sem o segundo transistor tem de reprovar
{
  const m = missions.find(x => x.id === "g-and"); const ex = EXAMPLES["g-and"].filter(it => !(it.t === "tn" && it.x === 5));
  const r = roda(m, montar(m, ex)); const reprovou = !(r && r.all);
  console.log(`${reprovou ? "ok      " : "REPROVADO"} controle negativo: E com um transistor a menos ${reprovou ? "reprova, como devia" : "PASSOU, o verificador não mede"}`);
  if (!reprovou) falhas++;
}
console.log(falhas ? `\nREPROVADO: ${falhas} falha(s) em ${feitas} figuras` : `\nPASSA: ${feitas} figuras conferidas pela tabela-verdade da missão + controle negativo`);
process.exit(falhas ? 1 : 0);
