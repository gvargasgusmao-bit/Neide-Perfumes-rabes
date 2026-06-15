const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'src', 'data', 'db.json');
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

// 1. Atualizar configurações
db.configuracoes.nome_marca = 'Neide Perfumes Importados';
db.configuracoes.whatsapp_contato = '5567996962426';
db.configuracoes.mensagem_padrao = 'Olá, Neide Perfumes Importados! Vi o site e quero saber mais sobre a fragrância ';

// 2. Expandir marcas
const marcasAdicionais = ['Lattafa', 'Maison Alhambra', 'Armaf', 'Afnan', 'French Avenue', 'Al Wataniah', 'Ard Al Zaafaran', 'Orientica', 'Asdaaf', 'Amouage', 'Roja Parfums'];
let maxIdMarca = Math.max(...db.marcas.map(m => m.id_marca));
marcasAdicionais.forEach(nomeMarca => {
  if (!db.marcas.find(m => m.nome === nomeMarca)) {
    maxIdMarca++;
    db.marcas.push({ id_marca: maxIdMarca, nome: nomeMarca });
  }
});

// 3. Expandir familias olfativas
const familiasNomes = ['floral', 'amadeirada', 'oriental', 'citrica', 'especiada', 'oud', 'doce', 'couro', 'frutada', 'baunilha'];
db.familias_olfativas = familiasNomes.map((nome, index) => ({ id_familia: index + 1, nome: nome }));

