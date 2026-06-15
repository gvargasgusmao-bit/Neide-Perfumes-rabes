const express = require('express');
const router = express.Router();
const ProductController = require('../controllers/ProductController');

// ============================================================
// ROTAS PÚBLICAS
// ============================================================

// Home
router.get('/', ProductController.getHome);

// Quiz (página)
router.get('/quiz', ProductController.getQuiz);

// Catálogo (com filtros via query params)
router.get('/catalogo', ProductController.getCatalog);

// Página individual de produto
router.get('/perfume/:slug', ProductController.getProductBySlug);

// ============================================================
// API — Recomendações (POST — usado pelo quiz)
// ============================================================
router.post('/api/recomendacoes', ProductController.postRecomendacoes);

module.exports = router;