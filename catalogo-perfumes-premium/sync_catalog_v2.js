const fs = require('fs');
const path = require('path');

const rawData = `Venti Silky Princess Fragrance World / Queen of Silk Creed - R$ 350,00
Afnan - Souvenir Desert Rose 100ml - R$ 400,00
Ajward Pattafa 60ml - R$ 300,00
Al Nobre Almeer Lattafa - R$ 350,00
Al Sheikh EDP 100ml da Sahari Collections - R$ 250,00
Al Ward - Sabah 100ml - R$ 300,00
Al Wataniah - Ameerati 100ml - R$ 300,00
Al Wataniah - Attar Al Wesal 100ml - R$ 300,00
Al Wataniah - Boraq 75ml - R$ 280,00
Al Wataniah - Durrat Al Aroo 85ml - R$ 300,00
Al Wataniah Al Layl EDP Unissex 100ml - R$ 290,00
Al Wataniah Ghala Eau de Parfum 100ml Feminino - R$ 300,00
Al Wataniah Kenz Al Malik 100ml - R$ 290,00
Al Wataniah Nawal Fluorite EDP 100ml Feminino - R$ 250,00
Al Wataniah Sultan Al Lail Original 100ml - R$ 240,00
Al Wataniah Tiara Pink Eau de Parfum 100ml - R$ 250,00
Al Wataniah Tibyan 100ml - R$ 249,90
Alpine Maison Alhambra - R$ 300,00
Amber Divine Passion Cool&Cool 100ml - R$ 450,00
Amnia Al Wataniah Compartilhável 100ml - R$ 330,00
Armaf - Infinity Gold 105ml - R$ 600,00
Asdaaf - Ameerat Al Arab 100ml - R$ 290,00
Asdaaf - Andaleeb Flora 100ml - R$ 280,00
Athena Maison Alhambra (inspirado na fragrância Goddess, da Burberry) 100ml - R$ 300,00
Attar Al Wesal Gold - R$ 400,00
B.A.D Femme Maison Alhambra 100ml - R$ 300,00
B.A.D Home 100ml Maison Alhambra - R$ 300,00
Bakhoorroyal Ocean Cool&Cool - R$ 450,00
Baroque Rouge 540 Maison Alhambra Compartilhável - R$ 300,00
Bayaan Lattafa 100ml - R$ 350,00
Blue Seduction Antonio Banderas 200ml - R$ 300,00
Bob My Pet (perfume para pet) - R$ 150,00
Body Cream Delilah Maison Alhambra 110g - R$ 210,00
Body Cream Delilah Maison Alhambra 110g 24h - R$ 240,00
Body Cream Hidratante Yara 305ml - R$ 300,00
Body Cream Hidratação Dear Body 200g - R$ 200,00
Body Creme Asad Black - R$ 300,00
Celeste Maison Alhambra 100ml - R$ 350,00
Chants Tenderina Maison Alhambra Feminino 100ml - R$ 300,00
Club de Nuit Maleka Armaf - R$ 450,00
Club de Nuit Woman Armaf Feminino - R$ 400,00
Como Moiselle Maison Alhambra - R$ 330,00
Creme Hidratante Body Cream 200g - Pote Pasta - R$ 190,00
Dalal Lattafa - R$ 590,00
Decantes - R$ 100,00
Delilah Blanc Maison Alhambra 100ml - R$ 400,00
Delilah Pour Femme EDP 100ml Maison Alhambra - R$ 350,00
Durrah Nicho Lattafa Perfumes Compartilhável - R$ 600,00
Eclaire Lattafa Perfumes Feminino 100ml - R$ 450,00
Eclat de Lune Maison Alhambra - R$ 300,00
El Ward Palais des Roses Eau de Parfum Unissex 100ml - R$ 290,00
Emaan Lattafa 100ml - R$ 350,00
Emper Al Fares Musk Effect Unissex 100ml EDP - R$ 250,00
Espada Intense Le Chameau Compartilhável 100ml - R$ 299,90
Extravagant Lover Maison Alhambra - R$ 350,00
Ferrari Black Masculino de Ferrari Eau de Toilette - R$ 300,00
Genius Rose Emper 100ml - R$ 250,00
Glacier Pour Homme Maison Alhambra - R$ 350,00
Habik For Men Lattafa Perfumes Masculino - R$ 450,00
Happy Brush Kids 75ml Lattafa Pride - R$ 200,00
Her Confession Lattafa Perfumes 100ml - R$ 450,00
His Confession Lattafa Perfumes - R$ 450,00
Intrude da Maison Alhambra / Givenchy L'Interdit - R$ 300,00
Ishq Al Shuyukh Silver Lattafa Perfumes - R$ 450,00
Jardim de Rêve Maison Alhambra 100ml - R$ 350,00
Jazzab Elixir Body Cream - R$ 280,00
Jorge di Profumo Deep Blue Maison Alhambra - R$ 250,00
Ju Ilant Vitality Maison Alhambra - R$ 250,00
Khamrah Lattafa Perfumes Compartilhável 100ml - R$ 350,00
Khanjar Lattafa Perfumes Compartilhável 85ml - R$ 600,00
Kit Souvenir Floral Bouquet - R$ 600,00
Kit Yara - 2 und: Yara Candy e Yara - R$ 550,00
La African Drummer Lattafa Pride - R$ 350,00
La Vivacitê Maison Alhambra 100ml - R$ 350,00
Lattafa - Afeef 100ml - R$ 700,00
Lattafa - Asad 100ml - R$ 300,00
Lattafa - Asad Bourbon 100ml - R$ 330,00
Lattafa - Asad Elixir 100ml - R$ 400,00
Lattafa - Atheeri 100ml - R$ 750,00
Lattafa - Fakhar 100ml - R$ 349,90
Lattafa - Fakhar Extrait Gold 100ml - R$ 349,90
Lattafa - Fakhar Platin 100ml - R$ 400,00
Lattafa - Fakhar Rose 100ml - R$ 350,00
Lattafa - Musamam White 100ml - R$ 550,00
Lattafa - Tharwah Gold 100ml - R$ 600,00
Lattafa - Yara 100ml - R$ 350,00
Lattafa Asad Zanzibar Limited Edition 100ml - R$ 350,00
Lattafa Pride La Collection D'Antiquités 1910 Eau de Parfum 100ml - R$ 399,90
Legend Intense Emper Eau de Toilette Masculino - R$ 290,00
Liwan Ard Zafaran - R$ 400,00
Mahib Adyan by Anfar 100ml - R$ 300,00
Maison Alhambra - Body Perfume Mist 250ml - R$ 150,00
Manaal - Ard Al Zaafaran 100ml - R$ 400,00
Marshmallow Blush Paris Corn - R$ 450,00
Mawwal - Basir 100ml - R$ 450,00
Mayer Lattafa - R$ 300,00
Maître de Blue Maison Alhambra Masculino 100ml - R$ 300,00
Mia Dolcezza Maison Alhambra - R$ 350,00
Milena Ard Al Zaafaran 100ml - R$ 450,00
Montaigne Vanille Maison Alhambra - R$ 300,00
Norah Lucher Adyan - R$ 300,00
Óleo Concentrado Yara Lattafa 20ml - R$ 250,00
Óleo Concentrado Al Wataniah 12ml - R$ 200,00
Olivia Maison Alhambra - R$ 300,00
Orientica Premium - Royal Amber 80ml - R$ 750,00
Perfume Armaf Club de Nuit Intense Man 105ml - R$ 450,00
Perfume Dar El Ward Oriental Oud EDP 100ml - R$ 290,00
Perfume Lattafa Qaed Al Fursan Black Eau de Parfum 90ml - R$ 290,00
Perfume Sahari Blue Sultan EDP Unisex 100ml - R$ 250,00
Petra Lattafa - R$ 450,00
Pink Eclipse Maison Alhambra - ref. olfativa Prada Paradoxe - 100ml - R$ 450,00
Pisa Lattafa Pride - R$ 500,00
Qaed Al Fursan Unlimited Lattafa Perfumes Compartilhável 90ml - R$ 350,00
Qarar Asdaaf 100ml - R$ 300,00
Queen of Arabia Lattafa Perfumes Feminino - R$ 700,00
Raneen Asdaaf 100ml - R$ 350,00
Reem Asdaaf / Lattafa Eau de Parfum 100ml - R$ 350,00
Rose Mystery Intense Maison Alhambra - R$ 390,00
Safeer Al Wald Ard Zafaran - R$ 300,00
Safeer Al Ward Creme Hidratante 450g - R$ 330,00
Salvo Eau de Parfum Maison Alhambra - R$ 350,00
Shahd de Lattafa - R$ 350,00
Shaheen Silver Lattafa - R$ 350,00
Shahreen Gold Lattafa - R$ 400,00
Sing Kids 75ml Lattafa Pride - R$ 200,00
So Candid Rouge Maison Alhambra 100ml - R$ 300,00
Spray Corporal e Cabelo Lattafa Haya 150ml - R$ 200,00
Spray Corporal e Cabelo Lattafa Yara 150ml - R$ 200,00
Spray Corporal e Capilar Mayer Lattafa 150ml - R$ 220,00
Summer Forever Maison Alhambra - inspirado na fragrância Muse, de Xerjoff - R$ 300,00
Teriaq Lattafa 100ml - R$ 350,00
Thahaani Al Wataniah Compartilhável 100ml - R$ 279,00
Tiramisu Caramel Zimaya 100ml - R$ 400,00
Uniq Armaf Effects Ok Uniq - R$ 450,00
Veneno Bianco French Avenue - R$ 600,00
Venti Carisma Fragrance World / Creed Carminda - R$ 350,00
Venti Sublime - R$ 350,00
Very Velvet Aqua Maison Alhambra - R$ 300,00
Victoria's Secret - Body Splash 250ml - R$ 180,00
Victorioso Nero Masculino Maison Alhambra Eau de Parfum 100ml - R$ 300,00
Vouge Night Maison Alhambra - R$ 300,00
Vougue Rouge Maison Alhambra - R$ 300,00
Vulcan Feu French Avenue Compartilhável 100ml - R$ 600,00
Watani Al Wataniah Feminino 100ml - R$ 250,00
Winners Trophy Gold Lattafa Pride - R$ 350,00
Yara Candy Lattafa 100ml - R$ 300,00
Yara Elixir Lattafa 100ml Feminino - R$ 400,00
Yara Tous Lattafa Perfumes Feminino 100ml - R$ 350,00
Yeah Man Partum - R$ 350,00
Your Touch Extrait Maison Alhambra / Stronger With You Intensely Armani - R$ 250,00
Yum Yum Armaf Feminino 100ml - R$ 600,00
Árabe Collection - Spray Corporal 200ml - R$ 60,00`;

