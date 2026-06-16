const fs = require('fs');

const ocrText = `Página 1 de 31
/Venti Silky Princess Fragrance World/ Queen of Silk Creed
ref:338
R$ 350,00
Afnan - Souvenir Desert Rose 100 ml
ref:26
R$ 400,00
ajward pattafa 60ml
ref:428
R$ 300,00
Página 2 de 31
al nobre almeer lattafa
ref:438,00
R$ 350,00
Al Sheikh EDP 100 ml da Sahari Collections
ref:262
R$ 250,00
Al Ward - Sabah 100ml
ref:37
R$ 300,00
Al Wataniah - Ameerati 100 ml
ref:27
R$ 300,00
Al Wataniah - Attar Al Wesal 100 ml
ref:28
R$ 300,00
Página 3 de 31
Al Wataniah - Boraq 75 ml
ref:51
R$ 280,00
Al Wataniah - Durrat Al Aroo 85 ml
ref:14
R$ 300,00
AL WATANIAH AL LAYL EDP UNISSEX 100ML
ref:115
R$ 290,00
Al Wataniah Ghala Eau De Parfum 100ml Feminino | Original +
ref:85
R$ 300,00
Al Wataniah Kenz Al Malik 100ml
ref:65
R$ 290,00
Página 4 de 31
AL WATANIAH NAWAL FLUORITE EDP 100ML FEMININO
ref:297
R$ 250,00
Al Wataniah Sultan Al Lail Original - 100ml
ref:66
R$ 240,00
Al Wataniah Tiara Pink Eau de Parfum 100ml
ref:302
R$ 250,00
AL WATANIAH TIBYAN 100ML
ref:203
R$ 249,90
alpine maison alhambra
ref:454
R$ 300,00
Página 5 de 31
Amber Divine Passion Cool&Cool 100ml
ref:418
R$ 450,00
amnia Al Wataniah Compartilhável 100ml
ref:349
R$ 330,00
Armaf - Infinity Gold 105 ml
ref:53
R$ 600,00
Asdaaf - Ameerat Al Arab 100 ml
ref:56
R$ 290,00
Asdaaf - Andaleeb Flora 100 ml
ref:58
R$ 280,00
Página 6 de 31
Athena Maison Alhambra inspirado na fragrância Goddess da Burberry. 100ml
ref:198
R$ 300,00
attar al wesal gold
ref:458
R$ 400,00
B.A.D FEMME maison alhambra 100ml
ref:354
R$ 300,00
B.A.D home 100 ml maison two mission alhambra
ref:353
R$ 300,00
Bakhoorroyal ocean cool&cool
ref:417
R$ 450,00
Página 7 de 31
Baroque Rouge 540 Maison Alhambra Compartilhável
ref:207
R$ 300,00
bayaan lattafa 100ml
ref:426
R$ 350,00
Blue Seduction Antonio Banderas 200ml
ref:211
R$ 300,00
bob my pet perfume para pet
ref:437
R$ 150,00
body cream delilah maison alhambra 110g
ref:457
R$ 210,00
Página 8 de 31
body cream delilah maison alhambra 110g 24h
ref:447
R$ 240,00
body cream hidratante yara 305ml
ref:401
R$ 300,00
body creame hodrattion dear body dv 200g
ref:459
R$ 200,00
body creme asad black
ref:424
R$ 300,00
celeste Maison Alhambra 100ml
ref:299
R$ 350,00
Página 9 de 31
Chants Tenderina Maison Alhambra Feminino 100ml
ref:300
R$ 300,00
Club De Nuit Maleka Armaf
ref:336
R$ 450,00
Club de Nuit Woman Armaf Feminino
ref:242
R$ 400,00
Como Moiselle Maison Alhambra
ref:268
R$ 330,00
Creme Hidratante Body Cream 200g - Pote Pasta.
ref:141
R$ 190,00
Página 10 de 31
dalal lattafa
ref:421
R$ 590,00
decantes
ref:435
R$ 100,00
Delilah Blanc Maison Alhambra 100ml
ref:196
R$ 400,00
Delilah Pour Femme EDP 100ml Maison Alhambra
ref:169
R$ 350,00
Durrah nicho Lattafa Perfumes Compartilhável
ref:276
R$ 600,00
Página 11 de 31
Eclaire Lattafa Perfumes Feminino 100ml
ref:202
R$ 450,00
Eclat De Lune Maison Alhambra
ref:247
R$ 300,00
El Ward Palais Des Roses Eau de Parfum Unissex 100ML
ref:248
R$ 290,00
emaan lattafa 100ml
ref:420
R$ 350,00
Emper Al Fares Musk Effect Unissex 100ml EDP Ref olfativa: Musk Therapy Initio
ref:254
R$ 250,00
Página 12 de 31
Espada Intense Le Chameau Compartilhável 100ml
ref:193
R$ 299,90
extravagant lover maison alhambra
ref:431
R$ 350,00
Ferrari Black Masculino De Ferrari Eau De Toilette
ref:184
R$ 300,00
genius rose emper 100ml
ref:356
R$ 250,00
glacier pour homme maison alhambra
ref:415
R$ 350,00
Página 13 de 31
Habik For Men Lattafa Perfumes Masculino
ref:236
R$ 450,00
happy brush kids 75ml lattafa pride
ref:333
R$ 200,00
Her Confession Lattafa Perfumes 100ml
ref:188
R$ 450,00
His Confession Lattafa Perfumes
ref:282
R$ 450,00
Intrude da Maison Alhambra / Givenchy LInterdit
ref:322
R$ 300,00
Página 14 de 31
Ishq Al Shuyukh Silver Lattafa Perfumes
ref:281
R$ 450,00
jardim de reve maison alhambra 100ml
ref:416
R$ 350,00
jazzab elixir body cream
ref:456
R$ 280,00
jorge di profumo deep blue maison alhambra
ref:327
R$ 250,00
ju ilant vitality maison alhambra
ref:380
R$ 250,00
Página 15 de 31
Khamrah Lattafa Perfumes Compartilhável 100ml
ref:293
R$ 350,00
Khanjar Lattafa Perfumes Compartilhável 85ml
ref:191
R$ 600,00
kit souvenir floral bouquet
ref:346
R$ 600,00
kit yara 2 und yara candy e yara
ref:385
R$ 550,00
la african drummer lattafa pride
ref:441
R$ 350,00
Página 16 de 31
la vivacitê maison alhambra 100ml
ref:429
R$ 350,00
Lattafa - Afeef 100 ml
ref:21
R$ 700,00
Lattafa - Asad 100 ml
ref:6
R$ 300,00
Lattafa - Asad Bourbon 100ml
ref:3
R$ 330,00
LATTAFA - ASAD ELIXIR 100ml
ref:311
R$ 400,00
Página 17 de 31
Lattafa - Atheeri 100 ml
ref:22
R$ 750,00
Lattafa - Fakhar 100 ml
ref:32
R$ 349,90
Lattafa - Fakhar Extrait Gold 100 ml
ref:24
R$ 349,90
Lattafa - Fakhar Platin 100 ml
ref:23
R$ 400,00
Lattafa - Fakhar Rose 100 ml
ref:30
R$ 350,00
Página 18 de 31
Lattafa - Musamam White 100 ml
ref:34
R$ 550,00
Lattafa - THARWAH GOLD 100 ml
ref:48
R$ 600,00
Lattafa - Yara 100 ml
ref:12
R$ 350,00
Lattafa Asad Zanzibar Limited Edition 100ml
ref:4
R$ 350,00
Lattafa Pride La Collection Dantiquités 1910 Eau de Parfum 100ml
ref:119
R$ 399,90
Página 19 de 31
Legend Intense Emper Eau de Toilette Masculino
ref:267
R$ 290,00
liwan ard zafaran
ref:408
R$ 400,00
mahib adyan by anfar 100ml
ref:348
R$ 300,00
Maison Alhambra - Body perfume Mist 250ml
ref:335
R$ 150,00
Manaal - Ard Al Zaafaran 100 ml
ref:60
R$ 400,00
Página 20 de 31
Marshmallow Blush paris corn
ref:446
R$ 450,00
Mawwal - Basir 100 ml
ref:52
R$ 450,00
mayer lattafa
ref:436
R$ 300,00
Maître de Blue Maison Alhambra Masculino ism Blue de chanel 100ml
ref:195
R$ 300,00
Mia Dolcezza Maison Alhambra
ref:382
R$ 350,00
Página 21 de 31
Milena Ard Al Zaafaran 100ml
ref:328
R$ 450,00
montaigne vanille maison alhambra
ref:414
R$ 300,00
norah lucher adyan
ref:370
R$ 300,00
oleo comcentrado yara lattafa 20ml dv
ref:400
R$ 250,00
oleo concentrado al wataniah 12ml
ref:433
R$ 200,00
Página 22 de 31
olivia maison alhambra
ref:439
R$ 300,00
Orientica Premium - Royal Amber 80ml
ref:19
R$ 750,00
Perfume ARMAF Club de nuit intense man 105 ml
ref:114
R$ 450,00
PERFUME DAR EL WARD ORIENTAL OUD EDP 100ML
ref:249
R$ 290,00
PERFUME LATTAFA QAED AL FURSAN BLACK EAU DE PARFUM 90ML
ref:250
R$ 290,00
Página 23 de 31
Perfume Sahari Blue Sultan EDP - Unisex 100mL
ref:259
R$ 250,00
petra lattafa
ref:440,00
R$ 450,00
Pink Eclipse Maison Alhambra Ref. Olfativa Prada Paradoxe 100ml
ref:199
R$ 450,00
pisa lattafa pride
ref:410
R$ 500,00
Qaed Al Fursan Unlimited Lattafa Perfumes Compartilhável 90ml
ref:285
R$ 350,00
Página 24 de 31
qarar asdaaf 100ml
ref:425
R$ 300,00
Queen Of Arabia Lattafa Perfumes Feminino
ref:243
R$ 700,00
RANEEN ASDAAF 100ml
ref:355 I was asking
R$ 350,00
Reem asdaaf / lattafa eau de parfum 100ml
ref:413
R$ 350,00
rose mystery intense maison alhambra
ref:448
R$ 390,00
Página 25 de 31
safeer al wald ard zafaran
ref:444
R$ 300,00
safeer al ward creme hidratante 450g
ref:445
R$ 330,00
salvo eau de parfum maison alhambra
ref:412
R$ 350,00
Shahd de Lattafa
ref:430
R$ 350,00
shaheen silver lattafa
ref:369
R$ 350,00
Página 26 de 31
shahreen gold lattafa
ref:460
R$ 400,00
Sing Kids 75ml Lattafa Pride
ref:99
R$ 200,00
So Candid rouge Maison Alhambra 100ml
ref:301
R$ 300,00
SPRAY CORPORAL E CABELO LATTAFA HAYA 150ML
ref:306
R$ 200,00
Spray Corporal e cabelo Lattafa Yara 150 Ml
ref:307
R$ 200,00
Página 27 de 31
spray corporal e capilar mayer lattafa 150ml
ref:402
R$ 220,00
Summer Forever Maison Alhambra / Inspirado na fragrância Muse de Xerjoff
ref:329
R$ 300,00
teriaq lattafa 100ml
ref:453
R$ 350,00
Thahaani Al Wataniah Compartilhável 100ml
ref:232
R$ 279,00
tiramisu caramel zimaya 100ml
ref:427
R$ 400,00
Página 28 de 31
uniq armaf effects ok uniq
ref:358
R$ 450,00
Veneno Bianco French Avenue
ref:316
R$ 600,00
Venti Carisma Fragrance World / creed carminda
ref:337
R$ 350,00
venti sublime
ref:432
R$ 350,00
very velvet aqua maison alhambra
ref:373
R$ 300,00
Página 29 de 31
Victorias s Secret - Body Splash 250 ml
ref:40
R$ 180,00
Victorioso Nero Masculino Maison Alhambra Eau de Parfum 100 ml
ref:264
R$ 300,00
vouge night maison alhambra
ref:375
R$ 300,00
vougue rouge maison alhanbra
ref:374
R$ 300,00
Vulcan Feu French Avenue Compartilhável 100ml
ref:233
R$ 600,00
Página 30 de 31
Watani Al Wataniah Feminino 100ml
ref:298
R$ 250,00
winners trophy gold lattafa pride
ref:376
R$ 350,00
yara candy lattafa 100ml
ref:345
R$ 300,00
Yara Elixir Lattafa 100ml Feminino
ref:310
R$ 400,00
Yara Tous Lattafa Perfumes Feminino 100ml
ref:201
R$ 350,00
Página 31 de 31
yeah man partum
ref:409
R$ 350,00
your touch extrait maison alhambra / Stronger With You Intensely armani
ref:321
R$ 250,00
Yum Yum Armaf Feminino 100ml
ref:288
R$ 600,00
Árabe Collection - Spray Corporal 200 ml
ref:39
R$ 60,00`;

const refMap = {};
let currentName = '';
const lines = ocrText.split('\n');
for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();
  if (line.startsWith('Página')) continue;
  
  if (line.startsWith('ref:')) {
    const refRaw = line.split(':')[1].split(',')[0].trim();
    // I was asking -> ignore text after space if any, just grab digits
    const refMatch = refRaw.match(/^(\d+)/);
    if (refMatch) {
      const refId = refMatch[1];
      refMap[refId] = currentName;
    }
  } else if (line.startsWith('R$')) {
    currentName = '';
  } else if (line.length > 0) {
    // If it's a new name block, set currentName. If it spans multiple lines, append.
    if (!currentName) {
      currentName = line;
    } else {
      currentName += ' ' + line;
    }
  }
}

// Ensure the map handles specific IDs correctly (e.g. "perfume-exclusivo-X")
fs.writeFileSync('refMap.json', JSON.stringify(refMap, null, 2));
console.log('Mapped refs: ' + Object.keys(refMap).length);

