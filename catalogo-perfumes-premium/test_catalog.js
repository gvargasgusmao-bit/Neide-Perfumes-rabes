const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const ejs = require('ejs');
const path = require('path');

const db = require('./src/data/db.json');
const htmlTemplate = fs.readFileSync(path.join(__dirname, 'src/views/catalog.ejs'), 'utf8');

const renderedHtml = ejs.render(htmlTemplate, {
  perfumes: db.perfumes,
  marcas: db.marcas,
  config: db.configuracoes,
  filtros: {},
  filename: path.join(__dirname, 'src/views/catalog.ejs') // needed for includes
});

const dom = new JSDOM(renderedHtml, { runScripts: "dangerously" });
const window = dom.window;

try {
  console.log("Testing catalog.js filters...");
  
  // Try calling aplicarFiltros directly
  if (typeof window.aplicarFiltros === 'function') {
    window.aplicarFiltros();
    console.log("aplicarFiltros executed without errors.");
    
    // Select a checkbox and trigger change
    const checkbox = window.document.querySelector('input[name="genero"][value="masculino"]');
    if (checkbox) {
      checkbox.checked = true;
      checkbox.dispatchEvent(new window.Event('change'));
      console.log("aplicarFiltros executed on change event.");
    } else {
      console.log("Checkbox not found.");
    }
  } else {
    console.log("aplicarFiltros function not found in global scope.");
  }
} catch (e) {
  console.error("Error during execution:", e);
}
