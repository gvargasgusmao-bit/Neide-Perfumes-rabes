"""
=============================================================================
  NEIDE PERFUMES ÁRABES — Catálogo Premium
  app.py — Single-file Flask Application
  Version : 1.2.0  (dotenv, campo descrição, caminhos unificados)
=============================================================================
"""

import os
import re
import sqlite3
import secrets
import datetime
import urllib.parse
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template_string,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
    g,
)

load_dotenv()  # Carrega .env antes de qualquer leitura de os.environ

# ---------------------------------------------------------------------------
# APP & CONFIGURAÇÃO
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder="static")

_secret_key = os.environ.get("SECRET_KEY")
if not _secret_key:
    raise RuntimeError(
        "\n[ERRO] SECRET_KEY não definida!\n"
        "Crie ou edite o arquivo .env na raiz do projeto e adicione:\n"
        "  SECRET_KEY=<uma string longa e aleatória>\n"
    )
app.secret_key = _secret_key

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
if not ADMIN_PASSWORD:
    raise RuntimeError(
        "\n[ERRO] ADMIN_PASSWORD não definida!\n"
        "Crie ou edite o arquivo .env na raiz do projeto e adicione:\n"
        "  ADMIN_PASSWORD=<sua senha segura>\n"
    )

ADMIN_ROUTE = "/painel-secreto-rodrigo-2026"
WHATSAPP_NUMBER = "5567984281754"

DB_PATH = Path(__file__).parent / "database.db"
UPLOAD_FOLDER = Path(__file__).parent / "static" / "images"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# ---------------------------------------------------------------------------
# DATASET — 145 PRODUTOS
# ---------------------------------------------------------------------------
PRODUCTS_SEED = [
    ("338", "Venti Silky Princess Fragrance World / Queen of Silk Creed", 350.00),
    ("26", "Afnan - Souvenir Desert Rose 100 ml", 400.00),
    ("428", "ajward pattafa 60ml", 300.00),
    ("438", "al nobre almeer lattafa", 350.00),
    ("262", "Al Sheikh EDP 100 ml da Sahari Collections", 250.00),
    ("37", "Al Ward - Sabah 100 ml", 300.00),
    ("27", "Al Wataniah - Ameerati 100 ml", 300.00),
    ("28", "Al Wataniah - Attar Al Wesal 100 ml", 300.00),
    ("51", "Al Wataniah - Boraq 75 ml", 280.00),
    ("14", "Al Wataniah - Durrat Al Aroo 85 ml", 300.00),
    ("115", "Al Wataniah Al Layl EDP Unissex 100 ml", 290.00),
    ("85", "Al Wataniah Ghala EDP Feminino 100 ml", 300.00),
    ("65", "Al Wataniah Kenz Al Malik 100 ml", 290.00),
    ("297", "Al Wataniah Nawal Fluorite EDP Feminino 100 ml", 250.00),
    ("66", "Al Wataniah Sultan Al Lail 100 ml", 240.00),
    ("302", "Al Wataniah Tiara Pink EDP 100 ml", 250.00),
    ("203", "Al Wataniah Tibyan 100 ml", 249.90),
    ("454", "Alpine Maison Alhambra", 300.00),
    ("418", "Amber Divine Passion Cool and Cool 100ml", 450.00),
    ("349", "Amnia Al Wataniah 100 ml", 330.00),
    ("53", "Armaf - Infinity Gold 105 ml", 600.00),
    ("56", "Asdaaf - Ameerat Al Arab 100 ml", 290.00),
    ("58", "Asdaaf - Andaleeb Flora 100 ml", 280.00),
    ("198", "Athena Maison Alhambra 100ml", 300.00),
    ("354", "B.A.D Femme Maison Alhambra 100ml", 300.00),
    ("353", "B.A.D Homme Maison Alhambra 100ml", 300.00),
    ("417", "Bakhoor Royal Ocean Cool and Cool", 450.00),
    ("207", "Baroque Rouge 540 Maison Alhambra", 300.00),
    ("426", "Bayaan lattafa 100ml", 350.00),
    ("211", "Blue Seduction Antonio Banderas 200 ml", 300.00),
    ("437", "Bob My Pet - Perfume para Pet", 150.00),
    ("457", "Body Cream Delilah Maison Alhambra 110g", 210.00),
    ("447", "Body Cream Delilah Maison Alhambra 110g 24h", 240.00),
    ("401", "Body Cream Hidratante Yara 305ml", 300.00),
    ("424", "Body Cream Asad Black", 300.00),
    ("299", "Celeste Maison Alhambra 100ml", 350.00),
    ("300", "Chants Tenderina Maison Alhambra Feminino 100ml", 300.00),
    ("336", "Club de Nuit Maleka Armaf", 450.00),
    ("242", "Club de Nuit Woman Armaf Feminino", 400.00),
    ("268", "Como Moiselle Maison Alhambra", 330.00),
    ("141", "Creme Hidratante Body Cream Yara 200g", 190.00),
    ("421", "Dalal Lattafa", 590.00),
    ("435", "Decantes", 100.00),
    ("196", "Delilah Blanc Maison Alhambra 100ml", 400.00),
    ("169", "Delilah Pour Femme EDP 100ml Maison Alhambra", 350.00),
    ("276", "Durrah Lattafa Perfumes", 600.00),
    ("202", "Eclaire Lattafa Perfumes Feminino 100ml", 450.00),
    ("247", "Eclat De Lune Maison Alhambra", 300.00),
    ("248", "El Ward Palais Des Roses EDP Unissex 100ml", 290.00),
    ("420", "Emaan Lattafa 100ml", 350.00),
    ("254", "Emper Al Fares Musk Effect Unissex 100ml EDP", 250.00),
    ("193", "Espada Intense Le Chameau 100 ml", 299.90),
    ("431", "Extravagant Lover Maison Alhambra", 350.00),
    ("184", "Ferrari Black Masculino Eau de Toilette", 300.00),
    ("356", "Genius Rose Emper 100ml", 250.00),
    ("415", "Glacier Pour Homme Maison Alhambra", 350.00),
    ("333", "Happy Brush Kids 75ml lattafa pride", 200.00),
    ("188", "Her Confession Lattafa Perfumes 100ml", 450.00),
    ("282", "His Confession Lattafa Perfumes", 450.00),
    ("322", "Intrude Maison Alhambra 100ml", 300.00),
    ("281", "Ishq Al Shuyukh Silver Lattafa", 450.00),
    ("416", "Jardim de Reve Maison Alhambra 100ml", 350.00),
    ("456", "Jazzab Elixir body cream", 280.00),
    ("327", "Jorge di Profumo Deep Blue Maison Alhambra", 250.00),
    ("380", "Jubilant Vitality Maison Alhambra", 250.00),
    ("293", "Khamrah Lattafa Perfumes 100ml", 350.00),
    ("191", "Khanjar Lattafa Perfumes 85 ml", 600.00),
    ("346", "Kit Souvenir Floral Bouquet", 600.00),
    ("385", "Kit Yara 2un (Yara Candy + Yara)", 550.00),
    ("441", "La African Drummer Lattafa pride", 350.00),
    ("429", "La Vivacite Maison Alhambra 100ml", 350.00),
    ("21", "Lattafa - Afeef 100 ml", 700.00),
    ("6", "Lattafa - Asad 100 ml", 300.00),
    ("3", "Lattafa - Asad Bourbon 100 ml", 330.00),
    ("311", "Lattafa - Asad Elixir 100 ml", 400.00),
    ("22", "Lattafa - Atheeri 100 ml", 750.00),
    ("32", "Lattafa - Fakhar 100 ml", 349.90),
    ("24", "Lattafa - Fakhar Extrait Gold 100 ml", 349.90),
    ("23", "Lattafa - Fakhar Platin 100 ml", 400.00),
    ("30", "Lattafa - Fakhar Rose 100 ml", 350.00),
    ("34", "Lattafa - Musamam White 100 ml", 550.00),
    ("48", "Lattafa - Tharwah Gold 100 ml", 600.00),
    ("12", "Lattafa - Yara 100 ml", 350.00),
    ("4", "Lattafa Asad Zanzibar Limited Edition 100ml", 350.00),
    ("119", "Lattafa Pride La Collection d Antiquites 1910 100 ml", 399.90),
    ("267", "Legend Intense Emper Eau de Toilette Masculino", 290.00),
    ("408", "Liwan ard al zafaran", 400.00),
    ("348", "Mahib Adyan by anfar 100ml", 300.00),
    ("335", "Maison Alhambra Body Perfume Mist 250ml", 150.00),
    ("60", "Manaal - Ard Al Zaafaran 100 ml", 400.00),
    ("446", "Marshmallow Blush Paris Corner", 450.00),
    ("52", "Mawwal - Basir 100 ml", 450.00),
    ("436", "Mayar Lattafa", 300.00),
    ("195", "Maitre de Blue Maison Alhambra Masculino 100ml", 300.00),
    ("382", "Mia Dolcezza Maison Alhambra", 350.00),
    ("328", "Milena Ard Al Zaafaran 100 ml", 450.00),
    ("414", "Montaigne Vanille Maison Alhambra", 300.00),
    ("370", "norah lucher adyan", 300.00),
    ("400", "Oleo Concentrado Yara Lattafa 20ml", 250.00),
    ("433", "Oleo Concentrado Al Wataniah 12ml", 200.00),
    ("439", "Olivia Maison Alhambra", 300.00),
    ("19", "Orientica Premium Royal Amber 80 ml", 750.00),
    ("114", "Armaf Club de Nuit Intense Man 105 ml", 450.00),
    ("249", "Dar El Ward Oriental Oud EDP 100 ml", 290.00),
    ("250", "Lattafa Qaed Al Fursan Black EDP 90 ml", 290.00),
    ("259", "Sahari Blue Sultan EDP Unisex 100 ml", 250.00),
    ("440", "Petra Lattafa", 450.00),
    ("199", "Pink Eclipse Maison Alhambra 100ml", 400.00),
    ("410", "Pisa lattafa pride", 500.00),
    ("285", "Qaed Al Fursan Unlimited Lattafa 90ml", 350.00),
    ("425", "Qarar Asdaaf 100ml", 300.00),
    ("243", "Queen of Arabia Lattafa Perfumes Feminino", 700.00),
    ("355", "Raneen Asdaaf 100ml", 350.00),
    ("413", "Reem Asdaaf / lattafa EDP 100ml", 350.00),
    ("448", "Rose Mystery Intense Maison Alhambra", 390.00),
    ("444", "Safeer Al Ward Ard Al Zafaran", 300.00),
    ("445", "Safeer Al Ward Creme Hidratante 450g", 330.00),
    ("412", "Salvo EDP Maison Alhambra", 350.00),
    ("430", "Shahd de Lattafa", 350.00),
    ("369", "Shaheen Silver Lattafa", 350.00),
    ("99", "Sing Kids 75ml lattafa pride", 200.00),
    ("301", "So Candid Rouge Maison Alhambra 100ml", 300.00),
    ("306", "Spray Corporal e Cabelo Lattafa Haya 150ml", 200.00),
    ("307", "Spray Corporal e Cabelo Lattafa Yara 150ml", 200.00),
    ("402", "Spray Corporal e Capilar Mayar Lattafa 150ml", 220.00),
    ("329", "Summer Forever Maison Alhambra", 300.00),
    ("453", "Teriaq Lattafa 100ml", 350.00),
    ("232", "Thahaani Al Wataniah 100 ml", 279.00),
    ("427", "Tiramisu Caramel Zimaya 100ml", 400.00),
    ("358", "uniq armaf effects ok", 450.00),
    ("316", "Veneno Bianco French Avenue", 600.00),
    ("337", "Venti Carisma Fragrance World / creed carminda", 350.00),
    ("432", "venti sublime", 350.00),
    ("373", "very velvet aqua maison alhambra", 300.00),
    ("40", "Victorias s Secret - Body Splash 250 ml", 180.00),
    ("264", "Victorioso Nero Masculino Maison Alhambra Eau de Parfum 100 ml", 300.00),
    ("375", "vouge night maison alhambra", 300.00),
    ("374", "vougue rouge maison alhanbra", 300.00),
    ("233", "Vulcan Feu French Avenue Compartilhável 100ml", 600.00),
    ("298", "Watani Al Wataniah Feminino 100ml", 250.00),
    ("376", "Winners Trophy Gold Lattafa Pride", 350.00),
    ("345", "Yara Candy Lattafa 100ml", 300.00),
    ("310", "Yara Elixir Lattafa Feminino 100ml", 400.00),
    ("201", "Yara Tous Lattafa Perfumes Feminino 100ml", 350.00),
    ("409", "yeah man parfum", 350.00),
    ("321", "Your Touch Extrait Maison Alhambra", 250.00),
    ("288", "Yum Yum Armaf Feminino 100ml", 600.00),
    ("39", "Arabe Collection Spray Corporal 200ml", 60.00),
]

