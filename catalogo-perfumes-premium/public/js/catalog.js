
// ============================================================
// CATÁLOGO — Filtros e busca client-side
// ============================================================
const TODOS_CARDS = Array.from(document.querySelectorAll('.perfume-card'));
const MAPA_PRECO_MAX = { 'ate_250': 250, 'ate_350': 350, 'ate_500': 500, 'acima_500': Infinity };
const MAPA_PRECO_MIN = { 'ate_250': 0, 'ate_350': 0, 'ate_500': 0, 'acima_500': 500 };

let filtrosPreco = new Set();

function togglePreco(el) {
  const val = el.dataset.preco;
  if (el.classList.contains('ativo')) {
    el.classList.remove('ativo');
    filtrosPreco.delete(val);
  } else {
    el.classList.add('ativo');
    filtrosPreco.add(val);
  }
  aplicarFiltros();
}

function aplicarFiltros() {
  const busca = document.getElementById('busca-input').value.toLowerCase().trim();
  const generosAtivos = [...document.querySelectorAll('input[name="genero"]:checked')].map(i => i.value);
  const familiasAtivas = [...document.querySelectorAll('input[name="familia"]:checked')].map(i => i.value);
  const marcasAtivas = [...document.querySelectorAll('input[name="marca"]:checked')].map(i => i.value);
  const ocasioesAtivas = [...document.querySelectorAll('input[name="ocasiao"]:checked')].map(i => i.value);
  const ordenar = document.getElementById('select-ordenar').value;

  let visiveis = TODOS_CARDS.filter(card => {
    // Busca
    if (busca) {
      const nome = card.dataset.nome || '';
      const marca = card.dataset.marca || '';
      const familia = card.dataset.familia || '';
      if (!nome.includes(busca) && !marca.includes(busca) && !familia.includes(busca)) return false;
    }

    // Gênero
    if (generosAtivos.length > 0 && !generosAtivos.includes(card.dataset.genero)) return false;

    // Família
    if (familiasAtivas.length > 0 && !familiasAtivas.includes(card.dataset.familia)) return false;

    // Marca
    if (marcasAtivas.length > 0 && !marcasAtivas.includes(card.dataset.marcaId)) return false;

    // Preço
    if (filtrosPreco.size > 0) {
      const preco = parseFloat(card.dataset.preco) || 0;
      let passaPreco = false;
      filtrosPreco.forEach(fp => {
        if (preco >= MAPA_PRECO_MIN[fp] && (fp === 'acima_500' ? preco > 500 : preco <= MAPA_PRECO_MAX[fp])) {
          passaPreco = true;
        }
      });
      if (!passaPreco) return false;
    }

    // Ocasião
    if (ocasioesAtivas.length > 0) {
      const ocasioesCard = (card.dataset.ocasiao || '').split(',');
      if (!ocasioesAtivas.some(o => ocasioesCard.includes(o))) return false;
    }

    return true;
  });

  // Ordenação
  visiveis = visiveis.sort((a, b) => {
    if (ordenar === 'preco_asc') return parseFloat(a.dataset.preco) - parseFloat(b.dataset.preco);
    if (ordenar === 'preco_desc') return parseFloat(b.dataset.preco) - parseFloat(a.dataset.preco);
    if (ordenar === 'nome_asc') return a.dataset.nome.localeCompare(b.dataset.nome);
    if (ordenar === 'nome_desc') return b.dataset.nome.localeCompare(a.dataset.nome);
    return 0;
  });

  // Mostrar/ocultar
  const grade = document.getElementById('grade-catalogo');
  TODOS_CARDS.forEach(c => { c.style.display = 'none'; });
  visiveis.forEach(c => {
    grade.appendChild(c);
    c.style.display = '';
  });

  // Sem resultados
  const semRes = document.getElementById('sem-resultados');
  if (visiveis.length === 0) {
    semRes.classList.add('visivel');
  } else {
    semRes.classList.remove('visivel');
  }

  // Contagem
  document.getElementById('contagem-resultados').textContent =
    `Mostrando ${visiveis.length} de ${TODOS_CARDS.length} perfumes`;
}

function limparFiltros() {
  document.querySelectorAll('input[type="checkbox"]').forEach(i => i.checked = false);
  document.getElementById('busca-input').value = '';
  document.getElementById('select-ordenar').value = 'padrao';
  filtrosPreco.clear();
  document.querySelectorAll('.filtro-preco-pill').forEach(p => p.classList.remove('ativo'));
  aplicarFiltros();
}

function toggleFiltrosMobile() {
  const sidebar = document.getElementById('filtros-sidebar');
  sidebar.classList.toggle('aberto');
}

// Aplicar filtros iniciais via URL params
(function iniciarFiltrosURL() {
  const params = new URLSearchParams(window.location.search);
  const genero = params.get('genero');
  const familia = params.get('familia');
  const marca = params.get('marca');

  if (genero) {
    const input = document.getElementById('filtro-' + genero);
    if (input) { input.checked = true; }
  }
  if (familia) {
    const input = document.getElementById('filtro-' + familia);
    if (input) { input.checked = true; }
  }
  if (marca) {
    // Marca por nome
    document.querySelectorAll('input[name="marca"]').forEach(i => {
      if (i.parentElement.querySelector('.filtro-opcao-texto')
          .textContent.trim().toLowerCase().includes(marca.toLowerCase())) {
        i.checked = true;
      }
    });
  }

  if (genero || familia || marca) aplicarFiltros();
})();

// Mobile: mostrar botão de filtros
if (window.innerWidth <= 900) {
  document.getElementById('btn-filtros-mobile').style.display = '';
}
