const fs = require('fs');
const path = require('path');

// Caminhos dos ficheiros
const pythonFilePath = path.join(__dirname, 'catalogo_perfumes.py');
const dbFilePath = path.join(__dirname, 'src', 'data', 'db.json');

console.log('⏳ A iniciar a migração de dados de Alta Perfumaria...');

try {
    // 1. Ler o ficheiro Python
    const pythonCode = fs.readFileSync(pythonFilePath, 'utf8');

    // 2. Extrair os produtos com Expressões Regulares (RegEx)
    const regex = /\(\s*"(\d+)"\s*,\s*"(.*?)"\s*,\s*([\d.]+)\s*\)/g;
    let match;
    const perfumesExtraidos = [];

    while ((match = regex.exec(pythonCode)) !== null) {
        perfumesExtraidos.push({
            id: parseInt(match[1]),
            nomeBruto: match[2],
            preco: parseFloat(match[3])
        });
    }

    console.log(`✓ Foram encontrados ${perfumesExtraidos.length} produtos no ficheiro Python.`);

    // 3. Estruturar as Marcas Premium (Dedução automática baseada no nome)
    const marcasBase = [
        { id_marca: 1, nome: "Amouage", pais_origem: "Omã" },
        { id_marca: 2, nome: "Roja Parfums", pais_origem: "Inglaterra" },
        { id_marca: 3, nome: "Lattafa", pais_origem: "EAU" },
        { id_marca: 4, nome: "Maison Alhambra", pais_origem: "EAU" },
        { id_marca: 5, nome: "Al Wataniah", pais_origem: "EAU" },
        { id_marca: 6, nome: "Armaf", pais_origem: "EAU" },
        { id_marca: 7, nome: "Asdaaf", pais_origem: "EAU" },
        { id_marca: 8, nome: "Exclusivo Maison Núr", pais_origem: "Vários" } // Fallback
    ];

    // 4. Transformar os dados para o padrão db.json
    const perfumesPremium = perfumesExtraidos.map(p => {
        // Gerador de Slug amigável para SEO
        const slug = p.nomeBruto.toLowerCase()
            .normalize("NFD").replace(/[\u0300-\u036f]/g, "") // Remove acentos
            .replace(/[^a-z0-9]+/g, '-') // Substitui espaços e símbolos por hifens
            .replace(/(^-|-$)+/g, ''); // Remove hifens nas pontas

        // Deduzir a marca
        let idMarca = 8; // Default
        const nomeUpper = p.nomeBruto.toUpperCase();
        if (nomeUpper.includes('LATTAFA')) idMarca = 3;
        else if (nomeUpper.includes('ALHAMBRA')) idMarca = 4;
        else if (nomeUpper.includes('WATANIAH')) idMarca = 5;
        else if (nomeUpper.includes('ARMAF')) idMarca = 6;
        else if (nomeUpper.includes('ASDAAF')) idMarca = 7;

        return {
            id_perfume: p.id,
            slug: slug,
            nome: p.nomeBruto,
            id_marca: idMarca,
            id_familia: 1, // Definido como 1 por defeito. Pode ser refinado depois.
            volume_ml: 100, // Volume genérico inicial
            preco: p.preco,
            preco_sob_consulta: false,
            status_estoque: "disponivel",
            seo_title: `${p.nomeBruto} | Maison Núr`,
            seo_description: `Descubra a sofisticação de ${p.nomeBruto}. Notas exclusivas na Maison Núr.`,
            descricao_curta: "Uma assinatura olfativa de luxo e sofisticação.",
            descricao_longa: "Fragrância meticulosamente elaborada, perfeita para quem exige exclusividade e presença marcante.",
            piramide_olfativa: {
                topo: ["Notas de topo a definir"],
                coracao: ["Notas de coração a definir"],
                fundo: ["Notas de fundo a definir"]
            },
            imagem_url: `/assets/images/perfumes/ref_${p.id}.jpg`,
            destaque: false // Para não encher a Home, colocaremos em destaque só alguns futuramente
        };
    });

    // Destacar os primeiros 4 para a Home não ficar vazia
    for(let i=0; i<4 && i<perfumesPremium.length; i++){
        perfumesPremium[i].destaque = true;
    }

    // 5. Estruturar e Guardar o JSON Final
    const dbFinal = {
        configuracoes: {
            nome_marca: "Maison Núr",
            whatsapp_contato: "5567996962426", // Extraído do seu ficheiro Python
            mensagem_padrao: "Olá, Maison Núr. Desejo uma consultoria exclusiva sobre a fragrância "
        },
        marcas: marcasBase,
        familias_olfativas: [
            { id_familia: 1, nome: "Oriental Premium" },
            { id_familia: 2, nome: "Amadeirado Especiado" }
        ],
        perfumes: perfumesPremium
    };

    fs.writeFileSync(dbFilePath, JSON.stringify(dbFinal, null, 2), 'utf8');
    console.log('✓ Base de dados db.json reescrita com sucesso!');
    console.log('✨ Migração concluída. A arquitetura de dados está pronta para escalar.');

} catch (error) {
    console.error('✗ Erro na migração:', error.message);
}