const fs = require('fs');
const path = require('path');

const pdfData = [
  { nome_pdf: "/Venti Silky Princess Fragrance World/ Queen of Silk Creed", preco: 350 },
  { nome_pdf: "Afnan - Souvenir Desert Rose 100 ml", preco: 400 },
  { nome_pdf: "ajward pattafa 60ml", preco: 300 },
  { nome_pdf: "al nobre almeer lattafa", preco: 350 },
  { nome_pdf: "Al Sheikh EDP 100 ml da Sahari Collections", preco: 250 },
  { nome_pdf: "Al Ward - Sabah 100ml", preco: 300 },
  { nome_pdf: "Al Wataniah - Ameerati 100 ml", preco: 300 },
  { nome_pdf: "Al Wataniah - Attar Al Wesal 100 ml", preco: 300 },
  { nome_pdf: "Al Wataniah - Boraq 75 ml", preco: 280 },
  { nome_pdf: "Al Wataniah - Durrat Al Aroo 85 ml", preco: 300 },
  { nome_pdf: "AL WATANIAH AL LAYL EDP UNISSEX 100ML", preco: 290 },
  { nome_pdf: "Al Wataniah Ghala Eau De Parfum 100ml Feminino", preco: 300 },
  { nome_pdf: "Al Wataniah Kenz Al Malik 100ml", preco: 290 },
  { nome_pdf: "AL WATANIAH NAWAL FLUORITE EDP 100ML FEMININO", preco: 250 },
  { nome_pdf: "Al Wataniah Sultan Al Lail Original - 100ml", preco: 240 },
  { nome_pdf: "Al Wataniah Tiara Pink Eau de Parfum 100ml", preco: 250 },
  { nome_pdf: "AL WATANIAH TIBYAN 100ML", preco: 249.9 },
  { nome_pdf: "alpine maison alhambra", preco: 300 },
  { nome_pdf: "Amber Divine Passion Cool&Cool 100ml", preco: 450 },
  { nome_pdf: "amnia Al Wataniah Compartilhável 100ml", preco: 330 },
  { nome_pdf: "Armaf - Infinity Gold 105 ml", preco: 600 },
  { nome_pdf: "Asdaaf - Ameerat Al Arab 100 ml", preco: 290 },
  { nome_pdf: "Asdaaf - Andaleeb Flora 100 ml", preco: 280 },
  { nome_pdf: "Athena Maison Alhambra inspirado na fragrância Goddess da Burberry. 100ml", preco: 300 },
  { nome_pdf: "attar al wesal gold", preco: 400 },
  { nome_pdf: "B.A.D FEMME maison alhambra 100ml", preco: 300 },
  { nome_pdf: "B.A.D home 100 ml maison two mission alhambra", preco: 300 },
  { nome_pdf: "Bakhoorroyal ocean cool&cool", preco: 450 },
  { nome_pdf: "Baroque Rouge 540 Maison Alhambra Compartilhável", preco: 300 },
  { nome_pdf: "bayaan lattafa 100ml", preco: 350 },
  { nome_pdf: "Blue Seduction Antonio Banderas 200ml", preco: 300 },
  { nome_pdf: "bob my pet perfume para pet", preco: 150 },
  { nome_pdf: "body cream delilah maison alhambra 110g", preco: 210 },
  { nome_pdf: "body cream delilah maison alhambra 110g 24h", preco: 240 },
  { nome_pdf: "body cream hidratante yara 305ml", preco: 300 },
  { nome_pdf: "body creame hodrattion dear body dv 200g", preco: 200 },
  { nome_pdf: "body creme asad black", preco: 300 },
  { nome_pdf: "celeste Maison Alhambra 100ml", preco: 350 },
  { nome_pdf: "Chants Tenderina Maison Alhambra Feminino 100ml", preco: 300 },
  { nome_pdf: "Club De Nuit Maleka Armaf", preco: 450 },
  { nome_pdf: "Club de Nuit Woman Armaf Feminino", preco: 400 },
  { nome_pdf: "Como Moiselle Maison Alhambra", preco: 330 },
  { nome_pdf: "Creme Hidratante Body Cream 200g - Pote Pasta.", preco: 190 },
  { nome_pdf: "dalal lattafa", preco: 590 },
  { nome_pdf: "decantes", preco: 100 },
  { nome_pdf: "Delilah Blanc Maison Alhambra 100ml", preco: 400 },
  { nome_pdf: "Delilah Pour Femme EDP 100ml Maison Alhambra", preco: 350 },
  { nome_pdf: "Durrah nicho Lattafa Perfumes Compartilhável", preco: 600 },
  { nome_pdf: "Eclaire Lattafa Perfumes Feminino 100ml", preco: 450 },
  { nome_pdf: "Eclat De Lune Maison Alhambra", preco: 300 },
  { nome_pdf: "El Ward Palais Des Roses Eau de Parfum Unissex 100ML", preco: 290 },
  { nome_pdf: "emaan lattafa 100ml", preco: 350 },
  { nome_pdf: "Emper Al Fares Musk Effect Unissex 100ml EDP Ref olfativa: Musk Therapy Initio", preco: 250 },
  { nome_pdf: "Espada Intense Le Chameau Compartilhável 100ml", preco: 299.9 },
  { nome_pdf: "extravagant lover maison alhambra", preco: 350 },
  { nome_pdf: "Ferrari Black Masculino De Ferrari Eau De Toilette", preco: 300 },
  { nome_pdf: "genius rose emper 100ml", preco: 250 },
  { nome_pdf: "glacier pour homme maison alhambra", preco: 350 },
  { nome_pdf: "Habik For Men Lattafa Perfumes Masculino", preco: 450 },
  { nome_pdf: "happy brush kids 75ml lattafa pride", preco: 200 },
  { nome_pdf: "Her Confession Lattafa Perfumes 100ml", preco: 450 },
  { nome_pdf: "His Confession Lattafa Perfumes", preco: 450 },
  { nome_pdf: "Intrude da Maison Alhambra / Givenchy LInterdit", preco: 300 },
  { nome_pdf: "Ishq Al Shuyukh Silver Lattafa Perfumes", preco: 450 },
  { nome_pdf: "jardim de reve maison alhambra 100ml", preco: 350 },
  { nome_pdf: "jazzab elixir body cream", preco: 280 },
  { nome_pdf: "jorge di profumo deep blue maison alhambra", preco: 250 },
  { nome_pdf: "ju ilant vitality maison alhambra", preco: 250 },
  { nome_pdf: "Khamrah Lattafa Perfumes Compartilhável 100ml", preco: 350 },
  { nome_pdf: "Khanjar Lattafa Perfumes Compartilhável 85ml", preco: 600 },
  { nome_pdf: "kit souvenir floral bouquet", preco: 600 },
  { nome_pdf: "kit yara 2 und yara candy e yara", preco: 550 },
  { nome_pdf: "la african drummer lattafa pride", preco: 350 },
  { nome_pdf: "la vivacitê maison alhambra 100ml", preco: 350 },
  { nome_pdf: "Lattafa - Afeef 100 ml", preco: 700 },
  { nome_pdf: "Lattafa - Asad 100 ml", preco: 300 },
  { nome_pdf: "Lattafa - Asad Bourbon 100ml", preco: 330 },
  { nome_pdf: "LATTAFA - ASAD ELIXIR 100ml", preco: 400 },
  { nome_pdf: "Lattafa - Atheeri 100 ml", preco: 750 },
  { nome_pdf: "Lattafa - Fakhar 100 ml", preco: 349.9 },
  { nome_pdf: "Lattafa - Fakhar Extrait Gold 100 ml", preco: 349.9 },
  { nome_pdf: "Lattafa - Fakhar Platin 100 ml", preco: 400 },
  { nome_pdf: "Lattafa - Fakhar Rose 100 ml", preco: 350 },
  { nome_pdf: "Lattafa - Musamam White 100 ml", preco: 550 },
  { nome_pdf: "Lattafa - THARWAH GOLD 100 ml", preco: 600 },
  { nome_pdf: "Lattafa - Yara 100 ml", preco: 350 },
  { nome_pdf: "Lattafa Asad Zanzibar Limited Edition 100ml", preco: 350 },
  { nome_pdf: "Lattafa Pride La Collection Dantiquités 1910 Eau de Parfum 100ml", preco: 399.9 },
  { nome_pdf: "Legend Intense Emper Eau de Toilette Masculino", preco: 290 },
  { nome_pdf: "liwan ard zafaran", preco: 400 },
  { nome_pdf: "mahib adyan by anfar 100ml", preco: 300 },
  { nome_pdf: "Maison Alhambra - Body perfume Mist 250ml", preco: 150 },
  { nome_pdf: "Manaal - Ard Al Zaafaran 100 ml", preco: 400 },
  { nome_pdf: "Marshmallow Blush paris corn", preco: 450 },
  { nome_pdf: "Mawwal - Basir 100 ml", preco: 450 },
  { nome_pdf: "mayer lattafa", preco: 300 },
  { nome_pdf: "Maître de Blue Maison Alhambra Masculino ism Blue de chanel 100ml", preco: 300 },
  { nome_pdf: "Mia Dolcezza Maison Alhambra", preco: 350 },
  { nome_pdf: "Milena Ard Al Zaafaran 100ml", preco: 450 },
  { nome_pdf: "montaigne vanille maison alhambra", preco: 300 },
  { nome_pdf: "norah lucher adyan", preco: 300 },
  { nome_pdf: "oleo comcentrado yara lattafa 20ml dv", preco: 250 },
  { nome_pdf: "oleo concentrado al wataniah 12ml", preco: 200 },
  { nome_pdf: "olivia maison alhambra", preco: 300 },
  { nome_pdf: "Orientica Premium - Royal Amber 80ml", preco: 750 },
  { nome_pdf: "Perfume ARMAF Club de nuit intense man 105 ml", preco: 450 },
  { nome_pdf: "PERFUME DAR EL WARD ORIENTAL OUD EDP 100ML", preco: 290 },
  { nome_pdf: "PERFUME LATTAFA QAED AL FURSAN BLACK EAU DE PARFUM 90ML", preco: 290 },
  { nome_pdf: "Perfume Sahari Blue Sultan EDP - Unisex 100mL", preco: 250 },
  { nome_pdf: "petra lattafa", preco: 450 },
  { nome_pdf: "Pink Eclipse Maison Alhambra Ref. Olfativa Prada Paradoxe 100ml", preco: 450 },
  { nome_pdf: "pisa lattafa pride", preco: 500 },
  { nome_pdf: "Qaed Al Fursan Unlimited Lattafa Perfumes Compartilhável 90ml", preco: 350 },
  { nome_pdf: "qarar asdaaf 100ml", preco: 300 },
  { nome_pdf: "Queen Of Arabia Lattafa Perfumes Feminino", preco: 700 },
  { nome_pdf: "RANEEN ASDAAF 100ml", preco: 350 },
  { nome_pdf: "Reem asdaaf / lattafa eau de parfum 100ml", preco: 350 },
  { nome_pdf: "rose mystery intense maison alhambra", preco: 390 },
  { nome_pdf: "safeer al wald ard zafaran", preco: 300 },
  { nome_pdf: "safeer al ward creme hidratante 450g", preco: 330 },
  { nome_pdf: "salvo eau de parfum maison alhambra", preco: 350 },
  { nome_pdf: "Shahd de Lattafa", preco: 350 },
  { nome_pdf: "shaheen silver lattafa", preco: 350 },
  { nome_pdf: "shahreen gold lattafa", preco: 400 },
  { nome_pdf: "Sing Kids 75ml Lattafa Pride", preco: 200 },
  { nome_pdf: "So Candid rouge Maison Alhambra 100ml", preco: 300 },
  { nome_pdf: "SPRAY CORPORAL E CABELO LATTAFA HAYA 150ML", preco: 200 },
  { nome_pdf: "Spray Corporal e cabelo Lattafa Yara 150 Ml", preco: 200 },
  { nome_pdf: "spray corporal e capilar mayer lattafa 150ml", preco: 220 },
  { nome_pdf: "Summer Forever Maison Alhambra / Inspirado na fragrância Muse de Xerjoff", preco: 300 },
  { nome_pdf: "teriaq lattafa 100ml", preco: 350 },
  { nome_pdf: "Thahaani Al Wataniah Compartilhável 100ml", preco: 279 },
  { nome_pdf: "tiramisu caramel zimaya 100ml", preco: 400 },
  { nome_pdf: "uniq armaf effects ok uniq", preco: 450 },
  { nome_pdf: "Veneno Bianco French Avenue", preco: 600 },
  { nome_pdf: "Venti Carisma Fragrance World / creed carminda", preco: 350 },
  { nome_pdf: "venti sublime", preco: 350 },
  { nome_pdf: "very velvet aqua maison alhambra", preco: 300 },
  { nome_pdf: "Victorias s Secret - Body Splash 250 ml", preco: 180 },
  { nome_pdf: "Victorioso Nero Masculino Maison Alhambra Eau de Parfum 100 ml", preco: 300 },
  { nome_pdf: "vouge night maison alhambra", preco: 300 },
  { nome_pdf: "vougue rouge maison alhanbra", preco: 300 },
  { nome_pdf: "Vulcan Feu French Avenue Compartilhável 100ml", preco: 600 },
  { nome_pdf: "Watani Al Wataniah Feminino 100ml", preco: 250 },
  { nome_pdf: "winners trophy gold lattafa pride", preco: 350 },
  { nome_pdf: "yara candy lattafa 100ml", preco: 300 },
  { nome_pdf: "Yara Elixir Lattafa 100ml Feminino", preco: 400 },
  { nome_pdf: "Yara Tous Lattafa Perfumes Feminino 100ml", preco: 350 },
  { nome_pdf: "yeah man partum", preco: 350 },
  { nome_pdf: "your touch extrait maison alhambra / Stronger With You Intensely armani", preco: 250 },
  { nome_pdf: "Yum Yum Armaf Feminino 100ml", preco: 600 },
  { nome_pdf: "Árabe Collection - Spray Corporal 200 ml", preco: 60 }
];

