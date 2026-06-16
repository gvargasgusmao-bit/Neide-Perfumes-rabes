const db = require('../data/db.json');

// ============================================================
// MAPA DE SIMILARIDADE — Perfumes famosos → família olfativa
// ============================================================
const MAPA_SIMILARES = {
  // Masculinos frescos/amadeirados
  'sauvage': { familia: 'amadeirada', genero: 'masculino', intensidade: 'forte', estilo: ['elegante','casual'] },
  'bleu de chanel': { familia: 'amadeirada', genero: 'masculino', intensidade: 'moderada', estilo: ['elegante','executivo'] },
  'invictus': { familia: 'amadeirada', genero: 'masculino', intensidade: 'forte', estilo: ['jovem','sedutor'] },
  'one million': { familia: 'especiada', genero: 'masculino', intensidade: 'forte', estilo: ['sedutor','luxuoso'] },
  'acqua di gio': { familia: 'citrica', genero: 'masculino', intensidade: 'moderada', estilo: ['casual','elegante'] },
  'fahrenheit': { familia: 'amadeirada', genero: 'masculino', intensidade: 'forte', estilo: ['elegante','sofisticado'] },
  'bad boy': { familia: 'especiada', genero: 'masculino', intensidade: 'forte', estilo: ['sedutor','jovem'] },
  'eros': { familia: 'amadeirada', genero: 'masculino', intensidade: 'forte', estilo: ['sedutor','jovem'] },
  'drakkar noir': { familia: 'amadeirada', genero: 'masculino', intensidade: 'forte', estilo: ['executivo','elegante'] },
  'terra di hermes': { familia: 'amadeirada', genero: 'masculino', intensidade: 'moderada', estilo: ['elegante','sofisticado'] },

  // Femininos florais/doces
  'la vie est belle': { familia: 'baunilha', genero: 'feminino', intensidade: 'moderada', estilo: ['elegante','sofisticado'] },
  'good girl': { familia: 'floral', genero: 'feminino', intensidade: 'forte', estilo: ['sedutor','jovem'] },
  'chance': { familia: 'floral', genero: 'feminino', intensidade: 'moderada', estilo: ['elegante','casual'] },
  'flowerbomb': { familia: 'floral', genero: 'feminino', intensidade: 'forte', estilo: ['sedutor','luxuoso'] },
  'black opium': { familia: 'doce', genero: 'feminino', intensidade: 'forte', estilo: ['sedutor','jovem'] },
  'mon paris': { familia: 'floral', genero: 'feminino', intensidade: 'moderada', estilo: ['elegante','sofisticado'] },
  'miss dior': { familia: 'floral', genero: 'feminino', intensidade: 'moderada', estilo: ['elegante','casual'] },
  'tresor': { familia: 'floral', genero: 'feminino', intensidade: 'forte', estilo: ['elegante','sofisticado'] },
  'coco mademoiselle': { familia: 'oriental', genero: 'feminino', intensidade: 'moderada', estilo: ['elegante','sofisticado'] },
  '212 sexy': { familia: 'floral', genero: 'feminino', intensidade: 'moderada', estilo: ['sedutor','jovem'] },
  'idole': { familia: 'floral', genero: 'feminino', intensidade: 'moderada', estilo: ['elegante','casual'] },
  'alien': { familia: 'baunilha', genero: 'feminino', intensidade: 'muito_marcante', estilo: ['luxuoso','sofisticado'] },

  // Unissex/Nicho
  'baccarat rouge 540': { familia: 'oriental', genero: 'unissex', intensidade: 'muito_marcante', estilo: ['luxuoso','sofisticado'] },
  'oud wood': { familia: 'oud', genero: 'unissex', intensidade: 'forte', estilo: ['luxuoso','sofisticado'] },
  'aventus': { familia: 'amadeirada', genero: 'masculino', intensidade: 'forte', estilo: ['luxuoso','executivo'] },
  'silver mountain water': { familia: 'citrica', genero: 'masculino', intensidade: 'moderada', estilo: ['elegante','casual'] },
  'noir de noir': { familia: 'oriental', genero: 'unissex', intensidade: 'muito_marcante', estilo: ['luxuoso','sedutor'] },
  'mancera': { familia: 'oriental', genero: 'unissex', intensidade: 'forte', estilo: ['luxuoso','sofisticado'] },
};

