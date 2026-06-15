const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'src', 'data', 'db.json');
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

// Mapa de perfumes conhecidos para gêneros e famílias reais
const MAPA_REAL = {
  'club de nuit maleka': { genero: 'feminino', familia: 'floral' },
  'asad black': { genero: 'masculino', familia: 'especiada' },
  'musamam white': { genero: 'unissex', familia: 'floral' },
  'sabah al ward': { genero: 'feminino', familia: 'floral' },
  'bareeq al dhahab': { genero: 'masculino', familia: 'amadeirada' },
  'club de nuit intense man': { genero: 'masculino', familia: 'citrica' },
  'boraq': { genero: 'masculino', familia: 'amadeirada' },
  'khamrah': { genero: 'unissex', familia: 'doce' },
  'yara': { genero: 'feminino', familia: 'doce' },
  'fakhar': { genero: 'masculino', familia: 'amadeirada' },
  'ameer al oudh': { genero: 'unissex', familia: 'oud' },
  'najdia': { genero: 'masculino', familia: 'citrica' },
  'bade ee al oud': { genero: 'unissex', familia: 'especiada' }
};

const familiasPossiveis = ['doce', 'baunilha', 'frutada', 'floral', 'amadeirada', 'citrica', 'especiada', 'oriental', 'couro', 'oud'];
const ocasioesPossiveis = ['trabalho', 'dia_a_dia', 'academia', 'encontros', 'eventos', 'festas', 'uso_noturno'];
const estilosPossiveis = ['elegante', 'sedutor', 'sofisticado', 'jovem', 'luxuoso', 'executivo', 'casual'];
const intensidades = ['suave', 'moderada', 'forte', 'muito_marcante'];

let fIdx = 0;
let oIdx = 0;
let eIdx = 0;

db.perfumes.forEach((p, index) => {
  const nomeLower = p.nome.toLowerCase();
  
  // Tenta encontrar no mapa
  let encontrou = false;
  for (const [key, data] of Object.entries(MAPA_REAL)) {
    if (nomeLower.includes(key)) {
      p.genero = data.genero;
      p.familia_olfativa = data.familia;
      encontrou = true;
      break;
    }
  }

  // Se não encontrou no mapa (genéricos ou desconhecidos), distribui uniformemente
  if (!encontrou) {
    if (index % 3 === 0) p.genero = 'masculino';
    else if (index % 3 === 1) p.genero = 'feminino';
    else p.genero = 'unissex';

    p.familia_olfativa = familiasPossiveis[fIdx % familiasPossiveis.length];
    fIdx++;
  }

  // Define as outras características distribuídas para garantir que o quiz e filtros funcionem com dados ricos
  const numOcasioes = (index % 3) + 1; // 1 a 3 ocasiões
  p.ocasiao = [];
  for(let i=0; i<numOcasioes; i++){
    p.ocasiao.push(ocasioesPossiveis[(oIdx++) % ocasioesPossiveis.length]);
  }

  const numEstilos = (index % 2) + 1; // 1 a 2 estilos
  p.estilo = [];
  for(let i=0; i<numEstilos; i++){
    p.estilo.push(estilosPossiveis[(eIdx++) % estilosPossiveis.length]);
  }

  p.intensidade = intensidades[index % intensidades.length];
  p.fixacao = (index % 3) + 3; // 3 a 5
  p.projecao = (index % 3) + 3; // 3 a 5
  
  // Preços variados entre 150 e 600
  if(p.nome.includes("Exclusivo")) {
    p.preco = 150 + (index * 15) % 450; 
  }
});

fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
console.log('Banco de dados atualizado com gêneros, famílias e características distribuídas!');