const dbPath = path.join(__dirname, 'src', 'data', 'db.json');
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

// Helper to normalize strings
function norm(str) {
  return str.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]/g, '');
}

// Extract gender from string
function extractGender(str) {
  const low = str.toLowerCase();
  if (low.includes('feminino') || low.includes('woman') || low.includes('femme')) return 'feminino';
  if (low.includes('masculino') || low.includes('home') || low.includes('homme') || low.includes('man') || low.includes('men')) return 'masculino';
  if (low.includes('unissex') || low.includes('compartilhavel') || low.includes('compartilhável') || low.includes('unisex')) return 'unissex';
  return null;
}

let matches = 0;

// Add new badges logic setup while looping
db.perfumes.forEach(p => {
  const normalizedDBName = norm(p.slug || p.nome);
  
  // Find best match in pdfData
  let bestMatch = null;
  let highestScore = 0;
  
  pdfData.forEach(pdfItem => {
    const normPdf = norm(pdfItem.nome_pdf);
    // Intersection of words
    const wordsDB = p.nome.toLowerCase().split(/\s+/).filter(w => w.length > 2);
    const wordsPdf = pdfItem.nome_pdf.toLowerCase().split(/\s+/).filter(w => w.length > 2);
    
    let score = 0;
    wordsDB.forEach(w => {
      if (pdfItem.nome_pdf.toLowerCase().includes(w)) score++;
    });
    
    // Check if it's the highest
    if (score > highestScore) {
      highestScore = score;
      bestMatch = pdfItem;
    }
  });

  if (bestMatch && highestScore > 0) {
    p.preco = bestMatch.preco;
    // Extract gender if available in the PDF name
    const g = extractGender(bestMatch.nome_pdf);
    if (g) p.genero = g;
    matches++;
  } else {
    // try to guess gender from current name
    const g = extractGender(p.nome);
    if (g) p.genero = g;
  }
  
  // Update price ranges
  if (p.preco <= 250) p.preco_faixa = 'ate_250';
  else if (p.preco <= 350) p.preco_faixa = 'ate_350';
  else if (p.preco <= 500) p.preco_faixa = 'ate_500';
  else p.preco_faixa = 'acima_500';

  // Seed badges array if doesn't exist
  if (!p.badges) {
    p.badges = [];
    if (p.destaque) p.badges.push('Mais Vendido');
    if (p.fixacao === 5) p.badges.push('Fixação Extrema');
    if (p.preco <= 300) p.badges.push('Custo-Benefício');
  }
  
  // Also parse similares to seed "Inspirado no" badge
  if (p.similares_famosos && p.similares_famosos.length > 0) {
    // Only first one to avoid visual clutter
    const famoso = p.similares_famosos[0].split(' ').slice(0,2).join(' '); // just two words
    const badgeStr = 'Lembra o ' + famoso;
    if (!p.badges.includes(badgeStr)) p.badges.push(badgeStr);
  }
});

fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
console.log('Matches encontrados: ', matches);
