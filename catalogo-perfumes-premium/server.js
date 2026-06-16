const express = require('express');
const path = require('path');
const helmet = require('helmet');
const cors = require('cors');
require('dotenv').config();

const ProductController = require('./src/controllers/ProductController');

const app = express();
const PORT = process.env.PORT || 3000;

// Hardening de Segurança
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      styleSrc: ["'self'", "https://fonts.googleapis.com", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      scriptSrcAttr: ["'unsafe-inline'"],
      connectSrc: ["'self'", "https://wa.me"],
    }
  }
}));

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Arquivos estáticos
app.use(express.static(path.join(__dirname, 'public')));

// View engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'src', 'views'));

// Rotas
app.get('/', ProductController.getHome);
app.get('/quiz', ProductController.getQuiz);
app.get('/catalogo', ProductController.getCatalog);
app.get('/perfume/:slug', ProductController.getProductBySlug);
app.get('/perfumes-parecidos-com-:famosoSlug', ProductController.getSEOComparison);
app.post('/api/recomendacoes', ProductController.postRecomendacoes);

// 404 Fallback
app.use((req, res) => {
  res.status(404).render('404', {
    meta: { title: 'Página não encontrada | Neide Perfumes Importados', description: '' },
    config: { whatsapp_contato: '5567996962426', nome_marca: 'Neide Perfumes Importados' }
  });
});

app.listen(PORT, () => {
  console.log(`[Neide Perfumes] Servidor rodando em http://localhost:${PORT}`);
});