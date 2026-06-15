#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
  RODRIGO IMPORTADOS ÁRABES — Image Scraper & Catalog Generator
==============================================================================
  Author  : Elite Python Data Engineer
  Purpose : Download product images from Bing/Yahoo Image Search and generate
            a stunning, responsive HTML catalog for 145 Arabic perfumes.
  Features:
    - Robust requests.Session() with persistent cookies
    - Full Chrome-mimicking headers (anti-bot bypass)
    - JSON-aware parsing of <script> blocks to find real image URLs
    - Fallback: <img> tag scraping inside Bing's result grid
    - Up to 3 retries per product with exponential back-off
    - Progressive rate-limiting (2.5 – 4 s random delay)
    - Skips already-downloaded images (resume-safe)
    - Generates a luxury dark-mode HTML catalog upon completion
==============================================================================
  Usage: python scraper_catalogo.py
==============================================================================
"""

import os
import re
import json
import time
import random
import logging
import hashlib
import urllib.parse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

OUTPUT_DIR = Path("static/images")
CATALOG_FILE = Path("catalogo.html")
MIN_IMAGE_BYTES = 2_048          # 2 KB minimum image size
MAX_RETRIES = 3
BASE_DELAY_S = 2.5
MAX_DELAY_S = 4.0
REQUEST_TIMEOUT = 15             # seconds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("scraper.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
#  PRODUCT DATA  (Reference, Name, Price in BRL)
# ─────────────────────────────────────────────────────────────────────────────

PRODUCTS = [
    ("338", "Venti Silky Princess Fragrance World / Queen of Silk Creed", 350.00),
    ("26",  "Afnan - Souvenir Desert Rose 100 ml", 400.00),
    ("428", "ajward pattafa 60ml", 300.00),
    ("438", "al nobre almeer lattafa", 350.00),
    ("262", "Al Sheikh EDP 100 ml da Sahari Collections", 250.00),
    ("37",  "Al Ward - Sabah 100 ml", 300.00),
    ("27",  "Al Wataniah - Ameerati 100 ml", 300.00),
    ("28",  "Al Wataniah - Attar Al Wesal 100 ml", 300.00),
    ("51",  "Al Wataniah - Boraq 75 ml", 280.00),
    ("14",  "Al Wataniah - Durrat Al Aroo 85 ml", 300.00),
    ("115", "Al Wataniah Al Layl EDP Unissex 100 ml", 290.00),
    ("85",  "Al Wataniah Ghala EDP Feminino 100 ml", 300.00),
    ("65",  "Al Wataniah Kenz Al Malik 100 ml", 290.00),
    ("297", "Al Wataniah Nawal Fluorite EDP Feminino 100 ml", 250.00),
    ("66",  "Al Wataniah Sultan Al Lail 100 ml", 240.00),
    ("302", "Al Wataniah Tiara Pink EDP 100 ml", 250.00),
    ("203", "Al Wataniah Tibyan 100 ml", 249.90),
    ("454", "Alpine Maison Alhambra", 300.00),
    ("418", "Amber Divine Passion Cool and Cool 100ml", 450.00),
    ("349", "Amnia Al Wataniah 100 ml", 330.00),
    ("53",  "Armaf - Infinity Gold 105 ml", 600.00),
    ("56",  "Asdaaf - Ameerat Al Arab 100 ml", 290.00),
    ("58",  "Asdaaf - Andaleeb Flora 100 ml", 280.00),
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
    ("21",  "Lattafa - Afeef 100 ml", 700.00),
    ("6",   "Lattafa - Asad 100 ml", 300.00),
    ("3",   "Lattafa - Asad Bourbon 100 ml", 330.00),
    ("311", "Lattafa - Asad Elixir 100 ml", 400.00),
    ("22",  "Lattafa - Atheeri 100 ml", 750.00),
    ("32",  "Lattafa - Fakhar 100 ml", 349.90),
    ("24",  "Lattafa - Fakhar Extrait Gold 100 ml", 349.90),
    ("23",  "Lattafa - Fakhar Platin 100 ml", 400.00),
    ("30",  "Lattafa - Fakhar Rose 100 ml", 350.00),
    ("34",  "Lattafa - Musamam White 100 ml", 550.00),
    ("48",  "Lattafa - Tharwah Gold 100 ml", 600.00),
    ("12",  "Lattafa - Yara 100 ml", 350.00),
    ("4",   "Lattafa Asad Zanzibar Limited Edition 100ml", 350.00),
    ("119", "Lattafa Pride La Collection d Antiquites 1910 100 ml", 399.90),
    ("267", "Legend Intense Emper Eau de Toilette Masculino", 290.00),
    ("408", "Liwan ard al zafaran", 400.00),
    ("348", "Mahib Adyan by anfar 100ml", 300.00),
    ("335", "Maison Alhambra Body Perfume Mist 250ml", 150.00),
    ("60",  "Manaal - Ard Al Zaafaran 100 ml", 400.00),
    ("446", "Marshmallow Blush Paris Corner", 450.00),
    ("52",  "Mawwal - Basir 100 ml", 450.00),
    ("436", "Mayar Lattafa", 300.00),
    ("195", "Maitre de Blue Maison Alhambra Masculino 100ml", 300.00),
    ("382", "Mia Dolcezza Maison Alhambra", 350.00),
    ("328", "Milena Ard Al Zaafaran 100 ml", 450.00),
    ("414", "Montaigne Vanille Maison Alhambra", 300.00),
    ("370", "norah lucher adyan", 300.00),
    ("400", "Oleo Concentrado Yara Lattafa 20ml", 250.00),
    ("433", "Oleo Concentrado Al Wataniah 12ml", 200.00),
    ("439", "Olivia Maison Alhambra", 300.00),
    ("19",  "Orientica Premium Royal Amber 80 ml", 750.00),
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
    ("99",  "Sing Kids 75ml lattafa pride", 200.00),
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
    ("40",  "Victorias s Secret - Body Splash 250 ml", 180.00),
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
    ("39",  "Arabe Collection Spray Corporal 200ml", 60.00),
]

# ─────────────────────────────────────────────────────────────────────────────
#  STORE INFO (for HTML catalog)
# ─────────────────────────────────────────────────────────────────────────────

STORE = {
    "name":      "RODRIGO IMPORTADOS ÁRABES",
    "email":     "rodrigoimportadosarabes@gmail.com",
    "whatsapp":  "+55 67 99696-2426",
    "whatsapp_link": "https://wa.me/5567996962426",
    "instagram": "@rodrigoimportadosarabes",
    "instagram_link": "https://instagram.com/rodrigoimportadosarabes",
}

# ─────────────────────────────────────────────────────────────────────────────
#  USER-AGENT POOL  (rotate to reduce fingerprinting)
# ─────────────────────────────────────────────────────────────────────────────

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
]

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION FACTORY
# ─────────────────────────────────────────────────────────────────────────────

def make_session() -> requests.Session:
    """Create a requests session that mimics a real browser."""
    session = requests.Session()
    ua = random.choice(USER_AGENTS)
    session.headers.update({
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "DNT": "1",
    })
    return session


# ─────────────────────────────────────────────────────────────────────────────
#  BING IMAGE SEARCH — JSON BLOCK PARSER
# ─────────────────────────────────────────────────────────────────────────────

def _extract_bing_urls_from_json_blocks(html_text: str) -> list[str]:
    """
    Bing embeds image metadata in AF_initDataCallback / inline JSON blobs
    inside <script> tags. We scan every script block, decode any JSON-like
    structure, and collect URLs that look like image links.
    """
    urls: list[str] = []

    # Pattern 1 – "murl":"https://..." (Bing's primary image URL field)
    urls += re.findall(r'"murl"\s*:\s*"(https?://[^"]+\.(?:jpg|jpeg|png|webp))"', html_text, re.IGNORECASE)

    # Pattern 2 – "imgurl":"..." (alternate field name)
    urls += re.findall(r'"imgurl"\s*:\s*"(https?://[^"]+\.(?:jpg|jpeg|png|webp))"', html_text, re.IGNORECASE)

    # Pattern 3 – turl (thumbnail url) — guaranteed smaller but always present
    urls += re.findall(r'"turl"\s*:\s*"(https?://[^"]+)"', html_text, re.IGNORECASE)

    # Pattern 4 – plain https image urls inside script blocks (broad fallback)
    soup = BeautifulSoup(html_text, "html.parser")
    for script in soup.find_all("script"):
        body = script.string or ""
        hits = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)', body, re.IGNORECASE)
        urls.extend(hits)

    # Deduplicate while preserving order
    seen: set[str] = set()
    result: list[str] = []
    for u in urls:
        u_clean = u.rstrip("\\")
        if u_clean not in seen:
            seen.add(u_clean)
            result.append(u_clean)
    return result


def _extract_bing_urls_from_img_tags(html_text: str) -> list[str]:
    """
    Fallback: pull URLs from visible <a> elements that wrap image thumbnails
    (data-thurl / data-src attributes Bing uses on the result grid).
    """
    urls: list[str] = []
    soup = BeautifulSoup(html_text, "html.parser")

    # Bing's image containers expose data-thurl (thumbnail) and data-murl (main)
    for tag in soup.find_all(True, {"data-murl": True}):
        v = tag.get("data-murl", "")
        if v.startswith("http"):
            urls.append(v)

    for tag in soup.find_all(True, {"data-thurl": True}):
        v = tag.get("data-thurl", "")
        if v.startswith("http"):
            urls.append(v)

    for tag in soup.find_all("img"):
        for attr in ("src", "data-src", "data-lazy-src"):
            v = tag.get(attr, "")
            if v.startswith("http") and any(ext in v.lower() for ext in (".jpg", ".jpeg", ".png", ".webp")):
                urls.append(v)

    return urls


def search_bing_images(session: requests.Session, query: str) -> list[str]:
    """
    Query Bing Image Search and return a deduplicated list of image URLs.
    Uses JSON-block parsing first, then falls back to img-tag scraping.
    """
    params = {
        "q":    query,
        "form": "HDRSC2",
        "first": "1",
        "tsc":  "ImageBasicHover",
    }
    url = "https://www.bing.com/images/search?" + urllib.parse.urlencode(params)

    headers_override = {
        "Referer": "https://www.bing.com/",
        "Sec-Fetch-Site": "same-origin",
    }

    resp = session.get(url, headers=headers_override, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()

    urls = _extract_bing_urls_from_json_blocks(resp.text)
    if not urls:
        log.debug("  Bing JSON parse yielded nothing; trying img-tag fallback.")
        urls = _extract_bing_urls_from_img_tags(resp.text)

    return urls


# ─────────────────────────────────────────────────────────────────────────────
#  YAHOO IMAGE SEARCH — JSON BLOCK PARSER
# ─────────────────────────────────────────────────────────────────────────────

def _extract_yahoo_image_urls(html_text: str) -> list[str]:
    """
    Yahoo Images stores image data in inline JSON inside <script> tags.
    We extract all URLs from those blobs.
    """
    urls: list[str] = []

    # Primary pattern – Yahoo wraps data in mosaic JSON arrays
    urls += re.findall(r'"ou"\s*:\s*"(https?://[^"]+\.(?:jpg|jpeg|png|webp))"', html_text, re.IGNORECASE)
    urls += re.findall(r'"url"\s*:\s*"(https?://[^"]+\.(?:jpg|jpeg|png|webp))"', html_text, re.IGNORECASE)

    # Broad fallback scan of all <script> content
    soup = BeautifulSoup(html_text, "html.parser")
    for script in soup.find_all("script"):
        body = script.string or ""
        hits = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)', body, re.IGNORECASE)
        urls.extend(hits)

    # Deduplicate
    seen: set[str] = set()
    result: list[str] = []
    for u in urls:
        u_clean = u.rstrip("\\")
        if u_clean not in seen:
            seen.add(u_clean)
            result.append(u_clean)
    return result


def search_yahoo_images(session: requests.Session, query: str) -> list[str]:
    """
    Query Yahoo Image Search and return a list of image URLs.
    """
    params = {
        "p":   query,
        "fr":  "yfp-t",
        "fr2": "p%3As%2Cv%3Ai",
        "ei":  "UTF-8",
        "x":   "wrt",
        "iscqry": "",
    }
    url = "https://images.search.yahoo.com/search/images?" + urllib.parse.urlencode(params)

    headers_override = {
        "Referer": "https://search.yahoo.com/",
        "Sec-Fetch-Site": "same-site",
    }

    resp = session.get(url, headers=headers_override, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()

    return _extract_yahoo_image_urls(resp.text)


# ─────────────────────────────────────────────────────────────────────────────
#  IMAGE DOWNLOADER
# ─────────────────────────────────────────────────────────────────────────────

VALID_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

def download_image(session: requests.Session, image_url: str, dest_path: Path) -> bool:
    """
    Download *image_url* and save to *dest_path*.
    Returns True on success (file > MIN_IMAGE_BYTES), False otherwise.
    Skips tracking/redirect URLs that don't point to real images.
    """
    try:
        headers_override = {
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "https://www.bing.com/",
        }
        resp = session.get(
            image_url,
            headers=headers_override,
            timeout=REQUEST_TIMEOUT,
            stream=True,
            allow_redirects=True,
        )
        resp.raise_for_status()

        # Validate content-type
        ct = resp.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if ct and ct not in VALID_CONTENT_TYPES and not ct.startswith("image/"):
            log.debug("    Skipping non-image content-type: %s", ct)
            return False

        # Read body
        data = resp.content
        if len(data) < MIN_IMAGE_BYTES:
            log.debug("    Skipping tiny response (%d bytes).", len(data))
            return False

        dest_path.write_bytes(data)
        log.info("    ✓ Saved %d bytes → %s", len(data), dest_path.name)
        return True

    except requests.exceptions.RequestException as exc:
        log.debug("    Download failed (%s): %s", type(exc).__name__, exc)
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN SCRAPING LOOP
# ─────────────────────────────────────────────────────────────────────────────

def sanitize_query(name: str) -> str:
    """Produce a clean search query from the product name (English-friendly)."""
    # Remove parenthetical qualifiers and pipe characters
    name = re.sub(r"\(.*?\)", "", name)
    name = name.replace("/", " ").replace("|", " ")
    # Strip excess whitespace
    name = " ".join(name.split())
    return f"{name} perfume"


def run_scraper() -> dict[str, bool]:
    """
    Main loop. Iterates all 145 products, searches for images, downloads them.
    Returns a dict mapping ref → True/False (whether an image was saved).
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, bool] = {}
    session = make_session()

    total = len(PRODUCTS)
    for idx, (ref, name, price) in enumerate(PRODUCTS, start=1):
        dest = OUTPUT_DIR / f"ref_{ref}.jpg"

        # ── Skip if already downloaded ──────────────────────────────────────
        if dest.exists() and dest.stat().st_size > MIN_IMAGE_BYTES:
            log.info("[%d/%d] SKIP  ref_%s — already downloaded.", idx, total, ref)
            results[ref] = True
            continue

        log.info("[%d/%d] Processing ref_%s — %s", idx, total, ref, name)
        query = sanitize_query(name)
        saved = False

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # ── Try Bing first, then Yahoo ──────────────────────────────
                image_urls: list[str] = []
                try:
                    image_urls = search_bing_images(session, query)
                    log.debug("  Bing returned %d URLs.", len(image_urls))
                except requests.exceptions.HTTPError as e:
                    log.warning("  Bing HTTP %s — switching to Yahoo.", e.response.status_code)
                except requests.exceptions.RequestException as e:
                    log.warning("  Bing request error (%s) — switching to Yahoo.", e)

                if not image_urls:
                    try:
                        image_urls = search_yahoo_images(session, query)
                        log.debug("  Yahoo returned %d URLs.", len(image_urls))
                    except requests.exceptions.HTTPError as e:
                        log.warning("  Yahoo HTTP %s on attempt %d.", e.response.status_code, attempt)
                    except requests.exceptions.RequestException as e:
                        log.warning("  Yahoo request error (%s) on attempt %d.", e, attempt)

                # ── Try downloading each URL until one succeeds ─────────────
                for img_url in image_urls[:15]:   # try up to first 15 candidates
                    if download_image(session, img_url, dest):
                        saved = True
                        break

                if saved:
                    break   # exit retry loop

                log.warning("  No valid image on attempt %d/%d.", attempt, MAX_RETRIES)

                # Rotate User-Agent after a failure to reduce detection
                session.headers["User-Agent"] = random.choice(USER_AGENTS)

                # Exponential backoff between retries
                backoff = min(BASE_DELAY_S * (2 ** (attempt - 1)), 20)
                log.info("  Waiting %.1f s before retry…", backoff)
                time.sleep(backoff)

            except Exception as exc:
                log.error("  Unexpected error on attempt %d: %s", attempt, exc)
                time.sleep(BASE_DELAY_S)

        results[ref] = saved
        if not saved:
            log.error("  ✗ FAILED to download image for ref_%s — %s", ref, name)

        # ── Polite delay between products (anti-ban) ──────────────────────
        delay = random.uniform(BASE_DELAY_S, MAX_DELAY_S)
        log.debug("  Sleeping %.2f s…", delay)
        time.sleep(delay)

    return results


