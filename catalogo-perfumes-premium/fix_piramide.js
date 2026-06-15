const fs = require('fs');
const path = require('path');
const dbPath = path.join(__dirname, 'src', 'data', 'db.json');
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

// Pirâmides padrão por família olfativa
const PIRAMIDES_PADRAO = {
  floral:     { topo: ['Bergamota', 'Aldeídos'], coracao: ['Rosa', 'Jasmim', 'Peônia'], fundo: ['Almíscar', 'Sândalo', 'Âmbar'] },
  amadeirada: { topo: ['Bergamota', 'Cardamomo'], coracao: ['Cedro', 'Sândalo', 'Vetiver'], fundo: ['Âmbar', 'Baunilha', 'Almíscar'] },
  oriental:   { topo: ['Saffron', 'Bergamota'], coracao: ['Oud', 'Rosa', 'Jasmim'], fundo: ['Âmbar', 'Almíscar', 'Incenso'] },
  citrica:    { topo: ['Bergamota', 'Limão', 'Laranja'], coracao: ['Lavanda', 'Cedro'], fundo: ['Almíscar', 'Âmbar'] },
  especiada:  { topo: ['Pimenta', 'Cardamomo'], coracao: ['Patchouli', 'Cedro'], fundo: ['Baunilha', 'Âmbar', 'Almíscar'] },
  oud:        { topo: ['Saffron', 'Bergamota'], coracao: ['Oud', 'Rosa'], fundo: ['Âmbar', 'Almíscar', 'Incenso'] },
  doce:       { topo: ['Bergamota', 'Framboesa'], coracao: ['Rosa', 'Peônia'], fundo: ['Baunilha', 'Almíscar', 'Âmbar'] },
  baunilha:   { topo: ['Bergamota', 'Pera'], coracao: ['Rosa', 'Jasmim'], fundo: ['Baunilha', 'Sândalo', 'Âmbar'] },
  frutada:    { topo: ['Pêssego', 'Pera', 'Bergamota'], coracao: ['Rosa', 'Jasmim'], fundo: ['Almíscar', 'Cedro'] },
  couro:      { topo: ['Bergamota', 'Cardamomo'], coracao: ['Couro', 'Sândalo', 'Cedro'], fundo: ['Âmbar', 'Almíscar', 'Vetiver'] },
};
const PADRAO_GENERICO = { topo: ['Bergamota', 'Aldeídos'], coracao: ['Rosa', 'Jasmim'], fundo: ['Almíscar', 'Âmbar', 'Sândalo'] };

let corrigidos = 0;
db.perfumes.forEach(p => {
  if (!p.piramide_olfativa || !p.piramide_olfativa.topo) {
    const familia = (p.familia_olfativa || '').toLowerCase();
    p.piramide_olfativa = PIRAMIDES_PADRAO[familia] || PADRAO_GENERICO;
    corrigidos++;
  }
  // Garante que slug existe
  if (!p.slug) {
    p.slug = p.nome.toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .substring(0, 80);
  }
});

fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
console.log(`Corrigidos: ${corrigidos} perfumes sem pirâmide olfativa.`);
