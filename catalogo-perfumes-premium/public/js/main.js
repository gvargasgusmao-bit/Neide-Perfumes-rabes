/* ============================================================
   NEIDE PERFUMES IMPORTADOS — main.js
   Funcionalidades globais: Navbar, Animações, WhatsApp
   ============================================================ */

(function () {
  'use strict';

  // ============================================================
  // NAVBAR — Scroll behavior
  // ============================================================
  const navbar = document.getElementById('navbar');

  if (navbar) {
    // Scroll behavior removido, navbar é sempre sólida
    // Marca link ativo
    const path = window.location.pathname;
    document.querySelectorAll('.navbar-link').forEach(link => {
      const href = link.getAttribute('href');
      if (href === path || (href !== '/' && path.startsWith(href))) {
        link.classList.add('ativo');
      }
    });
  }

  // ============================================================
  // HAMBURGER — Menu mobile
  // ============================================================
  const hamburger = document.getElementById('navbar-hamburger');
  const menuMobile = document.getElementById('navbar-mobile');

  if (hamburger && menuMobile) {
    hamburger.addEventListener('click', () => {
      const aberto = hamburger.classList.toggle('aberto');
      menuMobile.classList.toggle('aberto', aberto);
      hamburger.setAttribute('aria-expanded', aberto.toString());
    });

    // Fechar ao clicar em link
    menuMobile.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('aberto');
        menuMobile.classList.remove('aberto');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });

    // Fechar ao clicar fora
    document.addEventListener('click', (e) => {
      if (!hamburger.contains(e.target) && !menuMobile.contains(e.target)) {
        hamburger.classList.remove('aberto');
        menuMobile.classList.remove('aberto');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ============================================================
  // INTERSECTION OBSERVER — Animações de entrada
  // ============================================================
  const observerConfig = {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  };

  const animarEntrada = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visivel');
        animarEntrada.unobserve(entry.target);
      }
    });
  }, observerConfig);

  document.querySelectorAll('.animar-entrada').forEach(el => {
    animarEntrada.observe(el);
  });

  // ============================================================
  // QUIZ PREVIEW — Animação dos passos
  // ============================================================
  const passos = document.querySelectorAll('.quiz-preview-passo');
  if (passos.length > 0) {
    let passoAtual = 0;
    setInterval(() => {
      passos[passoAtual].classList.remove('ativo');
      passoAtual = (passoAtual + 1) % passos.length;
      passos[passoAtual].classList.add('ativo');
    }, 1500);
  }

  // ============================================================
  // LAZY LOAD — Imagens
  // ============================================================
  if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    const lazyObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          lazyObserver.unobserve(img);
        }
      });
    });
    lazyImages.forEach(img => lazyObserver.observe(img));
  }

  // ============================================================
  // SMOOTH SCROLL — Links internos
  // ============================================================
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const alvo = document.querySelector(link.getAttribute('href'));
      if (alvo) {
        e.preventDefault();
        alvo.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ============================================================
  // MÉTRICAS — Animação das barras de produto
  // ============================================================
  const barras = document.querySelectorAll('.produto-metrica-fill, .metrica-barra-fill');
  const barraObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.transition = 'width 1s cubic-bezier(0.4, 0, 0.2, 1)';
        barraObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  barras.forEach(barra => barraObserver.observe(barra));

  // ============================================================
  // LOG de inicialização
  // ============================================================
  console.log('%c🌹 Neide Perfumes Importados', 'color:#C9A84C;font-size:16px;font-weight:bold;');
  console.log('%cPerfumes Árabes Originais • Envio para todo o Brasil', 'color:#999;font-size:12px;');

})();