// 4 e 5. Dados dos 30 perfumes principais
const destaquesData = {
  'baroque-rouge-540-maison-alhambra': { genero: 'unissex', familia: 'oriental', intensidade: 'muito_marcante', topo: ['Safranal', 'Cedro'], coracao: ['Ambroxan', 'Rosa'], fundo: ['Fava Tonka', 'Baunilha'], fixacao: 5, projecao: 5, ocasiao: ['encontros', 'festas', 'uso_noturno', 'eventos'], similares_famosos: ['Baccarat Rouge 540 Maison Francis Kurkdjian'], estilo: ['luxuoso', 'sedutor', 'sofisticado'], destaque: true },
  'al-noble-ameer-lattafa': { genero: 'masculino', familia: 'amadeirada', intensidade: 'forte', topo: ['Bergamota', 'Limão'], coracao: ['Cedro', 'Sândalo', 'Patchouli'], fundo: ['Âmbar', 'Baunilha', 'Almíscar'], fixacao: 4, projecao: 4, ocasiao: ['trabalho', 'eventos', 'encontros', 'festas'], similares_famosos: ['Dior Sauvage', 'Bleu de Chanel'], estilo: ['elegante', 'executivo', 'sofisticado'], destaque: true },
  'bayaan-lattafa-100-ml': { genero: 'unissex', familia: 'oud', intensidade: 'muito_marcante', topo: ['Saffron', 'Canela'], coracao: ['Oud', 'Rosa'], fundo: ['Âmbar', 'Almíscar'], fixacao: 5, projecao: 5, ocasiao: ['encontros', 'festas', 'uso_noturno', 'eventos'], similares_famosos: ['Tom Ford Oud Wood', 'Montale Black Aoud'], estilo: ['luxuoso', 'sofisticado', 'sedutor'], destaque: true },
  'her-confession-lattafa-perfumes-100-ml': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Bergamota', 'Pera'], coracao: ['Rosa', 'Peônia', 'Jasmim'], fundo: ['Sândalo', 'Almíscar', 'Âmbar'], fixacao: 4, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros'], similares_famosos: ['Lancôme La Vie Est Belle', 'Yves Saint Laurent Mon Paris'], estilo: ['elegante', 'sofisticado', 'casual'], destaque: true },
  'his-confession-lattafa-perfumes': { genero: 'masculino', familia: 'amadeirada', intensidade: 'forte', topo: ['Bergamota', 'Cardamomo'], coracao: ['Cedro', 'Sândalo'], fundo: ['Âmbar', 'Baunilha', 'Almíscar'], fixacao: 4, projecao: 4, ocasiao: ['trabalho', 'encontros', 'festas', 'eventos'], similares_famosos: ['Dior Fahrenheit', 'Guerlain La Petite Robe Noire'], estilo: ['elegante', 'executivo', 'sedutor'], destaque: true },
  'athena-maison-alhambra-100-ml': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Bergamota', 'Framboesa'], coracao: ['Peônia', 'Jasmim', 'Rosa'], fundo: ['Sândalo', 'Almíscar', 'Cedro'], fixacao: 4, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros', 'festas'], similares_famosos: ['Carolina Herrera Good Girl', 'Yves Saint Laurent Black Opium'], estilo: ['elegante', 'jovem', 'sedutor'], destaque: true },
  'b-a-d-homme-maison-alhambra-100-ml': { genero: 'masculino', familia: 'especiada', intensidade: 'forte', topo: ['Bergamota', 'Cardamomo'], coracao: ['Patchouli', 'Cedro'], fundo: ['Baunilha', 'Âmbar', 'Almíscar'], fixacao: 5, projecao: 4, ocasiao: ['encontros', 'festas', 'uso_noturno'], similares_famosos: ['Carolina Herrera Bad Boy', 'Paco Rabanne 1 Million'], estilo: ['sedutor', 'jovem', 'luxuoso'], destaque: true },
  'b-a-d-femme-maison-alhambra-100-ml': { genero: 'feminino', familia: 'floral', intensidade: 'forte', topo: ['Bergamota', 'Pera'], coracao: ['Rosa', 'Jasmim', 'Tuberosa'], fundo: ['Baunilha', 'Sândalo', 'Âmbar'], fixacao: 5, projecao: 4, ocasiao: ['encontros', 'festas', 'uso_noturno', 'eventos'], similares_famosos: ['Carolina Herrera Good Girl', 'Lancôme La Nuit Trésor'], estilo: ['sedutor', 'luxuoso', 'elegante'], destaque: true },
  'armaf-infinity-gold-105-ml': { genero: 'masculino', familia: 'amadeirada', intensidade: 'forte', topo: ['Bergamota', 'Limão', 'Noz-moscada'], coracao: ['Cedro', 'Sândalo', 'Patchouli'], fundo: ['Âmbar', 'Almíscar', 'Baunilha'], fixacao: 4, projecao: 4, ocasiao: ['trabalho', 'eventos', 'encontros'], similares_famosos: ['Dior Sauvage Parfum', 'Creed Aventus'], estilo: ['elegante', 'executivo', 'luxuoso'], destaque: false },
  'club-de-nuit-woman-armaf-feminino': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Limão', 'Bergamota', 'Pimentão Rosa'], coracao: ['Peônia', 'Rosa', 'Jasmim'], fundo: ['Almíscar', 'Cedro', 'Âmbar'], fixacao: 4, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'festas'], similares_famosos: ['Chanel No.5', 'Chanel Chance Eau Tendre'], estilo: ['elegante', 'sofisticado', 'casual'], destaque: false },
  'delilah-pour-femme-edp-100-ml-maison-alhambra': { genero: 'feminino', familia: 'baunilha', intensidade: 'moderada', topo: ['Bergamota', 'Limão'], coracao: ['Rosa', 'Jasmim'], fundo: ['Baunilha', 'Sândalo', 'Âmbar'], fixacao: 4, projecao: 3, ocasiao: ['dia_a_dia', 'encontros', 'festas'], similares_famosos: ['Lancôme La Vie Est Belle', 'Thierry Mugler Angel'], estilo: ['elegante', 'sofisticado', 'jovem'], destaque: true },
  'delilah-blanc-maison-alhambra-100-ml': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Bergamota', 'Lichia'], coracao: ['Rosa Branca', 'Magnólia'], fundo: ['Sândalo', 'Almíscar'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros'], similares_famosos: ['Gucci Bloom', 'Lancôme Idole'], estilo: ['elegante', 'sofisticado'], destaque: false },
  'eclaire-lattafa-perfumes-feminino-100-ml': { genero: 'feminino', familia: 'floral', intensidade: 'forte', topo: ['Bergamota', 'Framboesa', 'Pera'], coracao: ['Jasmim', 'Lírio', 'Peônia'], fundo: ['Sândalo', 'Almíscar', 'Cedro'], fixacao: 4, projecao: 4, ocasiao: ['encontros', 'festas', 'eventos', 'uso_noturno'], similares_famosos: ['Yves Saint Laurent Black Opium', 'Carolina Herrera Good Girl'], estilo: ['sedutor', 'luxuoso', 'jovem'], destaque: true },
  'celeste-maison-alhambra-100-ml': { genero: 'unissex', familia: 'amadeirada', intensidade: 'forte', topo: ['Bergamota', 'Mandarina'], coracao: ['Iris', 'Sândalo', 'Vetiver'], fundo: ['Âmbar', 'Almíscar', 'Cedro'], fixacao: 4, projecao: 4, ocasiao: ['trabalho', 'eventos', 'encontros'], similares_famosos: ['Giorgio Armani Acqua di Giò Profumo', 'Dior Homme Intense'], estilo: ['elegante', 'sofisticado', 'executivo'], destaque: false },
  'dalal-lattafa': { genero: 'feminino', familia: 'oriental', intensidade: 'muito_marcante', topo: ['Saffron', 'Rosa'], coracao: ['Oud', 'Jasmim'], fundo: ['Âmbar', 'Almíscar', 'Baunilha'], fixacao: 5, projecao: 5, ocasiao: ['encontros', 'festas', 'uso_noturno', 'eventos'], similares_famosos: ['YSL Opium', 'Tom Ford Black Orchid'], estilo: ['luxuoso', 'sedutor', 'sofisticado'], destaque: true },
  'durrah-lattafa-perfumes': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Bergamota', 'Lichia'], coracao: ['Rosa', 'Peônia'], fundo: ['Almíscar', 'Sândalo'], fixacao: 4, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros'], similares_famosos: ['Chanel Chance Eau Fraîche', 'Guerlain Mon Guerlain'], estilo: ['elegante', 'casual', 'sofisticado'], destaque: false },
  'emaan-lattafa-100-ml': { genero: 'unissex', familia: 'oriental', intensidade: 'muito_marcante', topo: ['Saffron', 'Bergamota'], coracao: ['Rosa', 'Oud'], fundo: ['Âmbar', 'Sândalo', 'Almíscar'], fixacao: 5, projecao: 4, ocasiao: ['encontros', 'festas', 'eventos', 'uso_noturno'], similares_famosos: ['Tom Ford Oud Wood', 'Initio Atomic Rose'], estilo: ['luxuoso', 'sofisticado'], destaque: false },
  'alpine-maison-alhambra': { genero: 'masculino', familia: 'citrica', intensidade: 'moderada', topo: ['Bergamota', 'Limão', 'Menta'], coracao: ['Lavanda', 'Cedro'], fundo: ['Almíscar', 'Âmbar', 'Vetiver'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'academia'], similares_famosos: ['Polo Blue Ralph Lauren', 'Giorgio Armani Acqua di Giò'], estilo: ['casual', 'jovem', 'elegante'], destaque: false },
  'glacier-pour-homme-maison-alhambra': { genero: 'masculino', familia: 'citrica', intensidade: 'moderada', topo: ['Bergamota', 'Mandarina', 'Menta'], coracao: ['Cardamomo', 'Iris'], fundo: ['Cedro', 'Almíscar', 'Âmbar'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'academia'], similares_famosos: ['Dior Sauvage EDT', 'Viktor & Rolf Spicebomb'], estilo: ['casual', 'jovem', 'executivo'], destaque: false },
  'club-de-nuit-maleka-armaf': { genero: 'unissex', familia: 'oriental', intensidade: 'muito_marcante', topo: ['Bergamota', 'Saffron'], coracao: ['Rosa', 'Oud', 'Jasmim'], fundo: ['Âmbar', 'Baunilha', 'Almíscar'], fixacao: 5, projecao: 5, ocasiao: ['encontros', 'festas', 'uso_noturno', 'eventos'], similares_famosos: ['Chanel N°5', 'Creed Aventus for Her'], estilo: ['luxuoso', 'sofisticado', 'sedutor'], destaque: false },
  'como-moiselle-maison-alhambra': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Bergamota', 'Pera'], coracao: ['Peônia', 'Rosa', 'Coco'], fundo: ['Sândalo', 'Âmbar', 'Almíscar'], fixacao: 4, projecao: 3, ocasiao: ['dia_a_dia', 'encontros', 'festas'], similares_famosos: ['Chanel Chance', 'Givenchy Irresistible'], estilo: ['elegante', 'jovem', 'casual'], destaque: false },
  'eclat-de-lune-maison-alhambra': { genero: 'feminino', familia: 'baunilha', intensidade: 'suave', topo: ['Bergamota', 'Baunilha'], coracao: ['Rosa', 'Jasmim'], fundo: ['Baunilha', 'Âmbar', 'Almíscar'], fixacao: 3, projecao: 2, ocasiao: ['dia_a_dia', 'encontros'], similares_famosos: ['Thierry Mugler Alien', 'Nina Ricci Nina'], estilo: ['suave', 'casual', 'jovem'], destaque: false },
  'al-wataniah-ameerati-100-ml': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Bergamota', 'Pimenta Rosa'], coracao: ['Rosa', 'Jasmim', 'Íris'], fundo: ['Almíscar', 'Sândalo'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros'], similares_famosos: ['Lancôme La Vie Est Belle', 'Gucci Bloom'], estilo: ['elegante', 'casual', 'sofisticado'], destaque: false },
  'al-wataniah-ghala-edp-feminino-100-ml': { genero: 'feminino', familia: 'oriental', intensidade: 'forte', topo: ['Saffron', 'Bergamota'], coracao: ['Rosa', 'Jasmim'], fundo: ['Oud', 'Âmbar', 'Almíscar'], fixacao: 4, projecao: 4, ocasiao: ['encontros', 'festas', 'eventos', 'uso_noturno'], similares_famosos: ['Tom Ford Black Orchid', 'Yves Saint Laurent Opium'], estilo: ['sedutor', 'luxuoso', 'sofisticado'], destaque: false },
  'asdaaf-ameerat-al-arab-100-ml': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Pera', 'Bergamota'], coracao: ['Jasmim', 'Rosa', 'Peônia'], fundo: ['Sândalo', 'Almíscar', 'Cedro'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros'], similares_famosos: ['Lancôme Trésor', 'Dior Miss Dior'], estilo: ['elegante', 'sofisticado', 'casual'], destaque: false },
  'el-ward-palais-des-roses-edp-unissex-100-ml': { genero: 'unissex', familia: 'floral', intensidade: 'moderada', topo: ['Bergamota', 'Lichia'], coracao: ['Rosa', 'Peônia'], fundo: ['Almíscar', 'Cedro', 'Âmbar'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros'], similares_famosos: ['Gucci Bloom', 'Maison Margiela Replica Flower Market'], estilo: ['elegante', 'casual', 'sofisticado'], destaque: false },
  'chants-tenderina-maison-alhambra-feminino-100-ml': { genero: 'feminino', familia: 'doce', intensidade: 'moderada', topo: ['Bergamota', 'Framboesa'], coracao: ['Peônia', 'Rosa'], fundo: ['Baunilha', 'Almíscar', 'Cedro'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'encontros'], similares_famosos: ['Viktor & Rolf Flowerbomb', 'Guerlain Mon Guerlain Bloom of Rose'], estilo: ['jovem', 'casual', 'elegante'], destaque: false },
  'extravagant-lover-maison-alhambra': { genero: 'unissex', familia: 'oriental', intensidade: 'forte', topo: ['Bergamota', 'Limão', 'Saffron'], coracao: ['Oud', 'Rosa'], fundo: ['Âmbar', 'Baunilha', 'Cedro'], fixacao: 4, projecao: 4, ocasiao: ['encontros', 'festas', 'eventos', 'uso_noturno'], similares_famosos: ['Tom Ford Noir de Noir', 'Initio Musk Therapy'], estilo: ['sedutor', 'luxuoso', 'sofisticado'], destaque: false },
  'afnan-souvenir-desert-rose-100-ml': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Rosa', 'Pêssego'], coracao: ['Rosa', 'Jasmim'], fundo: ['Almíscar', 'Sândalo', 'Cedro'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros'], similares_famosos: ['Dior Miss Dior Rose N Roses', 'Gucci Bloom Profumo di Fiori'], estilo: ['elegante', 'casual', 'sofisticado'], destaque: false },
  'venti-silky-princess-queen-of-silk-creed': { genero: 'feminino', familia: 'floral', intensidade: 'moderada', topo: ['Bergamota', 'Limão'], coracao: ['Iris', 'Rosa', 'Sândalo'], fundo: ['Almíscar', 'Âmbar'], fixacao: 3, projecao: 3, ocasiao: ['dia_a_dia', 'trabalho', 'encontros'], similares_famosos: ['Creed Aventus for Her', 'Creed Spring Flower'], estilo: ['elegante', 'sofisticado', 'luxuoso'], destaque: true },
};

