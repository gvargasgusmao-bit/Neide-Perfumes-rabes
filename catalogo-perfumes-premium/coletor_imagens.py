import os
import re
import time
import requests
from typing import List, Tuple

# ==========================================
# CONFIGURAÇÕES DA LOJA E INFRAESTRUTURA
# ==========================================
LOJA = {
    "nome":      "RODRIGO IMPORTADOS ÁRABES",
    "email":     "rodrigoimportadosarabes@gmail.com",
    "whatsapp":  "+55 67 99696-2426",
    "instagram": "@rodrigoimportadosarabes",
}

TAMANHO_MINIMO = 2048  # 2KB
DELAY_ENTRE_BUSCAS = 3.5  # Aumentado levemente para maior segurança
PASTA_DESTINO = "catalogo_imagens"

# ─────────────────────────────────────────────────────────────────
# Catálogo completo  (ref, nome exibição, preço R$)
# ─────────────────────────────────────────────────────────────────
PRODUTOS: List[Tuple[str, str, float]] = [
    ("338",  "Venti Silky Princess / Queen of Silk Creed",                 350.00),
    ("26",   "Afnan – Souvenir Desert Rose 100 ml",                        400.00),
    ("428",  "Ajward Pattafa 60 ml",                                       300.00),
    ("438",  "Al Noble Ameer Lattafa",                                     350.00),
    ("262",  "Al Sheikh EDP 100 ml – Sahari Collections",                  250.00),
    ("37",   "Al Ward – Sabah 100 ml",                                     300.00),
    ("27",   "Al Wataniah – Ameerati 100 ml",                              300.00),
    ("28",   "Al Wataniah – Attar Al Wesal 100 ml",                        300.00),
    ("51",   "Al Wataniah – Boraq 75 ml",                                  280.00),
    ("14",   "Al Wataniah – Durrat Al Aroo 85 ml",                         300.00),
    ("115",  "Al Wataniah Al Layl EDP Unissex 100 ml",                     290.00),
    ("85",   "Al Wataniah Ghala EDP Feminino 100 ml",                      300.00),
    ("65",   "Al Wataniah Kenz Al Malik 100 ml",                           290.00),
    ("297",  "Al Wataniah Nawal Fluorite EDP Feminino 100 ml",             250.00),
    ("66",   "Al Wataniah Sultan Al Lail 100 ml",                          240.00),
    ("302",  "Al Wataniah Tiara Pink EDP 100 ml",                          250.00),
    ("203",  "Al Wataniah Tibyan 100 ml",                                  249.90),
    ("454",  "Alpine Maison Alhambra",                                     300.00),
    ("418",  "Amber Divine Passion Cool and Cool 100 ml",                  450.00),
    ("349",  "Amnia Al Wataniah 100 ml",                                   330.00),
    ("53",   "Armaf – Infinity Gold 105 ml",                               600.00),
    ("56",   "Asdaaf – Ameerat Al Arab 100 ml",                            290.00),
    ("58",   "Asdaaf – Andaleeb Flora 100 ml",                             280.00),
    ("198",  "Athena Maison Alhambra 100 ml",                              300.00),
    ("354",  "B.A.D Femme Maison Alhambra 100 ml",                         300.00),
    ("353",  "B.A.D Homme Maison Alhambra 100 ml",                         300.00),
    ("417",  "Bakhoor Royal Ocean Cool and Cool",                          450.00),
    ("207",  "Baroque Rouge 540 Maison Alhambra",                          300.00),
    ("426",  "Bayaan Lattafa 100 ml",                                      350.00),
    ("211",  "Blue Seduction Antonio Banderas 200 ml",                     300.00),
    ("437",  "Bob My Pet – Perfume para Pet",                              150.00),
    ("457",  "Body Cream Delilah Maison Alhambra 110 g",                   210.00),
    ("447",  "Body Cream Delilah Maison Alhambra 110 g 24h",               240.00),
    ("401",  "Body Cream Hidratante Yara 305 ml",                          300.00),
    ("424",  "Body Cream Asad Black",                                      300.00),
    ("299",  "Celeste Maison Alhambra 100 ml",                             350.00),
    ("300",  "Chants Tenderina Maison Alhambra Feminino 100 ml",           300.00),
    ("336",  "Club de Nuit Maleka Armaf",                                  450.00),
    ("242",  "Club de Nuit Woman Armaf Feminino",                          400.00),
    ("268",  "Como Moiselle Maison Alhambra",                              330.00),
    ("141",  "Creme Hidratante Body Cream Yara 200 g",                     190.00),
    ("421",  "Dalal Lattafa",                                              590.00),
    ("435",  "Decantes",                                                   100.00),
    ("196",  "Delilah Blanc Maison Alhambra 100 ml",                       400.00),
    ("169",  "Delilah Pour Femme EDP 100 ml Maison Alhambra",              350.00),
    ("276",  "Durrah Lattafa Perfumes",                                    600.00),
    ("202",  "Eclaire Lattafa Perfumes Feminino 100 ml",                   450.00),
    ("247",  "Eclat De Lune Maison Alhambra",                              300.00),
    ("248",  "El Ward Palais Des Roses EDP Unissex 100 ml",                290.00),
    ("420",  "Emaan Lattafa 100 ml",                                       350.00),
    ("254",  "Emper Al Fares Musk Effect Unissex 100 ml EDP",              250.00),
    ("193",  "Espada Intense Le Chameau 100 ml",                           299.90),
    ("431",  "Extravagant Lover Maison Alhambra",                          350.00),
    ("184",  "Ferrari Black Masculino Eau de Toilette",                    300.00),
    ("356",  "Genius Rose Emper 100 ml",                                   250.00),
    ("415",  "Glacier Pour Homme Maison Alhambra",                         350.00),
    ("333",  "Happy Brush Kids 75 ml Lattafa Pride",                       200.00),
    ("188",  "Her Confession Lattafa Perfumes 100 ml",                     450.00),
    ("282",  "His Confession Lattafa Perfumes",                            450.00),
    ("322",  "Intrude Maison Alhambra 100 ml",                             300.00),
    ("281",  "Ishq Al Shuyukh Silver Lattafa",                             450.00),
    ("416",  "Jardim de Reve Maison Alhambra 100 ml",                      350.00),
    ("456",  "Jazzab Elixir Body Cream",                                   280.00),
    ("327",  "Jorge di Profumo Deep Blue Maison Alhambra",                 250.00),
    ("380",  "Jubilant Vitality Maison Alhambra",                          250.00),
    ("293",  "Khamrah Lattafa Perfumes 100 ml",                            350.00),
    ("191",  "Khanjar Lattafa Perfumes 85 ml",                             600.00),
    ("346",  "Kit Souvenir Floral Bouquet",                                600.00),
    ("385",  "Kit Yara 2 un. (Yara Candy + Yara)",                         550.00),
    ("441",  "La African Drummer Lattafa Pride",                           350.00),
    ("429",  "La Vivacite Maison Alhambra 100 ml",                         350.00),
    ("21",   "Lattafa – Afeef 100 ml",                                     700.00),
    ("6",    "Lattafa – Asad 100 ml",                                      300.00),
    ("3",    "Lattafa – Asad Bourbon 100 ml",                              330.00),
    ("311",  "Lattafa – Asad Elixir 100 ml",                               400.00),
    ("22",   "Lattafa – Atheeri 100 ml",                                   750.00),
    ("32",   "Lattafa – Fakhar 100 ml",                                    349.90),
    ("24",   "Lattafa – Fakhar Extrait Gold 100 ml",                       349.90),
    ("23",   "Lattafa – Fakhar Platin 100 ml",                             400.00),
    ("30",   "Lattafa – Fakhar Rose 100 ml",                               350.00),
    ("34",   "Lattafa – Musamam White 100 ml",                             550.00),
    ("48",   "Lattafa – Tharwah Gold 100 ml",                              600.00),
    ("12",   "Lattafa – Yara 100 ml",                                      350.00),
    ("4",    "Lattafa Asad Zanzibar Limited Edition 100 ml",               350.00),
    ("119",  "Lattafa Pride La Collection d'Antiquites 1910 100 ml",       399.90),
    ("267",  "Legend Intense Emper Eau de Toilette Masculino",             290.00),
    ("408",  "Liwan Ard Al Zafaran",                                       400.00),
    ("348",  "Mahib Adyan by Anfar 100 ml",                                300.00),
    ("335",  "Maison Alhambra Body Perfume Mist 250 ml",                   150.00),
    ("60",   "Manaal – Ard Al Zaafaran 100 ml",                            400.00),
    ("446",  "Marshmallow Blush Paris Corner",                             450.00),
    ("52",   "Mawwal – Basir 100 ml",                                      450.00),
    ("436",  "Mayar Lattafa",                                              300.00),
    ("195",  "Maitre de Blue Maison Alhambra Masculino 100 ml",            300.00),
    ("382",  "Mia Dolcezza Maison Alhambra",                               350.00),
    ("328",  "Milena Ard Al Zaafaran 100 ml",                              450.00),
    ("414",  "Montaigne Vanille Maison Alhambra",                          300.00),
    ("370",  "Norah Lucher Adyan",                                         300.00),
    ("400",  "Oleo Concentrado Yara Lattafa 20 ml",                        250.00),
    ("433",  "Oleo Concentrado Al Wataniah 12 ml",                         200.00),
    ("439",  "Olivia Maison Alhambra",                                     300.00),
    ("19",   "Orientica Premium Royal Amber 80 ml",                        750.00),
    ("114",  "Armaf Club de Nuit Intense Man 105 ml",                      450.00),
    ("249",  "Dar El Ward Oriental Oud EDP 100 ml",                        290.00),
    ("250",  "Lattafa Qaed Al Fursan Black EDP 90 ml",                     290.00),
    ("259",  "Sahari Blue Sultan EDP Unisex 100 ml",                       250.00),
    ("440",  "Petra Lattafa",                                              450.00),
    ("199",  "Pink Eclipse Maison Alhambra 100 ml",                        400.00),
    ("410",  "Pisa Lattafa Pride",                                         500.00),
    ("285",  "Qaed Al Fursan Unlimited Lattafa 90 ml",                     350.00),
    ("425",  "Qarar Asdaaf 100 ml",                                        300.00),
    ("243",  "Queen of Arabia Lattafa Perfumes Feminino",                  700.00),
    ("355",  "Raneen Asdaaf 100 ml",                                       350.00),
    ("413",  "Reem Asdaaf / Lattafa EDP 100 ml",                           350.00),
    ("448",  "Rose Mystery Intense Maison Alhambra",                       390.00),
    ("444",  "Safeer Al Ward Ard Al Zafaran",                              300.00),
    ("445",  "Safeer Al Ward Creme Hidratante 450 g",                      330.00),
    ("412",  "Salvo EDP Maison Alhambra",                                  350.00),
    ("430",  "Shahd de Lattafa",                                           350.00),
    ("369",  "Shaheen Silver Lattafa",                                     350.00),
    ("99",   "Sing Kids 75 ml Lattafa Pride",                              200.00),
    ("301",  "So Candid Rouge Maison Alhambra 100 ml",                     300.00),
    ("306",  "Spray Corporal e Cabelo Lattafa Haya 150 ml",                200.00),
    ("307",  "Spray Corporal e Cabelo Lattafa Yara 150 ml",                200.00),
    ("402",  "Spray Corporal e Capilar Mayar Lattafa 150 ml",              220.00),
    ("329",  "Summer Forever Maison Alhambra",                             300.00),
    ("453",  "Teriaq Lattafa 100 ml",                                      350.00),
    ("232",  "Thahaani Al Wataniah 100 ml",                                279.00),
    ("427",  "Tiramisu Caramel Zimaya 100 ml",                             400.00),
    ("358",  "Uniq Armaf Effects",                                         450.00),
    ("316",  "Veneno Bianco French Avenue",                                600.00),
    ("337",  "Venti Carisma Fragrance World",                              350.00),
    ("432",  "Venti Sublime",                                              350.00),
    ("373",  "Very Velvet Aqua Maison Alhambra",                           300.00),
    ("40",   "Victoria's Secret Body Splash 250 ml",                       180.00),
    ("264",  "Victorioso Nero Maison Alhambra EDP 100 ml",                 300.00),
    ("375",  "Vogue Night Maison Alhambra",                                300.00),
    ("374",  "Vogue Rouge Maison Alhambra",                                300.00),
    ("233",  "Vulcan Feu French Avenue 100 ml",                            600.00),
    ("298",  "Watani Al Wataniah Feminino 100 ml",                         250.00),
    ("376",  "Winners Trophy Gold Lattafa Pride",                          350.00),
    ("345",  "Yara Candy Lattafa 100 ml",                                  300.00),
    ("310",  "Yara Elixir Lattafa Feminino 100 ml",                        400.00),
    ("201",  "Yara Tous Lattafa Perfumes Feminino 100 ml",                 350.00),
    ("409",  "Yeah Man Parfum",                                            350.00),
    ("321",  "Your Touch Extrait Maison Alhambra",                         250.00),
    ("288",  "Yum Yum Armaf Feminino 100 ml",                              600.00),
    ("39",   "Arabe Collection Spray Corporal 200 ml",                      60.00),
]


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
    "Referer": "https://br.images.search.yahoo.com/",
    "Upgrade-Insecure-Requests": "1"
}