const pdfData = rawData.split('\n').filter(Boolean).map(line => {
  const parts = line.split(' - R$ ');
  if (parts.length === 2) {
    const nome_pdf = parts[0].trim();
    const preco = parseFloat(parts[1].trim().replace(',', '.'));
    return { nome_pdf, preco };
  }
  return null;
}).filter(Boolean);

const dbPath = path.join(__dirname, 'src', 'data', 'db.json');
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

function norm(str) {
  return str.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]/g, '');
}

function extractGender(str) {
  const low = str.toLowerCase();
  if (low.includes('feminino') || low.includes('woman') || low.includes('femme')) return 'feminino';
  if (low.includes('masculino') || low.includes('home') || low.includes('homme') || low.includes('man') || low.includes('men')) return 'masculino';
  if (low.includes('unissex') || low.includes('compartilhavel') || low.includes('compartilhável') || low.includes('unisex')) return 'unissex';
  return null;
}

let matches = 0;

db.perfumes.forEach(p => {
  let bestMatch = null;
  let highestScore = 0;
  
  pdfData.forEach(pdfItem => {
    const wordsDB = p.nome.toLowerCase().split(/\s+/).filter(w => w.length > 2);
    let score = 0;
    wordsDB.forEach(w => {
      if (pdfItem.nome_pdf.toLowerCase().includes(w)) score++;
    });
    
    if (score > highestScore) {
      highestScore = score;
      bestMatch = pdfItem;
    }
  });

  if (bestMatch && highestScore > 0) {
    p.nome = bestMatch.nome_pdf; // ALSO update the exact name
    p.preco = bestMatch.preco;
    const g = extractGender(bestMatch.nome_pdf);
    if (g) p.genero = g;
    matches++;
  }
  
  if (p.preco <= 250) p.preco_faixa = 'ate_250';
  else if (p.preco <= 350) p.preco_faixa = 'ate_350';
  else if (p.preco <= 500) p.preco_faixa = 'ate_500';
  else p.preco_faixa = 'acima_500';
});

fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
console.log('Matches encontrados: ', matches);