# ---------------------------------------------------------------------------
# EXTRAÇÃO INTELIGENTE DE MARCA E GÊNERO
# ---------------------------------------------------------------------------
BRAND_KEYWORDS = [
    ("Maison Alhambra", ["maison alhambra", "alhambra"]),
    ("Lattafa Pride", ["lattafa pride"]),
    ("Lattafa", ["lattafa"]),
    ("Al Wataniah", ["al wataniah"]),
    ("Asdaaf", ["asdaaf"]),
    ("Armaf", ["armaf"]),
    ("Afnan", ["afnan"]),
    ("Orientica", ["orientica"]),
    ("Emper", ["emper"]),
    ("Ard Al Zaafaran", ["ard al zaafaran", "ard al zafaran"]),
    ("Cool and Cool", ["cool and cool"]),
    ("Paris Corner", ["paris corner"]),
    ("Fragrance World", ["fragrance world"]),
    ("French Avenue", ["french avenue"]),
    ("Zimaya", ["zimaya"]),
    ("Le Chameau", ["le chameau"]),
    ("Ferrari", ["ferrari"]),
    ("Antonio Banderas", ["antonio banderas"]),
    ("Mawwal", ["mawwal"]),
    ("Al Ward", ["al ward"]),
    ("Sahari", ["sahari"]),
    ("Adyan", ["adyan", "anfar"]),
    ("Pattafa", ["pattafa"]),
    ("Victorias Secret", ["victorias s secret", "victoria"]),
]