session = requests.Session()
session.headers.update(HEADERS)

# ==========================================

def baixar_imagem(url, nome_arquivo):
    """Tenta baixar a imagem e verifica o tamanho mínimo estipulado."""
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=5)
        if resposta.status_code == 200:
            if len(resposta.content) >= TAMANHO_MINIMO:
                caminho_completo = os.path.join(PASTA_DESTINO, f"{nome_arquivo}.jpg")
                with open(caminho_completo, 'wb') as f:
                    f.write(resposta.content)
                return True
            else:
                print(f"    [!] Imagem ignorada: Menor que {TAMANHO_MINIMO} bytes.")
    except Exception as e:
        print(f"    [x] Erro ao baixar {url}: {e}")
    return False

def buscar_fallback_yahoo(produto):
    """Rota de contingência utilizando o Yahoo (Bing via Yahoo) com Regex corrigido."""
    print(f"    [*] Iniciando fallback no Yahoo para: {produto}")
    query = requests.utils.quote(produto)
    url_busca = f"https://br.images.search.yahoo.com/search/images?p={query}"
    
    try:
        resp = session.get(url_busca, timeout=10)
        if resp.status_code != 200:
            print(f"    [!] Erro HTTP {resp.status_code}. Snippet: {resp.text[:150].strip()}...")
            return []

        # Regex corrigido para capturar links do CDN do Bing no HTML do Yahoo
        links = re.findall(r"https://tse\d\.mm\.bing\.net/th\?id=[^\"\'& ]+", resp.text)
        
        links_unicos = list(dict.fromkeys(links))
        return links_unicos[:3]
    except Exception as e:
        print(f"    [x] Falha na busca pelo Yahoo: {e}")
        return []

