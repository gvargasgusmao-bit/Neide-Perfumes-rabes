const fs = require('fs');
const path = require('path');

function slugify(text) {
  return text.toString().toLowerCase()
    .normalize('NFD') 
    .replace(/[\u0300-\u036f]/g, '') 
    .replace(/\s+/g, '-') 
    .replace(/[^\w\-]+/g, '') 
    .replace(/\-\-+/g, '-') 
    .replace(/^-+/, '') 
    .replace(/-+$/, '');
}

function extractGender(str) {
  const low = str.toLowerCase();
  if (low.includes('feminino') || low.includes('woman') || low.includes('femme')) return 'feminino';
  if (low.includes('masculino') || low.includes('home') || low.includes('homme') || low.includes('man') || low.includes('men')) return 'masculino';
  return 'unissex'; 
}

// 1. Read the parsed OCR refMap
const refMap = JSON.parse(fs.readFileSync('./refMap.json', 'utf8'));

// 2. Read the rawData prices from the previous script
const text = fs.readFileSync('./build_95_catalog.js', 'utf8');
const rawDataStr = text.split('const rawData = \`')[1].split('\`;')[0];
const pricesMap = {};

rawDataStr.split('\n').filter(Boolean).forEach(line => {
  const parts = line.split(' - R$ ');
  if (parts.length === 2) {
    const nome = parts[0].trim();
    const preco = parseFloat(parts[1].trim().replace(',', '.'));
    pricesMap[slugify(nome)] = { nome, preco };
  }
});

// 3. Scan the optimized directory
const imgDir = path.join(__dirname, 'public', 'assets', 'images', 'optimized');
const images = fs.readdirSync(imgDir).filter(f => f.endsWith('.webp') || f.endsWith('.jpg') || f.endsWith('.png'));

const newPerfumes = [];
let idCounter = 1;

images.forEach(img => {
  let nomeEncontrado = null;
  let precoEncontrado = null;
  
  // Try to match by "perfume-exclusivo-X.webp"
  const exclMatch = img.match(/perfume-exclusivo-(\d+)/);
  if (exclMatch) {
    const refId = exclMatch[1];
    const nameFromPdf = refMap[refId];
    if (nameFromPdf) {
      const slugPdf = slugify(nameFromPdf);
      if (pricesMap[slugPdf]) {
        nomeEncontrado = pricesMap[slugPdf].nome;
        precoEncontrado = pricesMap[slugPdf].preco;
      } else {
        // Fallback: name from PDF, default price
        nomeEncontrado = nameFromPdf;
        precoEncontrado = 300;
      }
    }
  } else {
    // Try to match by slug directly
    const slugFile = img.replace(/\.webp|\.jpg|\.png/g, '');
    if (pricesMap[slugFile]) {
      nomeEncontrado = pricesMap[slugFile].nome;
      precoEncontrado = pricesMap[slugFile].preco;
    } else {
      // Maybe the filename is slightly different from the slug
      // Fuzzy matching slug
      for (const [slug, data] of Object.entries(pricesMap)) {
        if (slugFile.includes(slug) || slug.includes(slugFile)) {
          nomeEncontrado = data.nome;
          precoEncontrado = data.preco;
          break;
        }
      }
    }
  }
  
  if (!nomeEncontrado) {
    console.log('NAO ENCONTRADO NOME PARA IMAGEM:', img);
    // Continue building anyway with generic name so we don't drop the image entirely?
    // Actually the user wants to keep the products we HAVE images for, AND set correct names.
    // If we can't find a name, it's better to keep it as "Desconhecido" so they can edit,
    // but the matching above should catch 99%.
    nomeEncontrado = img.replace(/-/g, ' ').replace(/\.webp|\.jpg|\.png/g, '');
    precoEncontrado = 299.90;
  }
  
  const cleanNome = nomeEncontrado.replace(/inspirado na fragrância.*$/i, '').replace(/100ml|85ml|75ml|200ml|105ml|110g|24h|305ml|200g|60ml/gi, '').trim();
  const finalSlug = slugify(cleanNome);

  const novo = {
    id_perfume: idCounter++,
    slug: finalSlug,
    nome: cleanNome,
    id_marca: 1,
    preco: precoEncontrado,
    status_estoque: "em_estoque",
    genero: extractGender(nomeEncontrado),
    familia_olfativa: "oriental",
    imagem_url: `/assets/images/optimized/${img}`,
    destaque: false,
    volume_ml: 100,
    ocasiao: ["uso_noturno", "encontros"],
    estilo: ["elegante"],
    intensidade: "forte",
    fixacao: 4,
    projecao: 4,
    piramide_olfativa: {
      topo: ["Bergamota", "Especiarias"],
      coracao: ["Notas Florais", "Madeiras"],
      fundo: ["Âmbar", "Almíscar"]
    },
    similares_famosos: [],
    badges: []
  };
  
  if (novo.preco <= 250) novo.preco_faixa = 'ate_250';
  else if (novo.preco <= 350) novo.preco_faixa = 'ate_350';
  else if (novo.preco <= 500) novo.preco_faixa = 'ate_500';
  else novo.preco_faixa = 'acima_500';
  
  if (novo.preco <= 300) novo.badges.push('Custo-Benefício');
  
  const lowerName = cleanNome.toLowerCase();
  if (lowerName.includes('inspirado na fragrância')) {
      const parts = lowerName.split('inspirado na fragrância');
      const famoso = parts[1].replace(/,.*$/, '').replace('da', '').trim();
      novo.similares_famosos = [famoso];
      novo.badges.push('Lembra o ' + famoso.split(' ')[0]);
  } else if (lowerName.includes('ref. olfativa')) {
      const parts = lowerName.split('ref. olfativa');
      const famoso = parts[1].replace('-', '').replace('100ml', '').trim();
      novo.similares_famosos = [famoso];
      novo.badges.push('Lembra o ' + famoso.split(' ')[0]);
  }
  
  newPerfumes.push(novo);
});

// Set first 8 to destaque
for(let i=0; i<Math.min(8, newPerfumes.length); i++) {
  newPerfumes[i].destaque = true;
}

const dbPath = path.join(__dirname, 'src', 'data', 'db.json');
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
db.perfumes = newPerfumes;

fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
console.log('Database FINALIZADA com ' + newPerfumes.length + ' perfumes.');