GENDER_KEYWORDS = {
    "Feminino": [
        "feminino",
        "femme",
        "woman",
        "women",
        "girl",
        "rose",
        "pink",
        "floral",
        "princess",
        "queen",
        "ameerati",
        "her",
        "yara",
        "delilah",
        "milena",
        "marshmallow",
        "candy",
        "tenderina",
        "blush",
        "celeste",
        "nawal",
        "tiara",
        "ghala",
        "watani",
        "eclaire",
        "raneen",
        "reem",
        "dalal",
        "emaan",
        "olivia",
        "norah",
        "mia dolcezza",
        "yum yum",
        "veneno bianco",
        "fakhar rose",
        "durrat al aroo",
        "como moiselle",
        "eclat de lune",
        "la vivacite",
        "extravagant lover",
        "jardim de reve",
        "b.a.d femme",
        "pink eclipse",
        "athena",
        "summer forever",
        "rose mystery",
        "chants tenderina",
        "your touch",
        "so candid rouge",
        "safeer al ward",
        "kit yara",
    ],
    "Masculino": [
        "masculino",
        "homme",
        "man",
        "men",
        "boy",
        "noir",
        "black",
        "intense",
        "glacier",
        "asad",
        "khanjar",
        "sultan",
        "sheikh",
        "fakhar",
        "ishq",
        "qaed",
        "fursan",
        "his confession",
        "shaheen",
        "winners",
        "vulcan",
        "espada",
        "legend intense",
        "ferrari",
        "pisa",
        "glacier pour homme",
        "intrude",
        "yeah man",
        "victorioso nero",
        "jorge di profumo",
        "maitre de blue",
        "b.a.d homme",
        "kenz al malik",
        "boraq",
        "club de nuit intense man",
        "armaf infinity",
    ],
    "Unissex": [
        "unissex",
        "unisex",
        "oud",
        "amber",
        "musk",
        "attar",
        "al layl",
        "khamrah",
        "bakhoor",
        "el ward palais",
        "al fares musk",
        "orientica",
        "mawwal",
        "manaal",
        "baroque rouge",
        "amnia",
        "liwan",
        "dar el ward",
        "sahari blue",
        "thahaani",
        "mahib",
        "blue seduction",
        "decantes",
        "venti",
        "kit souvenir",
        "teriaq",
        "petra",
        "shahd",
        "bayaan",
        "qarar",
    ],
}


def extract_brand(name: str) -> str:
    """Detecta a marca do produto com base em palavras-chave no nome."""
    nl = name.lower()
    for label, kws in BRAND_KEYWORDS:
        for kw in kws:
            if kw in nl:
                return label
    return "Outros"


def extract_gender(name: str) -> str:
    """Determina o gênero do produto por pontuação de palavras-chave no nome."""
    nl = name.lower()
    scores = {g: 0 for g in GENDER_KEYWORDS}
    for gender, kws in GENDER_KEYWORDS.items():
        for kw in kws:
            if kw in nl:
                scores[gender] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Unissex"


# ---------------------------------------------------------------------------
# BANCO DE DADOS
# ---------------------------------------------------------------------------
def get_db():
    """Retorna (ou abre) a conexão SQLite para o contexto de request atual."""
    if "db" not in g:
        g.db = sqlite3.connect(str(DB_PATH))
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL;")
    return g.db