// ============================================================
// ALGORITMO DE PONTUAÇÃO
// Pesos: similaridade(40) + familia(25) + ocasiao(15) + intensidade(10) + preco(10) + bonus genero
// ============================================================
function calcularScore(perfume, respostas) {
  let score = 0;

  // 1. Similaridade com perfume famoso (40 pts)
  if (respostas.perfume_famoso) {
    const buscaLower = respostas.perfume_famoso.toLowerCase().trim();
    const refData = Object.keys(MAPA_SIMILARES).find(k => buscaLower.includes(k) || k.includes(buscaLower.split(' ')[0]));

    if (refData) {
      const ref = MAPA_SIMILARES[refData];
      const similaresPerfume = (perfume.similares_famosos || []).map(s => s.toLowerCase());
      const refNomes = Object.keys(MAPA_SIMILARES).filter(k =>
        buscaLower.includes(k) || k.includes(buscaLower.split(' ')[0])
      );

      // Verifica se o perfume é similar ao famoso
      const ehSimilar = similaresPerfume.some(s => refNomes.some(rn => s.includes(rn.split(' ')[0]))) ||
                        similaresPerfume.some(s => s.includes(buscaLower.split(' ')[0]));

      if (ehSimilar) {
        score += 40; // Match direto de similaridade
      } else if (perfume.familia_olfativa === ref.familia) {
        score += 20; // Mesma família do perfume de referência
      }

      // Bônus por mesma família do perfume de referência
      if (perfume.familia_olfativa === ref.familia) score += 8;

      // Bônus por estilo compatível com referência
      const estiloRef = ref.estilo || [];
      const estiloPerf = perfume.estilo || [];
      const matchEstilo = estiloRef.filter(e => estiloPerf.includes(e)).length;
      score += matchEstilo * 4;
    }
  }

  // 2. Família olfativa (25 pts)
  if (respostas.familia && respostas.familia.length > 0) {
    if (respostas.familia.includes(perfume.familia_olfativa)) {
      score += 25;
    }
  }

  // 3. Ocasião (15 pts)
  if (respostas.ocasiao && respostas.ocasiao.length > 0) {
    const perfumeOcasiao = perfume.ocasiao || [];
    const matchOcasiao = respostas.ocasiao.filter(o => perfumeOcasiao.includes(o)).length;
    score += Math.min(15, matchOcasiao * 5);
  }

  // 4. Intensidade (10 pts)
  if (respostas.intensidade && perfume.intensidade === respostas.intensidade) {
    score += 10;
  }

  // 5. Faixa de preço (10 pts)
  if (respostas.preco_faixa) {
    const preco = perfume.preco || 0;
    let encaixaPreco = false;
    if (respostas.preco_faixa === 'ate_250' && preco <= 250) encaixaPreco = true;
    if (respostas.preco_faixa === 'ate_350' && preco <= 350) encaixaPreco = true;
    if (respostas.preco_faixa === 'ate_500' && preco <= 500) encaixaPreco = true;
    if (respostas.preco_faixa === 'acima_500' && preco > 500) encaixaPreco = true;
    if (encaixaPreco) score += 10;
  }

  // 6. Bônus de gênero
  if (respostas.genero) {
    if (perfume.genero === respostas.genero) score += 15;
    else if (perfume.genero === 'unissex') score += 8;
  }

  // 7. Bônus estilo pessoal
  if (respostas.estilo && respostas.estilo.length > 0) {
    const perfumeEstilo = perfume.estilo || [];
    const matchEstilo = respostas.estilo.filter(e => perfumeEstilo.includes(e)).length;
    score += matchEstilo * 3;
  }

  // 8. Bônus destaque
  if (perfume.destaque) score += 5;

  return score;
}

