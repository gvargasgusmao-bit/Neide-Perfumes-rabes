const express = require('express');
const path = require('path');
const helmet = require('helmet');
const cors = require('cors');
require('dotenv').config();

const routes = require('./src/routes/index');

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
app.use('/', routes);

// 404 Fallback
app.use((req, res) => {
  res.status(404).render('404', {
    meta: { title: 'Página não encontrada | Neide Perfumes Importados', description: '' },
    config: { whatsapp_contato: '5567996962426', nome_marca: 'Neide Perfumes Importados' }
  });
});

// Iniciar o servidor (Necessário para o Render)
app.listen(PORT, () => {
  console.log(`[Neide Perfumes] Servidor rodando na porta ${PORT}`);
});

// Export the app for Vercel Serverless
module.exports = app;