@app.teardown_appcontext
def close_db(_exc=None):  # _exc: contexto de erro Flask, ignorado intencionalmente
    """Fecha a conexão com o banco ao fim de cada request."""
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():  # noqa: C901
    """Cria as tabelas e aplica migrações seguras no banco de dados."""
    with sqlite3.connect(str(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                reference    TEXT    UNIQUE NOT NULL,
                name         TEXT    NOT NULL,
                price        REAL    NOT NULL,
                image_path   TEXT    NULL,
                brand        TEXT    NOT NULL DEFAULT '',
                gender       TEXT    NOT NULL DEFAULT 'Unissex',
                is_available INTEGER NOT NULL DEFAULT 1,
                description  TEXT    NOT NULL DEFAULT ''
            )
        """)
        # Migração segura: adiciona a coluna se o banco já existia sem ela
        try:
            conn.execute(
                "ALTER TABLE products ADD COLUMN description TEXT NOT NULL DEFAULT ''"
            )
            conn.commit()
            print("[DB] Coluna 'description' adicionada com sucesso.")
        except sqlite3.OperationalError:
            pass  # Coluna já existe — normal
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            rows = []
            for ref, name, price in PRODUCTS_SEED:
                rows.append(
                    (
                        ref,
                        name,
                        price,
                        None,
                        extract_brand(name),
                        extract_gender(name),
                        1,
                        "",
                    )
                )
            insert_sql = (
                "INSERT OR IGNORE INTO products "
                "(reference,name,price,image_path,brand,gender,is_available,description) "
                "VALUES (?,?,?,?,?,?,?,?)"
            )
            conn.executemany(insert_sql, rows)
            conn.commit()
            print(f"[DB] {len(rows)} produtos inseridos.")
        else:
            print(f"[DB] Banco já contém {count} produtos.")


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------
def login_required(f):
    """Decorator que exige login ativo na sessão para acessar a rota."""

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)

    return decorated


# ---------------------------------------------------------------------------
# UTILITÁRIOS DE UPLOAD
# ---------------------------------------------------------------------------
def allowed_file(filename: str) -> bool:
    """Retorna True se a extensão do arquivo está na lista de permitidos."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def safe_image_path(reference: str) -> str:
    """Constrói o caminho seguro (sem path traversal) para a imagem do produto."""
    clean = re.sub(r"[^a-zA-Z0-9_\-]", "_", reference)
    return str(UPLOAD_FOLDER / f"ref_{clean}.jpg")


def image_url(image_path):
    """Converte o caminho absoluto da imagem em URL relativa ao Flask static."""
    if not image_path:
        return None
    p = Path(image_path)
    if p.exists():
        return url_for("static", filename=f"images/{p.name}")
    return None


# ---------------------------------------------------------------------------
# CSS COMPARTILHADO (injetado em cada template)
# ---------------------------------------------------------------------------
SHARED_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  theme: {
    extend: {
      colors: {
        forest:   { DEFAULT:'#1C3A2F', light:'#2A5240', dark:'#122419' },
        gold:     { DEFAULT:'#C9A84C', light:'#E2C47E', dark:'#9E7A28' },
        cream:    { DEFAULT:'#FAF7F2', dark:'#F0EBE1' },
        charcoal: { DEFAULT:'#2C2C2C' },
      },
      fontFamily: {
        serif: ['Cormorant Garamond','Georgia','serif'],
        sans:  ['Inter','system-ui','sans-serif'],
      },
    }
  }
}
</script>
<style>
  ::-webkit-scrollbar{width:6px}
  ::-webkit-scrollbar-track{background:#FAF7F2}
  ::-webkit-scrollbar-thumb{background:#C9A84C;border-radius:3px}

  .card-hover{transition:transform .3s ease,box-shadow .3s ease}
  .card-hover:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(201,168,76,.18)}

  .alink::after{content:'';display:block;width:0;height:1px;background:#C9A84C;transition:width .3s ease}
  .alink:hover::after{width:100%}

  @keyframes fadeInUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
  .fi{animation:fadeInUp .6s ease both}
  .fi1{animation-delay:.1s}.fi2{animation-delay:.2s}.fi3{animation-delay:.3s}

  .ornament{display:flex;align-items:center;gap:1rem}
  .ornament::before,.ornament::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,transparent,#C9A84C,transparent)}

  @keyframes badgePulse{0%,100%{opacity:1}50%{opacity:.7}}
  .pulse{animation:badgePulse 2s infinite}

  .hero-bg{background:linear-gradient(135deg,#122419 0%,#1C3A2F 50%,#2A5240 100%)}

  .filter-bar{
    backdrop-filter:blur(12px);
    background:rgba(250,247,242,.95);
    border-bottom:1px solid rgba(201,168,76,.2);
  }
  .product-card.hidden{display:none!important}
</style>
"""

SHARED_FOOTER = """
<footer class="bg-[#122419] text-[#FAF7F2] py-12 mt-20">
  <div class="max-w-6xl mx-auto px-4 text-center">
    <p class="font-serif text-2xl text-[#C9A84C] mb-2">NEIDE PERFUMES ÁRABES</p>
    <p class="text-[#FAF7F2]/60 text-sm mb-4">Fragrâncias Exclusivas &bull; Importados Diretamente</p>
    <div class="ornament mb-6"><span class="text-[#C9A84C] text-lg">✦</span></div>
    <p class="text-[#FAF7F2]/50 text-xs">
      &copy; {{ year }} NEIDE PERFUMES ÁRABES &middot; Todos os direitos reservados.<br>
      Campo Grande &ndash; MS &middot; WhatsApp:
      <a href="https://wa.me/5567984281754" class="text-[#C9A84C] hover:text-[#E2C47E] transition-colors">(67) 98428-1754</a>
    </p>
  </div>
</footer>
"""

# ===========================================================================
# TEMPLATE — CATÁLOGO PÚBLICO
# ===========================================================================
CATALOG_TEMPLATE = (
    """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Catálogo | NEIDE PERFUMES ÁRABES</title>
  <meta name="description" content="Descubra nossa coleção de {{ total }} perfumes importados árabes premium.">
  """
    + SHARED_CSS
    + """
</head>
<body class="bg-[#FAF7F2] font-sans text-[#2C2C2C] antialiased min-h-screen">

<!-- HERO -->
<header class="hero-bg text-white relative overflow-hidden">
  <div class="absolute top-0 right-0 w-96 h-96 rounded-full opacity-5"
       style="background:radial-gradient(circle,#C9A84C,transparent);transform:translate(30%,-30%)"></div>
  <div class="absolute bottom-0 left-0 w-64 h-64 rounded-full opacity-5"
       style="background:radial-gradient(circle,#C9A84C,transparent);transform:translate(-30%,30%)"></div>

  <div class="max-w-6xl mx-auto px-4 py-16 text-center relative z-10">
    <div class="flex items-center justify-center gap-3 mb-6 fi">
      <div class="w-12 h-px bg-[#C9A84C] opacity-60"></div>
      <span class="text-[#C9A84C] text-2xl">✦</span>
      <div class="w-12 h-px bg-[#C9A84C] opacity-60"></div>
    </div>

    <h1 class="font-serif text-5xl sm:text-6xl font-light tracking-widest mb-2 fi fi1">NEIDE</h1>
    <p class="font-serif italic text-[#C9A84C] text-2xl mb-1 fi fi1">Perfumes Árabes</p>
    <p class="text-white/50 text-xs tracking-[0.3em] uppercase mb-8 fi fi2">Fragrâncias de Luxo Importadas</p>

    <div class="flex flex-wrap justify-center gap-8 fi fi3">
      <div class="text-center">
        <p class="text-[#C9A84C] font-serif text-3xl font-semibold">{{ total }}</p>
        <p class="text-white/50 text-xs tracking-widest uppercase">Produtos</p>
      </div>
      <div class="w-px bg-white/20 hidden sm:block"></div>
      <div class="text-center">
        <p class="text-[#C9A84C] font-serif text-3xl font-semibold">{{ brands|length }}</p>
        <p class="text-white/50 text-xs tracking-widest uppercase">Marcas</p>
      </div>
      <div class="w-px bg-white/20 hidden sm:block"></div>
      <div class="text-center">
        <p class="text-[#C9A84C] font-serif text-3xl font-semibold">✦</p>
        <p class="text-white/50 text-xs tracking-widest uppercase">Qualidade Premium</p>
      </div>
    </div>
  </div>
</header>

<!-- FILTROS -->
<div class="sticky top-0 z-30 shadow-lg filter-bar">
  <div class="max-w-6xl mx-auto px-4 py-3">
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 items-end">

      <div class="col-span-2 lg:col-span-1 relative">
        <label class="block text-[10px] text-[#1C3A2F] font-bold tracking-widest uppercase mb-1">Buscar Perfume</label>
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input id="fs" type="text" placeholder="Nome do perfume..."
            class="w-full pl-10 pr-4 py-2.5 border border-[#C9A84C]/30 rounded-xl bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#C9A84C]/40 transition-all">
        </div>
      </div>

      <div>
        <label class="block text-[10px] text-[#1C3A2F] font-bold tracking-widest uppercase mb-1">Marca</label>
        <select id="fb" class="w-full px-3 py-2.5 border border-[#C9A84C]/30 rounded-xl bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#C9A84C]/40 transition-all appearance-none">
          <option value="">Todas as Marcas</option>
          {% for b in brands %}<option value="{{ b }}">{{ b }}</option>{% endfor %}
        </select>
      </div>

      <div>
        <label class="block text-[10px] text-[#1C3A2F] font-bold tracking-widest uppercase mb-1">Gênero</label>
        <select id="fg" class="w-full px-3 py-2.5 border border-[#C9A84C]/30 rounded-xl bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#C9A84C]/40 transition-all appearance-none">
          <option value="">Todos</option>
          <option value="Feminino">Feminino</option>
          <option value="Masculino">Masculino</option>
          <option value="Unissex">Unissex</option>
        </select>
      </div>

      <div>
        <label class="block text-[10px] text-[#1C3A2F] font-bold tracking-widest uppercase mb-1">Faixa de Preço</label>
        <select id="fp" class="w-full px-3 py-2.5 border border-[#C9A84C]/30 rounded-xl bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#C9A84C]/40 transition-all appearance-none">
          <option value="">Todos os Preços</option>
          <option value="0-250">Até R$ 250</option>
          <option value="250-400">R$ 250 a R$ 400</option>
          <option value="400-99999">Acima de R$ 400</option>
        </select>
      </div>
    </div>

    <div class="mt-2 flex items-center gap-3">
      <span id="rc" class="text-xs text-[#1C3A2F]/60 font-medium"></span>
      <button id="cl" class="hidden text-xs text-[#C9A84C] font-semibold hover:text-[#9E7A28] transition-colors">✕ Limpar filtros</button>
    </div>
  </div>
</div>

<!-- GRID DE PRODUTOS -->
<main class="max-w-6xl mx-auto px-4 py-10">
  <div id="nr" class="hidden text-center py-24">
    <p class="font-serif text-3xl text-[#1C3A2F]/30 mb-2">Nenhum perfume encontrado</p>
    <p class="text-sm text-[#2C2C2C]/40">Tente ajustar os filtros.</p>
  </div>

  <div id="grid" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-5">
    {% for p in products %}
    <a href="{{ url_for('product_detail', reference=p.reference) }}"
       class="product-card card-hover group relative bg-white rounded-2xl overflow-hidden shadow-sm border border-[#C9A84C]/10 flex flex-col {% if not p.is_available %}opacity-60{% endif %}"
       data-name="{{ p.name|lower }}"
       data-brand="{{ p.brand }}"
       data-gender="{{ p.gender }}"
       data-price="{{ p.price }}">

      {% if not p.is_available %}
      <div class="absolute top-2 left-2 z-10 bg-[#2C2C2C] text-white text-[9px] font-bold tracking-widest uppercase px-2 py-0.5 rounded-full pulse">Esgotado</div>
      {% endif %}

      <div class="absolute top-2 right-2 z-10">
        {% if p.gender == 'Feminino' %}
        <span class="bg-rose-100 text-rose-600 text-[9px] font-bold tracking-widest uppercase px-2 py-0.5 rounded-full">Fem</span>
        {% elif p.gender == 'Masculino' %}
        <span class="bg-sky-100 text-sky-600 text-[9px] font-bold tracking-widest uppercase px-2 py-0.5 rounded-full">Masc</span>
        {% else %}
        <span class="bg-amber-100 text-amber-600 text-[9px] font-bold tracking-widest uppercase px-2 py-0.5 rounded-full">Uniss</span>
        {% endif %}
      </div>

      <div class="aspect-square bg-[#F0EBE1] flex items-center justify-center overflow-hidden">
        {% if p.img_url %}
        <img src="{{ p.img_url }}" alt="{{ p.name }}"
             class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy">
        {% else %}
        <div class="w-full h-full flex flex-col items-center justify-center gap-2">
          <svg class="w-12 h-12 text-[#C9A84C]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
          <span class="text-[9px] text-[#C9A84C]/40 tracking-widest uppercase">Sem imagem</span>
        </div>
        {% endif %}
      </div>

      <div class="p-3 flex flex-col flex-1 gap-1">
        <p class="text-[9px] text-[#C9A84C] tracking-widest uppercase font-bold">{{ p.brand }}</p>
        <p class="text-xs font-medium text-[#2C2C2C] leading-tight line-clamp-2 flex-1">{{ p.name }}</p>
        {% if p.description %}
        <p class="text-[10px] text-[#2C2C2C]/50 leading-snug line-clamp-2 mt-0.5">{{ p.description }}</p>
        {% endif %}
        <div class="flex items-center justify-between mt-2">
          <p class="font-serif text-base font-semibold text-[#1C3A2F]">R$ {{ "%.2f"|format(p.price)|replace('.', ',') }}</p>
          <span class="text-[9px] text-[#2C2C2C]/40">Ref: {{ p.reference }}</span>
        </div>
      </div>
    </a>
    {% endfor %}
  </div>
</main>

"""
    + SHARED_FOOTER
    + """

<script>
(function(){
  const fs=document.getElementById('fs'),
        fb=document.getElementById('fb'),
        fg=document.getElementById('fg'),
        fp=document.getElementById('fp'),
        rc=document.getElementById('rc'),
        cl=document.getElementById('cl'),
        nr=document.getElementById('nr'),
        cards=[...document.querySelectorAll('.product-card')];

  function run(){
    const q=fs.value.toLowerCase().trim(),
          b=fb.value, g=fg.value, pr=fp.value;
    let v=0;
    cards.forEach(c=>{
      const nm=!q||c.dataset.name.includes(q),
            bm=!b||c.dataset.brand===b,
            gm=!g||c.dataset.gender===g;
      let pm=true;
      if(pr){const[lo,hi]=pr.split('-').map(Number);pm=+c.dataset.price>=lo&&+c.dataset.price<=hi;}
      const show=nm&&bm&&gm&&pm;
      c.classList.toggle('hidden',!show);
      if(show)v++;
    });
    rc.textContent=v+' produto'+(v!==1?'s':'')+' encontrado'+(v!==1?'s':'');
    nr.classList.toggle('hidden',v>0);
    cl.classList.toggle('hidden',!(q||b||g||pr));
  }

  cl.addEventListener('click',()=>{fs.value='';fb.value='';fg.value='';fp.value='';run();});
  [fs,fb,fg,fp].forEach(e=>e.addEventListener('input',run));
  run();
})();
</script>
</body>
</html>"""
)

# ===========================================================================
# TEMPLATE — DETALHE DO PRODUTO
# ===========================================================================
DETAIL_TEMPLATE = (
    """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ p.name }} | NEIDE PERFUMES ÁRABES</title>
  <meta name="description" content="{{ p.name }} — R$ {{ '%.2f'|format(p.price)|replace('.', ',') }}. Ref: {{ p.reference }}.">
  """
    + SHARED_CSS
    + """
</head>
<body class="bg-[#FAF7F2] font-sans text-[#2C2C2C] antialiased min-h-screen">

<nav class="bg-[#1C3A2F] text-white py-4 px-4 shadow-lg">
  <div class="max-w-5xl mx-auto flex items-center justify-between">
    <a href="{{ url_for('catalog') }}" class="flex items-center gap-2 text-[#C9A84C] hover:text-[#E2C47E] transition-colors alink">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
      <span class="text-sm font-medium">Voltar ao Catálogo</span>
    </a>
    <p class="font-serif text-[#C9A84C] text-lg tracking-widest hidden sm:block">NEIDE PERFUMES ÁRABES</p>
    <div class="w-32"></div>
  </div>
</nav>

<main class="max-w-5xl mx-auto px-4 py-12">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-10 items-start">

    <!-- Imagem -->
    <div class="fi">
      <div class="rounded-3xl overflow-hidden shadow-2xl bg-[#F0EBE1] aspect-square flex items-center justify-center relative border border-[#C9A84C]/10">
        {% if img_url %}
        <img src="{{ img_url }}" alt="{{ p.name }}" class="w-full h-full object-contain">
        {% else %}
        <div class="flex flex-col items-center justify-center w-full h-full gap-4 p-10">
          <div class="w-28 h-28 rounded-full bg-[#1C3A2F]/5 flex items-center justify-center border-2 border-dashed border-[#C9A84C]/30">
            <svg class="w-14 h-14 text-[#C9A84C]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
            </svg>
          </div>
          <p class="text-sm text-[#1C3A2F]/40 italic font-serif">Imagem em breve</p>
        </div>
        {% endif %}

        {% if not p.is_available %}
        <div class="absolute inset-0 bg-[#2C2C2C]/60 flex items-center justify-center rounded-3xl backdrop-blur-sm">
          <div class="text-center text-white">
            <p class="font-serif text-2xl mb-1">Esgotado</p>
            <p class="text-sm opacity-70">Temporariamente Indisponível</p>
          </div>
        </div>
        {% endif %}
      </div>
    </div>

    <!-- Informações -->
    <div class="fi fi2 flex flex-col gap-5">

      <div class="flex flex-wrap gap-2">
        <span class="bg-[#1C3A2F]/10 text-[#1C3A2F] text-xs font-bold tracking-widest uppercase px-3 py-1 rounded-full">{{ p.brand }}</span>
        {% if p.gender == 'Feminino' %}
        <span class="bg-rose-100 text-rose-600 text-xs font-bold tracking-widest uppercase px-3 py-1 rounded-full">Feminino</span>
        {% elif p.gender == 'Masculino' %}
        <span class="bg-sky-100 text-sky-600 text-xs font-bold tracking-widest uppercase px-3 py-1 rounded-full">Masculino</span>
        {% else %}
        <span class="bg-amber-100 text-amber-600 text-xs font-bold tracking-widest uppercase px-3 py-1 rounded-full">Unissex</span>
        {% endif %}
        {% if not p.is_available %}
        <span class="bg-red-100 text-red-600 text-xs font-bold tracking-widest uppercase px-3 py-1 rounded-full pulse">Temporariamente Esgotado</span>
        {% endif %}
      </div>

      <h1 class="font-serif text-3xl sm:text-4xl font-light text-[#2C2C2C] leading-tight">{{ p.name }}</h1>

      <p class="font-serif text-4xl font-semibold text-[#1C3A2F]">
        R$ {{ "%.2f"|format(p.price)|replace('.', ',') }}
      </p>

      <div class="py-3 border-y border-[#C9A84C]/20">
        <span class="text-xs text-[#2C2C2C]/50 tracking-widest uppercase">Referência</span>
        <p class="font-mono text-sm font-medium text-[#2C2C2C] mt-0.5">#{{ p.reference }}</p>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="bg-[#FAF7F2] rounded-xl p-4 border border-[#C9A84C]/10">
          <p class="text-[10px] text-[#2C2C2C]/50 tracking-widest uppercase mb-1">Marca</p>
          <p class="font-medium text-sm">{{ p.brand }}</p>
        </div>
        <div class="bg-[#FAF7F2] rounded-xl p-4 border border-[#C9A84C]/10">
          <p class="text-[10px] text-[#2C2C2C]/50 tracking-widest uppercase mb-1">Gênero</p>
          <p class="font-medium text-sm">{{ p.gender }}</p>
        </div>
      </div>

      {% if p.description %}
      <div class="bg-[#FAF7F2] rounded-2xl p-5 border border-[#C9A84C]/10">
        <p class="text-[10px] text-[#C9A84C] tracking-widest uppercase font-bold mb-2">✦ Sobre este perfume</p>
        <p class="text-sm text-[#2C2C2C]/80 leading-relaxed whitespace-pre-line">{{ p.description }}</p>
      </div>
      {% endif %}

      <div class="space-y-3">
        {% if p.is_available %}
        <a id="whatsapp-btn" href="{{ wa_url }}" target="_blank" rel="noopener noreferrer"
           class="flex items-center justify-center gap-3 w-full py-4 px-6 rounded-2xl font-semibold text-white text-base transition-all duration-300 shadow-lg hover:shadow-xl hover:-translate-y-1"
           style="background:linear-gradient(135deg,#25D366,#128C7E)">
          <svg class="w-6 h-6 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
          Chamar no WhatsApp com este produto
        </a>
        {% else %}
        <div class="flex items-center justify-center w-full py-4 px-6 rounded-2xl bg-[#2C2C2C]/20 text-[#2C2C2C]/40 text-base cursor-not-allowed select-none">
          Produto Temporariamente Esgotado
        </div>
        {% endif %}

        <a href="{{ url_for('catalog') }}"
           class="flex items-center justify-center gap-2 w-full py-3 px-6 rounded-2xl border border-[#C9A84C]/40 text-[#1C3A2F] font-medium text-sm hover:bg-[#1C3A2F] hover:text-white hover:border-[#1C3A2F] transition-all duration-300">
          Ver Catálogo Completo
        </a>
      </div>
    </div>
  </div>
</main>

"""
    + SHARED_FOOTER
    + """
</body>
</html>"""
)

# ===========================================================================
# TEMPLATE — LOGIN ADMIN
# ===========================================================================
ADMIN_LOGIN_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Acesso Restrito</title>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
  tailwind.config={theme:{extend:{colors:{forest:'#1C3A2F',gold:'#C9A84C'},fontFamily:{serif:['Cormorant Garamond','serif'],sans:['Inter','sans-serif']}}}}
  </script>
  <style>
    body{background:linear-gradient(135deg,#0d1f19,#1C3A2F)}
    @keyframes fi{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    .card{animation:fi .6s ease both}
  </style>
</head>
<body class="min-h-screen flex items-center justify-center font-sans p-4">
  <div class="card w-full max-w-sm">
    <div class="text-center mb-8">
      <p class="font-serif text-[#C9A84C] text-5xl">✦</p>
      <h1 class="font-serif text-2xl text-white mt-3 tracking-widest">Área Restrita</h1>
      <p class="text-white/40 text-xs mt-1 tracking-widest uppercase">Acesso Administrativo</p>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
    {% for cat, msg in messages %}
    <div class="mb-4 px-4 py-3 rounded-xl text-sm
      {% if cat == 'error' %}bg-red-900/40 text-red-300 border border-red-700/40{% else %}bg-green-900/40 text-green-300 border border-green-700/40{% endif %}">
      {{ msg }}
    </div>
    {% endfor %}
    {% endwith %}

    <form method="POST" class="space-y-4">
      <div>
        <label class="block text-xs text-white/50 tracking-widest uppercase mb-2">Senha</label>
        <input type="password" name="password" id="admin-password" autofocus placeholder="••••••••"
          class="w-full px-4 py-3 rounded-xl bg-white/10 text-white placeholder-white/30 border border-white/10 focus:outline-none focus:border-[#C9A84C]/60 focus:ring-1 focus:ring-[#C9A84C]/40 transition-all">
      </div>
      <button type="submit" id="admin-login-btn"
        class="w-full py-3 rounded-xl font-semibold text-[#122419] hover:-translate-y-0.5 hover:shadow-lg transition-all duration-300"
        style="background:linear-gradient(135deg,#C9A84C,#E2C47E)">
        Entrar
      </button>
    </form>
  </div>
</body>
</html>"""

# ===========================================================================
# TEMPLATE — DASHBOARD ADMIN
# ===========================================================================
ADMIN_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Painel Admin | NEIDE PERFUMES ÁRABES</title>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
  tailwind.config={theme:{extend:{colors:{forest:{DEFAULT:'#1C3A2F',dark:'#122419',light:'#2A5240'},gold:{DEFAULT:'#C9A84C',light:'#E2C47E',dark:'#9E7A28'}},fontFamily:{serif:['Cormorant Garamond','serif'],sans:['Inter','sans-serif']}}}}
  </script>
  <style>
    ::-webkit-scrollbar{width:6px}
    ::-webkit-scrollbar-thumb{background:#C9A84C;border-radius:3px}
    .acard{transition:box-shadow .2s ease}
    .acard:hover{box-shadow:0 8px 30px rgba(201,168,76,.15)}
    input[type=file]::file-selector-button{background:#1C3A2F;color:#C9A84C;border:none;padding:4px 12px;border-radius:6px;cursor:pointer;font-size:12px}
  </style>
</head>
<body class="bg-gray-50 font-sans text-gray-800 min-h-screen">

<nav class="text-white px-6 py-4 shadow-xl sticky top-0 z-50" style="background:linear-gradient(135deg,#122419,#1C3A2F)">
  <div class="max-w-7xl mx-auto flex items-center justify-between">
    <div class="flex items-center gap-4">
      <span class="text-[#C9A84C] font-serif text-xl">✦</span>
      <div>
        <p class="font-serif text-[#C9A84C] tracking-widest text-sm">NEIDE PERFUMES ÁRABES</p>
        <p class="text-white/50 text-xs tracking-widest uppercase">Painel Administrativo</p>
      </div>
    </div>
    <div class="flex items-center gap-3">
      <span class="text-white/50 text-xs">{{ products|length }} produtos</span>
      <a href="{{ url_for('catalog') }}" class="text-xs text-[#C9A84C]/80 hover:text-[#C9A84C] border border-[#C9A84C]/30 px-3 py-1.5 rounded-lg hover:border-[#C9A84C] transition-all">Ver Catálogo</a>
      <a href="{{ url_for('admin_logout') }}" class="text-xs text-white/60 hover:text-white px-3 py-1.5 rounded-lg hover:bg-white/10 transition-all">Sair</a>
    </div>
  </div>
</nav>

{% with messages = get_flashed_messages(with_categories=true) %}
{% for cat, msg in messages %}
<div class="max-w-7xl mx-auto mt-4 px-6">
  <div class="px-4 py-3 rounded-xl text-sm font-medium
    {% if cat=='error' %}bg-red-50 text-red-700 border border-red-200
    {% elif cat=='success' %}bg-green-50 text-green-700 border border-green-200
    {% else %}bg-blue-50 text-blue-700 border border-blue-200{% endif %}">
    {{ msg }}
  </div>
</div>
{% endfor %}
{% endwith %}

<div class="max-w-7xl mx-auto px-6 py-6">

  <!-- Stats -->
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
    <div class="bg-white rounded-2xl p-4 shadow-sm border border-[#C9A84C]/10">
      <p class="text-xs text-gray-500 tracking-widest uppercase">Total</p>
      <p class="font-serif text-3xl text-[#1C3A2F] mt-1">{{ products|length }}</p>
    </div>
    <div class="bg-white rounded-2xl p-4 shadow-sm border border-[#C9A84C]/10">
      <p class="text-xs text-gray-500 tracking-widest uppercase">Disponíveis</p>
      <p class="font-serif text-3xl text-green-600 mt-1">{{ products|selectattr('is_available')|list|length }}</p>
    </div>
    <div class="bg-white rounded-2xl p-4 shadow-sm border border-[#C9A84C]/10">
      <p class="text-xs text-gray-500 tracking-widest uppercase">Esgotados</p>
      <p class="font-serif text-3xl text-red-500 mt-1">{{ products|rejectattr('is_available')|list|length }}</p>
    </div>
    <div class="bg-white rounded-2xl p-4 shadow-sm border border-[#C9A84C]/10">
      <p class="text-xs text-gray-500 tracking-widest uppercase">Com Imagem</p>
      <p class="font-serif text-3xl text-[#C9A84C] mt-1">{{ products|selectattr('image_path')|list|length }}</p>
    </div>
  </div>

  <!-- Busca -->
  <div class="mb-6 flex gap-3 items-center">
    <div class="relative flex-1 max-w-sm">
      <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#C9A84C]/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      <input id="as" type="text" placeholder="Buscar produto..."
        class="w-full pl-10 pr-4 py-2.5 border border-[#C9A84C]/30 rounded-xl bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#C9A84C]/30">
    </div>
    <span id="ac" class="text-sm text-gray-500"></span>
  </div>

  <!-- Grid de produtos admin -->
  <div id="agrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
    {% for p in products %}
    <div class="acard product-admin-card bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100"
         data-name="{{ p.name|lower }}">

      <div class="aspect-video bg-gray-50 flex items-center justify-center overflow-hidden relative border-b border-gray-100">
        {% if p.img_url %}
        <img src="{{ p.img_url }}" alt="{{ p.name }}" class="w-full h-full object-contain p-2">
        {% else %}
        <div class="flex flex-col items-center gap-2 text-gray-300 p-4">
          <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <span class="text-xs">Sem imagem</span>
        </div>
        {% endif %}
        <div class="absolute top-2 left-2">
          {% if p.is_available %}
          <span class="bg-green-100 text-green-700 text-[9px] font-bold px-2 py-0.5 rounded-full uppercase tracking-widest">Disponível</span>
          {% else %}
          <span class="bg-red-100 text-red-600 text-[9px] font-bold px-2 py-0.5 rounded-full uppercase tracking-widest">Esgotado</span>
          {% endif %}
        </div>
      </div>

      <div class="p-4 space-y-3">
        <div>
          <p class="text-[9px] text-[#C9A84C] font-bold tracking-widest uppercase">{{ p.brand }} · Ref: {{ p.reference }}</p>
          <p class="text-sm font-medium text-gray-800 leading-tight mt-0.5 line-clamp-2">{{ p.name }}</p>
          <p class="font-serif text-base text-[#1C3A2F] font-semibold mt-1">R$ {{ "%.2f"|format(p.price)|replace('.', ',') }}</p>
        </div>

        <form method="POST" action="{{ url_for('admin_toggle', reference=p.reference) }}">
          <button id="toggle-{{ p.reference }}"
            class="w-full text-xs font-semibold py-2 rounded-xl transition-all duration-200
            {% if p.is_available %}bg-red-50 text-red-600 hover:bg-red-100 border border-red-200
            {% else %}bg-green-50 text-green-700 hover:bg-green-100 border border-green-200{% endif %}">
            {% if p.is_available %}⬜ Marcar como Esgotado{% else %}✅ Marcar como Disponível{% endif %}
          </button>
        </form>

        <form method="POST" action="{{ url_for('admin_upload', reference=p.reference) }}" enctype="multipart/form-data"
              onsubmit="document.getElementById('ub-{{p.reference}}').textContent='⏳ Enviando...'">
          <label class="block text-[9px] text-gray-500 tracking-widest uppercase font-bold mb-1">Enviar Imagem (JPG/PNG · máx 5 MB)</label>
          <input type="file" name="image" accept=".jpg,.jpeg,.png"
            class="w-full text-xs text-gray-600 border border-gray-200 rounded-lg p-1.5 mb-2 focus:outline-none">
          <button type="submit" id="ub-{{ p.reference }}"
            class="w-full text-xs font-semibold py-2 rounded-xl bg-[#1C3A2F] text-[#C9A84C] hover:bg-[#122419] border border-[#1C3A2F]/20 transition-all duration-200">
            ↑ Enviar Imagem
          </button>
        </form>

        <form method="POST" action="{{ url_for('admin_update_description', reference=p.reference) }}"
              onsubmit="document.getElementById('db-{{p.reference}}').textContent='⏳ Salvando...'">
          <label class="block text-[9px] text-gray-500 tracking-widest uppercase font-bold mb-1">Descrição do Produto</label>
          <textarea name="description" rows="3" placeholder="Notas olfativas, família, volume, intensidade…"
            class="w-full text-xs text-gray-700 border border-gray-200 rounded-lg p-2 mb-2 focus:outline-none focus:ring-1 focus:ring-[#C9A84C]/40 resize-none leading-relaxed">{{ p.description or '' }}</textarea>
          <button type="submit" id="db-{{ p.reference }}"
            class="w-full text-xs font-semibold py-2 rounded-xl bg-[#FAF7F2] text-[#1C3A2F] hover:bg-[#F0EBE1] border border-[#C9A84C]/30 transition-all duration-200">
            💾 Salvar Descrição
          </button>
        </form>
      </div>
    </div>
    {% endfor %}
  </div>
</div>

<script>
const as=document.getElementById('as'),
      ac=document.getElementById('ac'),
      cards=[...document.querySelectorAll('.product-admin-card')];
function run(){
  const q=as.value.toLowerCase().trim();
  let v=0;
  cards.forEach(c=>{
    const show=!q||c.dataset.name.includes(q);
    c.style.display=show?'':'none';
    if(show)v++;
  });
  ac.textContent=v+' produto'+(v!==1?'s':'')+' visível'+(v!==1?'is':'');
}
as.addEventListener('input',run);
run();
</script>
</body>
</html>"""

# ===========================================================================
# ROTAS PÚBLICAS
# ===========================================================================


@app.route("/")
def catalog():
    """Exibe o catálogo público de perfumes com filtros."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM products ORDER BY is_available DESC, name ASC"
    ).fetchall()
    products = []
    for row in rows:
        p = dict(row)
        p["img_url"] = image_url(p.get("image_path"))
        products.append(p)
    brands = sorted({p["brand"] for p in products if p["brand"]}, key=str.lower)
    return render_template_string(
        CATALOG_TEMPLATE,
        products=products,
        brands=brands,
        total=len(products),
        year=datetime.date.today().year,
    )


@app.route("/produto/<reference>")
def product_detail(reference):
    """Exibe a página de detalhe de um produto pelo número de referência."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM products WHERE reference=?", (reference,)
    ).fetchone()
    if row is None:
        abort(404)
    p = dict(row)
    img = image_url(p.get("image_path"))
    wa_text = (
        f"Olá Neide, tenho interesse no perfume {p['name']} "
        f"(Ref: {p['reference']}), listado no catálogo!"
    )
    wa_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(wa_text)}"
    return render_template_string(
        DETAIL_TEMPLATE,
        p=p,
        img_url=img,
        wa_url=wa_url,
        year=datetime.date.today().year,
    )


# ===========================================================================
# ROTAS ADMIN
# ===========================================================================


@app.route(ADMIN_ROUTE, methods=["GET", "POST"])
def admin_login():
    """Tela de login do painel administrativo."""
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if secrets.compare_digest(pwd, ADMIN_PASSWORD):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Senha incorreta. Tente novamente.", "error")
    return render_template_string(ADMIN_LOGIN_TEMPLATE)


@app.route(ADMIN_ROUTE + "/dashboard")
@login_required
def admin_dashboard():
    """Dashboard administrativo: lista todos os produtos."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM products ORDER BY is_available DESC, name ASC"
    ).fetchall()
    products = [
        dict(r) | {"img_url": image_url(dict(r).get("image_path"))} for r in rows
    ]
    return render_template_string(ADMIN_TEMPLATE, products=products)


@app.route(ADMIN_ROUTE + "/toggle/<reference>", methods=["POST"])
@login_required
def admin_toggle(reference):
    """Alterna a disponibilidade (disponível/esgotado) de um produto."""
    db = get_db()
    row = db.execute(
        "SELECT is_available FROM products WHERE reference=?", (reference,)
    ).fetchone()
    if row is None:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("admin_dashboard"))
    new = 0 if row["is_available"] else 1
    db.execute("UPDATE products SET is_available=? WHERE reference=?", (new, reference))
    db.commit()
    flash(
        f"Produto Ref.{reference} marcado como {'disponível' if new else 'esgotado'}.",
        "success",
    )
    return redirect(url_for("admin_dashboard"))


@app.route(ADMIN_ROUTE + "/upload/<reference>", methods=["POST"])
@login_required
def admin_upload(reference):
    """Recebe e salva o upload de imagem de um produto."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM products WHERE reference=?", (reference,)
    ).fetchone()
    if row is None:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("admin_dashboard"))
    if "image" not in request.files:
        flash("Nenhum arquivo selecionado.", "error")
        return redirect(url_for("admin_dashboard"))
    f = request.files["image"]
    if not f.filename or not allowed_file(f.filename):
        flash("Formato inválido. Use JPG, JPEG ou PNG.", "error")
        return redirect(url_for("admin_dashboard"))
    f.seek(0, 2)
    sz = f.tell()
    f.seek(0)
    if sz > MAX_FILE_SIZE:
        flash("Arquivo muito grande. Limite: 5 MB.", "error")
        return redirect(url_for("admin_dashboard"))
    dest = safe_image_path(reference)
    f.save(dest)
    db.execute("UPDATE products SET image_path=? WHERE reference=?", (dest, reference))
    db.commit()
    flash(f"Imagem do produto Ref.{reference} enviada com sucesso! ✓", "success")
    return redirect(url_for("admin_dashboard"))


@app.route(ADMIN_ROUTE + "/logout")
def admin_logout():
    """Encerra a sessão do administrador."""
    session.clear()
    return redirect(url_for("catalog"))


# ===========================================================================
# ERROR HANDLERS
# ===========================================================================


@app.errorhandler(404)
def not_found(_e):
    """Página de erro 404 customizada."""
    return (
        render_template_string("""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><title>404 | NEIDE PERFUMES ÁRABES</title>
<script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-[#FAF7F2] min-h-screen flex flex-col items-center justify-center text-center px-4">
  <p class="text-6xl font-bold text-[#C9A84C] mb-4">404</p>
  <h1 class="text-2xl font-semibold text-[#1C3A2F] mb-2">Página não encontrada</h1>
  <p class="text-[#2C2C2C]/60 mb-8">A página que você procura não existe.</p>
  <a href="/" class="px-6 py-3 rounded-2xl bg-[#1C3A2F] text-[#C9A84C] font-semibold hover:bg-[#122419] transition-colors">
    Voltar ao Catálogo
  </a>
</body></html>"""),
        404,
    )


@app.errorhandler(413)
def too_large(_e):
    """Retorna ao painel se o arquivo enviado excede o limite."""
    flash("Arquivo muito grande. O limite é 5 MB.", "error")
    return redirect(url_for("admin_dashboard"))


# ===========================================================================
# ROTA ADMIN — ATUALIZAR DESCRIÇÃO
# ===========================================================================


@app.route(ADMIN_ROUTE + "/descricao/<reference>", methods=["POST"])
@login_required
def admin_update_description(reference):
    """Salva ou atualiza a descrição textual de um produto."""
    db = get_db()
    row = db.execute(
        "SELECT id FROM products WHERE reference=?", (reference,)
    ).fetchone()
    if row is None:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("admin_dashboard"))
    description = request.form.get("description", "").strip()
    db.execute(
        "UPDATE products SET description=? WHERE reference=?", (description, reference)
    )
    db.commit()
    flash(f"Descrição do produto Ref.{reference} atualizada! ✓", "success")
    return redirect(url_for("admin_dashboard"))


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  NEIDE PERFUMES ÁRABES — Catálogo Premium")
    print("=" * 60)
    init_db()
    print("[APP] Catálogo público : http://127.0.0.1:5000/")
    print(f"[APP] Painel admin     : http://127.0.0.1:5000{ADMIN_ROUTE}")
    print("[APP] Credenciais       : lidas do arquivo .env")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)