// ============================================================
// CONTROLLER
// ============================================================
const ProductController = {

  getHome: (req, res) => {
    const destaques = db.perfumes.filter(p => p.destaque === true && p.status_estoque !== 'esgotado');
    res.render('home', {
      perfumes: destaques,
      marcas: db.marcas,
      config: db.configuracoes
    });
  },

  getCatalog: (req, res) => {
    const { genero, familia, marca, ocasiao } = req.query;
    let perfumes = db.perfumes.filter(p => p.status_estoque !== 'esgotado');

    // Filtros server-side (para SEO e URL sharing)
    if (genero) perfumes = perfumes.filter(p => p.genero === genero || p.genero === 'unissex');
    if (familia) perfumes = perfumes.filter(p => p.familia_olfativa === familia);
    if (marca) {
      const marcaObj = db.marcas.find(m => m.nome.toLowerCase().includes(marca.toLowerCase()));
      if (marcaObj) perfumes = perfumes.filter(p => p.id_marca === marcaObj.id_marca);
    }
    if (ocasiao) perfumes = perfumes.filter(p => (p.ocasiao || []).includes(ocasiao));

    res.render('catalog', {
      perfumes,
      marcas: db.marcas,
      config: db.configuracoes,
      filtros: { genero, familia, marca, ocasiao }
    });
  },

  getProductBySlug: (req, res) => {
    const { slug } = req.params;
    const perfume = db.perfumes.find(p => p.slug === slug);

    if (!perfume) {
      return res.status(404).render('404', {
        meta: { title: 'Perfume não encontrado | Neide Perfumes', description: '' },
        config: db.configuracoes
      });
    }

    const marca = db.marcas.find(m => m.id_marca === perfume.id_marca) || null;

    // Perfumes relacionados: mesma família olfativa ou mesma marca
    const relacionados = db.perfumes.filter(p =>
      p.id_perfume !== perfume.id_perfume &&
      p.status_estoque !== 'esgotado' &&
      (p.familia_olfativa === perfume.familia_olfativa || p.id_marca === perfume.id_marca) &&
      (perfume.genero === 'unissex' || p.genero === perfume.genero || p.genero === 'unissex')
    ).slice(0, 4);

    res.render('product', {
      perfume,
      marca,
      marcas: db.marcas,
      relacionados,
      config: db.configuracoes
    });
  },

  getQuiz: (req, res) => {
    res.render('quiz', {
      config: db.configuracoes,
      meta: {
        title: 'Quiz de Perfumes | Neide Perfumes Importados',
        description: 'Descubra seu perfume árabe ideal respondendo 7 perguntas rápidas.'
      }
    });
  },

  postRecomendacoes: (req, res) => {
    const respostas = req.body;

    // Filtra perfumes disponíveis
    const candidatos = db.perfumes.filter(p => p.status_estoque !== 'esgotado');

    // Calcula score para cada um
    const comScore = candidatos.map(perfume => {
      const score = calcularScore(perfume, respostas);
      const marca = db.marcas.find(m => m.id_marca === perfume.id_marca);
      return {
        ...perfume,
        score,
        marca_nome: marca ? marca.nome : 'Importado'
      };
    });

    // Ordena por score descendente
    comScore.sort((a, b) => b.score - a.score);

    // Retorna top 3 garantindo diversidade (1 de destaque se possível)
    const top = comScore.slice(0, 10);
    const recomendacoes = [];

    // Primeira: melhor score absoluto
    if (top[0]) recomendacoes.push(top[0]);

    // Segunda: diferente marca/família da primeira
    const segunda = top.slice(1).find(p =>
      (!recomendacoes[0] || p.id_marca !== recomendacoes[0].id_marca)
    ) || top[1];
    if (segunda) recomendacoes.push(segunda);

    // Terceira: preferencialmente premium (acima da faixa pedida) ou diferente das anteriores
    const terceira = top.slice(1).find(p =>
      !recomendacoes.some(r => r.id_perfume === p.id_perfume) &&
      (p.preco > (recomendacoes[0] ? recomendacoes[0].preco : 0) || p.id_marca !== (recomendacoes[0] || {}).id_marca)
    ) || top.find(p => !recomendacoes.some(r => r.id_perfume === p.id_perfume));
    if (terceira) recomendacoes.push(terceira);

    res.json({ recomendacoes, total: comScore.length });
  },

  getSEOComparison: (req, res) => {
    const { famosoSlug } = req.params;
    // Ex: "sauvage", "baccarat-rouge"
    const famosoDecoded = famosoSlug.replace(/-/g, ' ');
    
    // Find perfumes that mention this famous perfume in similares_famosos
    const recomendados = db.perfumes.filter(p => 
      p.similares_famosos && p.similares_famosos.some(s => s.toLowerCase().includes(famosoDecoded.toLowerCase().split(' ')[0]))
    );

    if (recomendados.length === 0) {
      // Fallback: Just return a generic catalog search or a top perfume
      return res.redirect('/catalogo');
    }

    res.render('comparacao', {
      meta: {
        title: `Perfumes parecidos com ${famosoDecoded.toUpperCase()} | Neide Perfumes`,
        description: `Procurando perfumes árabes que lembram o ${famosoDecoded.toUpperCase()}? Descubra as melhores opções com alta fixação e projeção na Neide Perfumes Importados.`
      },
      famoso: famosoDecoded,
      recomendados: recomendados.slice(0, 3), // Top 3
      config: db.configuracoes
    });
  }
};

module.exports = ProductController;