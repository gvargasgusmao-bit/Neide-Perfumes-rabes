
// ============================================================
// QUIZ — Sistema completo
// ============================================================
const respostas = {
  genero: null,
  intensidade: null,
  estilo: [],
  ocasiao: [],
  familia: [],
  preco_faixa: null,
  perfume_famoso: ''
};

const multiSelect = ['estilo', 'ocasiao', 'familia'];
const TOTAL_ETAPAS = 7;
let etapaAtual = 1;

// Inicializa os listeners das opções
document.querySelectorAll('.quiz-opcao').forEach(btn => {
  btn.addEventListener('click', () => {
    const campo = btn.dataset.campo;
    const valor = btn.dataset.valor;

    if (multiSelect.includes(campo)) {
      // Multi-select
      btn.classList.toggle('selecionada');
      const isSelected = btn.classList.contains('selecionada');
      btn.setAttribute('aria-pressed', isSelected ? 'true' : 'false');

      if (isSelected) {
        if (!respostas[campo].includes(valor)) respostas[campo].push(valor);
      } else {
        respostas[campo] = respostas[campo].filter(v => v !== valor);
      }
      // Para multi: habilita próximo se pelo menos 1 selecionado
      atualizarBotaoProx(btn.closest('.quiz-etapa').dataset.etapa);
    } else {
      // Single select
      const etapa = btn.closest('.quiz-etapa');
      etapa.querySelectorAll('.quiz-opcao').forEach(b => {
        b.classList.remove('selecionada');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('selecionada');
      btn.setAttribute('aria-pressed', 'true');
      respostas[campo] = valor;
      atualizarBotaoProx(etapa.dataset.etapa);
    }
  });
});

function atualizarBotaoProx(etapa) {
  const btn = document.getElementById('prox-' + etapa);
  if (!btn) return;
  let habilitado = false;

  if (etapa == 1) habilitado = respostas.genero !== null;
  else if (etapa == 2) habilitado = respostas.intensidade !== null;
  else if (etapa == 3) habilitado = respostas.estilo.length > 0;
  else if (etapa == 4) habilitado = respostas.ocasiao.length > 0;
  else if (etapa == 5) habilitado = respostas.familia.length > 0;
  else if (etapa == 6) habilitado = respostas.preco_faixa !== null;

  btn.disabled = !habilitado;
}

function proximaEtapa(atual) {
  const etapaEl = document.getElementById('etapa-' + atual);
  const proximaEl = document.getElementById('etapa-' + (atual + 1));
  if (!proximaEl) return;

  etapaEl.classList.remove('ativa');
  proximaEl.classList.add('ativa');
  etapaAtual = atual + 1;
  atualizarProgresso();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function etapaAnterior(atual) {
  const etapaEl = document.getElementById('etapa-' + atual);
  const anteriorEl = document.getElementById('etapa-' + (atual - 1));
  if (!anteriorEl) return;

  etapaEl.classList.remove('ativa');
  anteriorEl.classList.add('ativa');
  etapaAtual = atual - 1;
  atualizarProgresso();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function pularEtapa(etapa) {
  proximaEtapa(etapa);
}

function atualizarProgresso() {
  const pct = Math.round((etapaAtual / TOTAL_ETAPAS) * 100);
  document.getElementById('quiz-barra-fill').style.width = pct + '%';
  document.getElementById('quiz-barra-fill').parentElement.setAttribute('aria-valuenow', pct);
  document.getElementById('quiz-etapa-atual').textContent = etapaAtual;
}

function preencherExemplo(texto) {
  document.getElementById('campo-perfume-famoso').value = texto;
}

async function enviarQuiz() {
  respostas.perfume_famoso = document.getElementById('campo-perfume-famoso').value.trim();

  // Mostra loading
  document.getElementById('quiz-form').style.display = 'none';
  document.getElementById('quiz-loading').classList.add('ativo');

  try {
    const resp = await fetch('/api/recomendacoes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(respostas)
    });
    const dados = await resp.json();

    if (!dados.recomendacoes || dados.recomendacoes.length === 0) {
      throw new Error('Sem resultados');
    }

    exibirResultados(dados.recomendacoes);
  } catch (e) {
    console.error('Erro ao buscar recomendações:', e);
    // fallback: mostra mensagem de erro amigável
    document.getElementById('quiz-loading').classList.remove('ativo');
    document.getElementById('quiz-form').style.display = 'block';
    alert('Ocorreu um erro. Por favor, tente novamente.');
  }
}

function exibirResultados(recomendacoes) {
  document.getElementById('quiz-loading').classList.remove('ativo');

  const container = document.getElementById('resultado-cards');
  container.innerHTML = '';

  const ranks = [
    { label: '🏆 Melhor Combinação', classe: 'primeira' },
    { label: '🥈 Segunda Opção', classe: 'segunda' },
    { label: '🥉 Alternativa Premium', classe: 'terceira' }
  ];

  recomendacoes.slice(0, 3).forEach((p, idx) => {
    const rank = ranks[idx];
    const generoLabel = p.genero === 'masculino' ? 'Masculino' : p.genero === 'feminino' ? 'Feminino' : 'Unissex';
    const score = Math.min(100, Math.round(p.score));
    const fixacaoPct = ((p.fixacao || 3) / 5) * 100;
    const projecaoPct = ((p.projecao || 3) / 5) * 100;

    const motivo = gerarMotivo(p, respostas);

    const similaresHtml = (p.similares_famosos || []).length > 0
      ? `<div class="produto-similares-famosos" style="margin-bottom:1rem;">
          <div class="produto-similares-titulo">Lembra</div>
          <div class="produto-similares-lista">
            ${p.similares_famosos.map(s => `<span class="produto-similar-tag">${s}</span>`).join('')}
          </div>
        </div>` : '';

    const waMensagem = encodeURIComponent(`Olá, Neide Perfumes! Fiz o quiz e quero saber mais sobre o perfume "${p.nome}". Vi que é recomendado para mim!`);
    const waLink = `https://wa.me/<%= config.whatsapp_contato %>?text=${waMensagem}`;

    container.innerHTML += `
      <article class="resultado-card" aria-label="${p.nome}">
        <div class="resultado-card-imagem" style="position:relative;">
          <div class="resultado-card-rank" style="position:absolute;top:12px;left:12px;z-index:3;">
            <span class="resultado-card-rank-badge ${rank.classe}">${rank.label}</span>
          </div>
          <div class="resultado-card-placeholder">
            <div class="resultado-card-placeholder-icone" aria-hidden="true">🌹</div>
          </div>
        </div>
        <div class="resultado-card-info">
          <div class="resultado-card-marca">${p.marca_nome || 'Importado'}</div>
          <h3 class="resultado-card-nome">${p.nome}</h3>
          <div class="score-compat">
            <span>Compatibilidade:</span>
            <span class="score-valor">${score}%</span>
          </div>
          <div class="resultado-card-preco">
            ${p.preco_sob_consulta ? 'Sob Consulta' : 'R$ ' + (p.preco || 0).toLocaleString('pt-BR', {minimumFractionDigits: 0})}
          </div>
          <div class="resultado-card-motivo">${motivo}</div>
          ${similaresHtml}
          <div class="resultado-card-metricas">
            <div class="metrica">
              <span class="metrica-label">Fixação</span>
              <div class="metrica-barra"><div class="metrica-barra-fill" style="width:${fixacaoPct}%"></div></div>
            </div>
            <div class="metrica">
              <span class="metrica-label">Projeção</span>
              <div class="metrica-barra"><div class="metrica-barra-fill" style="width:${projecaoPct}%"></div></div>
            </div>
          </div>
          <div class="resultado-card-acoes">
            <a href="${waLink}" class="btn btn-whatsapp" target="_blank" rel="noopener noreferrer" id="resultado-wa-${idx}" style="flex:1;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.890-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
              Quero esse perfume
            </a>
            <a href="/perfume/${p.slug}" class="btn btn-ghost" id="resultado-ver-${idx}">Ver detalhes</a>
          </div>
        </div>
      </article>
    `;
  });

  document.getElementById('quiz-resultado').classList.add('ativo');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function gerarMotivo(perfume, respostas) {
  const motivos = [];

  if (respostas.genero && (perfume.genero === respostas.genero || perfume.genero === 'unissex')) {
    motivos.push('combina com seu gênero');
  }
  if (respostas.familia && respostas.familia.includes(perfume.familia_olfativa)) {
    motivos.push(`tem notas ${perfume.familia_olfativa}s que você adora`);
  }
  if (respostas.intensidade && perfume.intensidade === respostas.intensidade) {
    motivos.push(`tem a intensidade ${respostas.intensidade} que você prefere`);
  }
  if (respostas.perfume_famoso && (perfume.similares_famosos || []).some(s =>
    s.toLowerCase().includes(respostas.perfume_famoso.toLowerCase().split(' ')[0]))) {
    motivos.push(`é muito similar ao ${respostas.perfume_famoso} que você já conhece`);
  }
  if (respostas.ocasiao && respostas.ocasiao.some(o => (perfume.ocasiao || []).includes(o))) {
    motivos.push('é perfeito para a ocasião escolhida');
  }

  if (motivos.length === 0) {
    return `${perfume.nome} é uma excelente escolha com ótima fixação e projeção, ideal para quem busca qualidade e exclusividade.`;
  }

  return `Este perfume foi selecionado porque ${motivos.join(', ')}.`;
}

function reiniciarQuiz() {
  // Reset respostas
  respostas.genero = null;
  respostas.intensidade = null;
  respostas.estilo = [];
  respostas.ocasiao = [];
  respostas.familia = [];
  respostas.preco_faixa = null;
  respostas.perfume_famoso = '';

  // Reset UI
  document.querySelectorAll('.quiz-opcao').forEach(btn => {
    btn.classList.remove('selecionada');
    btn.setAttribute('aria-pressed', 'false');
  });
  document.getElementById('campo-perfume-famoso').value = '';
  document.querySelectorAll('.quiz-etapa').forEach(e => e.classList.remove('ativa'));
  document.getElementById('etapa-1').classList.add('ativa');
  document.querySelectorAll('[id^="prox-"]').forEach(b => b.disabled = true);

  etapaAtual = 1;
  atualizarProgresso();

  document.getElementById('quiz-resultado').classList.remove('ativo');
  document.getElementById('quiz-form').style.display = 'block';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