function getPrecoFaixa(preco) {
  if (!preco) return 'ate_250';
  if (preco <= 250) return 'ate_250';
  if (preco <= 350) return 'ate_350';
  if (preco <= 500) return 'ate_500';
  return 'acima_500';
}

db.perfumes.forEach(p => {
  if (destaquesData[p.slug]) {
    const data = destaquesData[p.slug];
    p.genero = data.genero;
    p.familia_olfativa = data.familia;
    p.intensidade = data.intensidade;
    p.fixacao = data.fixacao;
    p.projecao = data.projecao;
    p.ocasiao = data.ocasiao;
    p.estacao = ['verao', 'outono'];
    p.estilo = data.estilo;
    p.similares_famosos = data.similares_famosos;
    p.preco_faixa = getPrecoFaixa(p.preco);
    p.destaque = data.destaque;
    p.piramide_olfativa = { topo: data.topo, coracao: data.coracao, fundo: data.fundo };
  } else {
    // Inferir dados para os outros
    const nomeLower = p.nome.toLowerCase();
    if (nomeLower.includes('feminino') || nomeLower.includes('femme') || nomeLower.includes('woman')) {
      p.genero = 'feminino';
    } else if (nomeLower.includes('masculino') || nomeLower.includes('homme') || nomeLower.includes('man') || nomeLower.includes('boy')) {
      p.genero = 'masculino';
    } else if (nomeLower.includes('unissex') || nomeLower.includes('kids')) {
      p.genero = 'unissex';
    } else {
      p.genero = 'unissex'; // Default fallback
    }

    if (nomeLower.includes('body cream') || nomeLower.includes('kids')) {
      p.familia_olfativa = 'doce';
    } else {
      p.familia_olfativa = 'amadeirada'; // Default
    }

    p.intensidade = 'moderada';
    p.fixacao = 3;
    p.projecao = 3;
    p.ocasiao = ['dia_a_dia', 'encontros'];
    p.estacao = ['verao', 'outono'];
    p.estilo = ['elegante', 'casual'];
    p.similares_famosos = [];
    p.preco_faixa = getPrecoFaixa(p.preco);
    if (typeof p.destaque === 'undefined') p.destaque = false;
  }
});

fs.writeFileSync(dbPath, JSON.stringify(db, null, 2), 'utf8');
console.log('Banco de dados enriquecido com sucesso!');