def buscar_imagens(nome_produto):
    """Gerencia a busca e o download da imagem de um produto."""
    print(f"\n[-] Processando: {nome_produto}")
    
    nome_arquivo = re.sub(r'[^a-z0-9]', '_', nome_produto.lower()).strip('_')
    nome_arquivo = re.sub(r'_{2,}', '_', nome_arquivo) # Remove underscores duplicados
    
    links_encontrados = buscar_fallback_yahoo(nome_produto)
    
    if not links_encontrados:
        print("    [!] Nenhuma imagem encontrada nas buscas.")
        return
        
    sucesso = False
    for link in links_encontrados:
        print(f"    [*] Tentando baixar: {link}")
        if baixar_imagem(link, nome_arquivo):
            print(f"    [+] Sucesso! Imagem salva como {nome_arquivo}.jpg")
            sucesso = True
            break  # Interrompe após baixar a primeira imagem válida com sucesso
            
    if not sucesso:
        print("    [!] Não foi possível baixar uma imagem válida para este produto.")

# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print(f"Iniciando raspagem de catálogo para: {LOJA['nome']}")
    print("-" * 50)
    
    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)
        print(f"Pasta '{PASTA_DESTINO}' criada com sucesso.")
        
    for ref, nome, preco in PRODUTOS:
        buscar_imagens(nome)
        print(f"Aguardando {DELAY_ENTRE_BUSCAS} segundos...")
        time.sleep(DELAY_ENTRE_BUSCAS)
        
    print("-" * 50)
    print("Operação concluída. Verifique a pasta destino.")