# ─────────────────────────────────────────────────────────────────────────────
#  HTML CATALOG GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

PLACEHOLDER_SVG = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'"
    " viewBox='0 0 300 300'%3E%3Crect width='300' height='300' fill='%231a1a2e'/%3E"
    "%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle'"
    " font-size='14' fill='%23888' font-family='sans-serif'%3EImagem%20Indispon%C3%ADvel%3C/text%3E%3C/svg%3E"
)


def format_price(price: float) -> str:
    return f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def generate_catalog(results: dict[str, bool]) -> None:
    """Render a luxury dark-mode HTML catalog with a responsive CSS grid."""

    # Build product cards HTML
    cards_html = []
    for ref, name, price in PRODUCTS:
        img_path = f"public/assets/images/perfumes/ref_{ref}.jpg"
        img_exists = results.get(ref, False)
        img_src = img_path if img_exists else PLACEHOLDER_SVG

        badge = ""
        if price >= 600:
            badge = '<span class="badge badge-premium">Premium</span>'
        elif price >= 400:
            badge = '<span class="badge badge-luxo">Luxo</span>'

        wa_msg = urllib.parse.quote(f"Olá! Tenho interesse no perfume: {name} (Ref. {ref}). Preço: {format_price(price)}")
        wa_url = f"https://wa.me/5567996962426?text={wa_msg}"

        cards_html.append(f"""
        <article class="card" id="produto-{ref}" data-ref="{ref}" data-price="{price}" data-name="{name.lower()}">
          <div class="card-image-wrap">
            <img
              src="{img_src}"
              alt="{name}"
              class="card-img"
              loading="lazy"
              onerror="this.src='{PLACEHOLDER_SVG}'"
            />
            <div class="card-overlay">
              <a href="{wa_url}" target="_blank" rel="noopener" class="btn-comprar">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                  <path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.118 1.528 5.846L.057 23.885l6.187-1.438A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.894a9.892 9.892 0 01-5.012-1.361l-.36-.214-3.733.867.934-3.613-.235-.373A9.868 9.868 0 012.106 12C2.106 6.533 6.533 2.106 12 2.106S21.894 6.533 21.894 12 17.467 21.894 12 21.894z"/>
                </svg>
                Pedir no WhatsApp
              </a>
            </div>
            {badge}
          </div>
          <div class="card-info">
            <p class="card-ref">Ref. #{ref}</p>
            <h3 class="card-name">{name}</h3>
            <p class="card-price">{format_price(price)}</p>
          </div>
        </article>""")

    cards_joined = "\n".join(cards_html)

    # Stats
    total_products = len(PRODUCTS)
    images_ok = sum(1 for v in results.values() if v)
    images_missing = total_products - images_ok

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Catálogo oficial de perfumes árabes importados da loja {STORE['name']}. Fragrâncias premium para homens e mulheres. WhatsApp: {STORE['whatsapp']}." />
  <meta property="og:title" content="Catálogo — {STORE['name']}" />
  <meta property="og:description" content="Perfumes árabes importados premium. Encomende agora pelo WhatsApp!" />
  <meta property="og:type" content="website" />
  <title>Catálogo de Perfumes — {STORE['name']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    /* ══════════════════════════════════════════════
       DESIGN TOKENS — LUXURY DARK PALETTE
    ══════════════════════════════════════════════ */
    :root {{
      --clr-bg:          #0b0b12;
      --clr-surface:     #13131f;
      --clr-surface-2:   #1b1b2e;
      --clr-border:      rgba(255,255,255,0.07);
      --clr-gold:        #c9a84c;
      --clr-gold-light:  #e8cc82;
      --clr-gold-dim:    rgba(201,168,76,0.15);
      --clr-accent:      #7b4fff;
      --clr-accent-soft: rgba(123,79,255,0.18);
      --clr-text:        #e8e8f0;
      --clr-text-muted:  #888899;
      --clr-green:       #25d366;
      --clr-premium:     #b5892f;
      --clr-luxo:        #7b4fff;
      --radius-card:     16px;
      --radius-btn:      50px;
      --shadow-card:     0 8px 32px rgba(0,0,0,0.55);
      --shadow-glow:     0 0 24px rgba(201,168,76,0.18);
      --font-serif:      "Cormorant Garamond", Georgia, serif;
      --font-sans:       "Outfit", system-ui, sans-serif;
      --transition:      0.28s cubic-bezier(0.34,1.56,0.64,1);
    }}

    /* ══════════════════════════════════════════════
       RESET & BASE
    ══════════════════════════════════════════════ */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    html {{ scroll-behavior: smooth; }}

    body {{
      font-family: var(--font-sans);
      background: var(--clr-bg);
      color: var(--clr-text);
      min-height: 100vh;
      line-height: 1.6;
    }}

    img {{ max-width: 100%; display: block; }}
    a   {{ color: inherit; text-decoration: none; }}

    /* ══════════════════════════════════════════════
       ANIMATED BACKGROUND GRADIENT
    ══════════════════════════════════════════════ */
    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(123,79,255,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 90%, rgba(201,168,76,0.07) 0%, transparent 55%);
      pointer-events: none;
      z-index: 0;
    }}

    /* ══════════════════════════════════════════════
       HERO / HEADER
    ══════════════════════════════════════════════ */
    .hero {{
      position: relative;
      z-index: 1;
      text-align: center;
      padding: 4rem 1.5rem 2rem;
      border-bottom: 1px solid var(--clr-border);
      background: linear-gradient(180deg, rgba(201,168,76,0.06) 0%, transparent 100%);
    }}

    .hero-logo-line {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.75rem;
      margin-bottom: 0.5rem;
    }}

    .hero-logo-icon {{
      width: 48px;
      height: 48px;
      fill: var(--clr-gold);
      filter: drop-shadow(0 0 10px rgba(201,168,76,0.5));
    }}

    .hero-title {{
      font-family: var(--font-serif);
      font-size: clamp(2rem, 5vw, 3.5rem);
      font-weight: 600;
      letter-spacing: 0.05em;
      background: linear-gradient(135deg, var(--clr-gold) 0%, var(--clr-gold-light) 50%, var(--clr-gold) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      line-height: 1.15;
    }}

    .hero-subtitle {{
      font-size: 1rem;
      color: var(--clr-text-muted);
      margin-top: 0.4rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      font-weight: 300;
    }}

    .hero-divider {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 1rem;
      margin: 1.5rem auto;
      max-width: 320px;
    }}

    .hero-divider::before,
    .hero-divider::after {{
      content: "";
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--clr-gold), transparent);
    }}

    .hero-divider-gem {{
      width: 8px;
      height: 8px;
      background: var(--clr-gold);
      transform: rotate(45deg);
      box-shadow: 0 0 8px var(--clr-gold);
    }}

    .hero-contacts {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 0.75rem 1.5rem;
      margin-top: 1.25rem;
    }}

    .hero-contact-link {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.9rem;
      color: var(--clr-text-muted);
      transition: color 0.2s;
    }}

    .hero-contact-link:hover {{ color: var(--clr-gold); }}

    .hero-contact-link svg {{ flex-shrink: 0; }}

    /* ══════════════════════════════════════════════
       CONTROLS BAR (Search + Sort)
    ══════════════════════════════════════════════ */
    .controls {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(11,11,18,0.88);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border-bottom: 1px solid var(--clr-border);
      padding: 0.85rem 1.5rem;
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      align-items: center;
      justify-content: space-between;
    }}

    .search-wrap {{
      position: relative;
      flex: 1 1 220px;
      max-width: 420px;
    }}

    .search-wrap svg {{
      position: absolute;
      left: 0.9rem;
      top: 50%;
      transform: translateY(-50%);
      fill: var(--clr-text-muted);
      pointer-events: none;
    }}

    .search-input {{
      width: 100%;
      background: var(--clr-surface-2);
      border: 1px solid var(--clr-border);
      border-radius: var(--radius-btn);
      padding: 0.6rem 1rem 0.6rem 2.5rem;
      color: var(--clr-text);
      font-size: 0.9rem;
      font-family: var(--font-sans);
      outline: none;
      transition: border-color 0.2s;
    }}

    .search-input::placeholder {{ color: var(--clr-text-muted); }}
    .search-input:focus {{ border-color: var(--clr-gold); }}

    .sort-select {{
      background: var(--clr-surface-2);
      border: 1px solid var(--clr-border);
      border-radius: var(--radius-btn);
      padding: 0.6rem 1.1rem;
      color: var(--clr-text);
      font-family: var(--font-sans);
      font-size: 0.9rem;
      outline: none;
      cursor: pointer;
      transition: border-color 0.2s;
    }}

    .sort-select:focus {{ border-color: var(--clr-gold); }}

    .results-count {{
      font-size: 0.82rem;
      color: var(--clr-text-muted);
      white-space: nowrap;
    }}

    /* ══════════════════════════════════════════════
       GRID
    ══════════════════════════════════════════════ */
    .catalog-wrap {{
      position: relative;
      z-index: 1;
      max-width: 1440px;
      margin: 0 auto;
      padding: 2rem 1.25rem 4rem;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 1.5rem;
    }}

    .card-hidden {{ display: none !important; }}

    /* ══════════════════════════════════════════════
       CARD
    ══════════════════════════════════════════════ */
    .card {{
      background: var(--clr-surface);
      border: 1px solid var(--clr-border);
      border-radius: var(--radius-card);
      overflow: hidden;
      transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
      cursor: pointer;
    }}

    .card:hover {{
      transform: translateY(-6px) scale(1.015);
      box-shadow: var(--shadow-card), var(--shadow-glow);
      border-color: rgba(201,168,76,0.35);
    }}

    /* Image wrapper */
    .card-image-wrap {{
      position: relative;
      aspect-ratio: 1 / 1;
      overflow: hidden;
      background: var(--clr-surface-2);
    }}

    .card-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }}

    .card:hover .card-img {{ transform: scale(1.08); }}

    /* Overlay CTA */
    .card-overlay {{
      position: absolute;
      inset: 0;
      background: linear-gradient(0deg, rgba(0,0,0,0.75) 0%, transparent 55%);
      display: flex;
      align-items: flex-end;
      padding: 1rem;
      opacity: 0;
      transition: opacity 0.3s ease;
    }}

    .card:hover .card-overlay {{ opacity: 1; }}

    .btn-comprar {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: var(--clr-green);
      color: #fff;
      font-weight: 600;
      font-size: 0.85rem;
      padding: 0.55rem 1.1rem;
      border-radius: var(--radius-btn);
      width: 100%;
      justify-content: center;
      transition: background 0.2s, transform 0.18s;
    }}

    .btn-comprar:hover {{
      background: #1da851;
      transform: scale(1.03);
    }}

    /* Badge */
    .badge {{
      position: absolute;
      top: 0.75rem;
      right: 0.75rem;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.2rem 0.7rem;
      border-radius: var(--radius-btn);
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}

    .badge-premium {{
      background: var(--clr-gold-dim);
      color: var(--clr-gold);
      border: 1px solid rgba(201,168,76,0.4);
    }}

    .badge-luxo {{
      background: var(--clr-accent-soft);
      color: #b89cff;
      border: 1px solid rgba(123,79,255,0.35);
    }}

    /* Card info */
    .card-info {{
      padding: 0.95rem 1.1rem 1.15rem;
    }}

    .card-ref {{
      font-size: 0.73rem;
      color: var(--clr-gold);
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 0.25rem;
    }}

    .card-name {{
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--clr-text);
      line-height: 1.35;
      margin-bottom: 0.6rem;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .card-price {{
      font-family: var(--font-serif);
      font-size: 1.3rem;
      font-weight: 600;
      color: var(--clr-gold-light);
      letter-spacing: 0.02em;
    }}

    /* ══════════════════════════════════════════════
       EMPTY STATE
    ══════════════════════════════════════════════ */
    .no-results {{
      display: none;
      grid-column: 1 / -1;
      text-align: center;
      padding: 4rem 1rem;
      color: var(--clr-text-muted);
      font-size: 1.1rem;
    }}

    /* ══════════════════════════════════════════════
       FOOTER
    ══════════════════════════════════════════════ */
    .footer {{
      position: relative;
      z-index: 1;
      border-top: 1px solid var(--clr-border);
      background: var(--clr-surface);
      text-align: center;
      padding: 2rem 1.5rem;
      color: var(--clr-text-muted);
      font-size: 0.85rem;
    }}

    .footer strong {{ color: var(--clr-gold); }}

    /* ══════════════════════════════════════════════
       SCROLL-TO-TOP BUTTON
    ══════════════════════════════════════════════ */
    .scroll-top {{
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      z-index: 200;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: var(--clr-gold);
      color: #0b0b12;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 16px rgba(0,0,0,0.4);
      opacity: 0;
      transform: translateY(12px);
      transition: opacity 0.3s, transform 0.3s;
      pointer-events: none;
    }}

    .scroll-top.visible {{
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }}

    .scroll-top:hover {{ background: var(--clr-gold-light); }}

    /* ══════════════════════════════════════════════
       STATS BAR
    ══════════════════════════════════════════════ */
    .stats-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 1.5rem;
      padding: 1.25rem 1.5rem;
      background: var(--clr-surface);
      border-bottom: 1px solid var(--clr-border);
      position: relative;
      z-index: 1;
    }}

    .stat-item {{
      text-align: center;
    }}

    .stat-value {{
      font-family: var(--font-serif);
      font-size: 1.6rem;
      font-weight: 600;
      color: var(--clr-gold);
      line-height: 1;
    }}

    .stat-label {{
      font-size: 0.75rem;
      color: var(--clr-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-top: 0.15rem;
    }}

    /* ══════════════════════════════════════════════
       RESPONSIVE
    ══════════════════════════════════════════════ */
    @media (max-width: 640px) {{
      .hero {{ padding: 2.5rem 1rem 1.5rem; }}
      .controls {{ flex-direction: column; align-items: stretch; }}
      .search-wrap {{ max-width: 100%; }}
      .grid {{ grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; }}
      .card-name {{ font-size: 0.85rem; }}
      .card-price {{ font-size: 1.1rem; }}
    }}

    @media (min-width: 1200px) {{
      .grid {{ grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }}
    }}
  </style>
</head>
<body>

  <!-- ═══════════════════════ HERO ═══════════════════════ -->
  <header class="hero" role="banner">
    <div class="hero-logo-line">
      <!-- Crescent + star Islamic-inspired SVG icon -->
      <svg class="hero-logo-icon" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M32 4C16.536 4 4 16.536 4 32s12.536 28 28 28 28-12.536 28-28S47.464 4 32 4zm0 4c4.14 0 8.05.996 11.5 2.762C36.38 14.116 31 21.464 31 30c0 8.536 5.38 15.884 12.5 19.238A23.95 23.95 0 0132 52C18.745 52 8 41.255 8 28 8 14.745 18.745 4 32 4z" opacity=".5"/>
        <polygon points="46,8 47.5,12.5 52,14 47.5,15.5 46,20 44.5,15.5 40,14 44.5,12.5" />
      </svg>
      <h1 class="hero-title">{STORE["name"]}</h1>
    </div>
    <p class="hero-subtitle">Perfumes Árabes Importados Premium</p>

    <div class="hero-divider" aria-hidden="true">
      <div class="hero-divider-gem"></div>
    </div>

    <nav class="hero-contacts" aria-label="Contatos da loja">
      <!-- WhatsApp -->
      <a href="{STORE['whatsapp_link']}" target="_blank" rel="noopener" class="hero-contact-link" aria-label="WhatsApp">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347zM12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.118 1.528 5.846L.057 23.885l6.187-1.438A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.894a9.892 9.892 0 01-5.012-1.361l-.36-.214-3.733.867.934-3.613-.235-.373A9.868 9.868 0 012.106 12C2.106 6.533 6.533 2.106 12 2.106S21.894 6.533 21.894 12 17.467 21.894 12 21.894z"/>
        </svg>
        {STORE["whatsapp"]}
      </a>
      <!-- Instagram -->
      <a href="{STORE['instagram_link']}" target="_blank" rel="noopener" class="hero-contact-link" aria-label="Instagram">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
        </svg>
        {STORE["instagram"]}
      </a>
      <!-- Email -->
      <a href="mailto:{STORE['email']}" class="hero-contact-link" aria-label="E-mail">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
        </svg>
        {STORE["email"]}
      </a>
    </nav>
  </header>

  <!-- ═══════════════════════ STATS ═══════════════════════ -->
  <section class="stats-bar" aria-label="Estatísticas do catálogo">
    <div class="stat-item">
      <div class="stat-value" id="stat-total">{total_products}</div>
      <div class="stat-label">Produtos</div>
    </div>
    <div class="stat-item">
      <div class="stat-value" id="stat-visible">{total_products}</div>
      <div class="stat-label">Exibindo</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">{images_ok}</div>
      <div class="stat-label">Com Imagem</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">{images_missing}</div>
      <div class="stat-label">Sem Imagem</div>
    </div>
  </section>

  <!-- ═══════════════════════ CONTROLS ═══════════════════════ -->
  <div class="controls" role="search">
    <div class="search-wrap">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
        <path d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
      </svg>
      <input
        type="search"
        id="search-input"
        class="search-input"
        placeholder="Buscar por nome ou referência…"
        aria-label="Buscar produto"
        autocomplete="off"
      />
    </div>

    <select id="sort-select" class="sort-select" aria-label="Ordenar por">
      <option value="default">Ordenar: Padrão</option>
      <option value="name-asc">Nome A → Z</option>
      <option value="name-desc">Nome Z → A</option>
      <option value="price-asc">Preço: Menor → Maior</option>
      <option value="price-desc">Preço: Maior → Menor</option>
      <option value="ref-asc">Referência ↑</option>
    </select>

    <span class="results-count" id="results-count" aria-live="polite">{total_products} produtos</span>
  </div>

  <!-- ═══════════════════════ CATALOG GRID ═══════════════════════ -->
  <main class="catalog-wrap" id="catalog" aria-label="Catálogo de perfumes">
    <div class="grid" id="product-grid" role="list">
      {cards_joined}
      <p class="no-results" id="no-results" role="status">
        Nenhum produto encontrado para "<span id="search-term-display"></span>".
      </p>
    </div>
  </main>

  <!-- ═══════════════════════ FOOTER ═══════════════════════ -->
  <footer class="footer" role="contentinfo">
    <p>
      © 2025 <strong>{STORE["name"]}</strong> — Todos os direitos reservados.<br />
      <small>Imagens meramente ilustrativas. Preços sujeitos a alteração sem aviso prévio.</small>
    </p>
  </footer>

  <!-- ═══════════════════════ SCROLL-TO-TOP ═══════════════════════ -->
  <button class="scroll-top" id="scroll-top" aria-label="Voltar ao topo" title="Voltar ao topo">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M18 15l-6-6-6 6"/>
    </svg>
  </button>

  <!-- ═══════════════════════ JAVASCRIPT ═══════════════════════ -->
  <script>
    (() => {{
      const grid       = document.getElementById('product-grid');
      const cards      = Array.from(grid.querySelectorAll('.card'));
      const searchInp  = document.getElementById('search-input');
      const sortSel    = document.getElementById('sort-select');
      const countEl    = document.getElementById('results-count');
      const visibleEl  = document.getElementById('stat-visible');
      const noResults  = document.getElementById('no-results');
      const termEl     = document.getElementById('search-term-display');
      const scrollBtn  = document.getElementById('scroll-top');

      // ── Save original DOM order ─────────────────────────────────
      const originalOrder = cards.map((c, i) => ({{ card: c, index: i }}));

      // ── Filter & Sort ───────────────────────────────────────────
      function applyFilters() {{
        const q    = searchInp.value.trim().toLowerCase();
        const sort = sortSel.value;

        let filtered = cards.filter(c => {{
          if (!q) return true;
          return c.dataset.name.includes(q) || c.dataset.ref.includes(q);
        }});

        // Sort
        const sorters = {{
          'name-asc':   (a, b) => a.dataset.name.localeCompare(b.dataset.name),
          'name-desc':  (a, b) => b.dataset.name.localeCompare(a.dataset.name),
          'price-asc':  (a, b) => +a.dataset.price - +b.dataset.price,
          'price-desc': (a, b) => +b.dataset.price - +a.dataset.price,
          'ref-asc':    (a, b) => +a.dataset.ref - +b.dataset.ref,
          'default':    (a, b) => originalOrder.find(o=>o.card===a).index - originalOrder.find(o=>o.card===b).index,
        }};

        if (sorters[sort]) filtered.sort(sorters[sort]);

        // Hide all, then show filtered in sorted order
        cards.forEach(c => {{ c.classList.add('card-hidden'); c.remove(); }});
        filtered.forEach(c => {{ c.classList.remove('card-hidden'); grid.appendChild(c); }});

        // Update counts
        const vis = filtered.length;
        countEl.textContent = vis + ' produto' + (vis !== 1 ? 's' : '');
        visibleEl.textContent = vis;

        // No-results message
        if (vis === 0) {{
          termEl.textContent = q;
          noResults.style.display = 'block';
          grid.appendChild(noResults);
        }} else {{
          noResults.style.display = 'none';
        }}
      }}

      searchInp.addEventListener('input', applyFilters);
      sortSel.addEventListener('change', applyFilters);

      // ── Scroll-to-top button ────────────────────────────────────
      window.addEventListener('scroll', () => {{
        if (window.scrollY > 400) {{
          scrollBtn.classList.add('visible');
        }} else {{
          scrollBtn.classList.remove('visible');
        }}
      }}, {{ passive: true }});

      scrollBtn.addEventListener('click', () => {{
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }});

      // ── Card click → opens WhatsApp ─────────────────────────────
      cards.forEach(card => {{
        card.addEventListener('click', (e) => {{
          // Only if not clicking the CTA button itself
          if (!e.target.closest('.btn-comprar')) {{
            const btn = card.querySelector('.btn-comprar');
            if (btn) btn.click();
          }}
        }});
        card.setAttribute('role', 'listitem');
      }});
    }})();
  </script>
</body>
</html>"""

    CATALOG_FILE.write_text(html, encoding="utf-8")
    log.info("✓ Catalog saved → %s  (%d products)", CATALOG_FILE, total_products)


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 65)
    log.info("  RODRIGO IMPORTADOS ÁRABES — Image Scraper & Catalog Builder")
    log.info("=" * 65)
    log.info("Products : %d", len(PRODUCTS))
    log.info("Output   : %s", OUTPUT_DIR.resolve())
    log.info("Catalog  : %s", CATALOG_FILE.resolve())
    log.info("-" * 65)

    # Verify dependencies
    try:
        import bs4   # noqa: F401
    except ImportError:
        log.error("Missing dependency: beautifulsoup4 — run:  pip install requests beautifulsoup4")
        raise SystemExit(1)

    results = run_scraper()

    # Summary
    ok  = sum(1 for v in results.values() if v)
    fail = len(results) - ok
    log.info("=" * 65)
    log.info("DONE  ✓ %d images downloaded  |  ✗ %d failed", ok, fail)
    log.info("=" * 65)

    # Always generate catalog (even with partial images)
    generate_catalog(results)

    if fail:
        log.warning("Products without image (check manually):")
        for ref, name, _ in PRODUCTS:
            if not results.get(ref):
                log.warning("  • ref_%s — %s", ref, name)


if __name__ == "__main__":
    main()
