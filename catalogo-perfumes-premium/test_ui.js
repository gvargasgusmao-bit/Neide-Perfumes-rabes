const puppeteer = require('puppeteer');

(async () => {
  console.log("Starting Puppeteer...");
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  // Capture console messages
  page.on('console', msg => {
    if (msg.type() === 'error' || msg.type() === 'warning') {
      console.log(`BROWSER ${msg.type().toUpperCase()}: ${msg.text()}`);
    }
  });

  page.on('pageerror', err => {
    console.log(`BROWSER PAGE ERROR: ${err.message}`);
  });

  try {
    console.log("Testing /catalogo ...");
    await page.goto('http://localhost:3000/catalogo', { waitUntil: 'networkidle0' });
    
    // Simulate checking a checkbox
    await page.evaluate(() => {
      const cb = document.querySelector('input[name="genero"][value="masculino"]');
      if (cb) {
        cb.checked = true;
        // Trigger change event since puppeteer click might bypass it if it's hidden
        const event = new Event('change', { bubbles: true });
        cb.dispatchEvent(event);
      }
    });

    await new Promise(r => setTimeout(r, 1000));
    
    console.log("Testing /quiz ...");
    await page.goto('http://localhost:3000/quiz', { waitUntil: 'networkidle0' });
    
    await page.evaluate(async () => {
      // Click first option
      document.querySelector('.quiz-opcao[data-valor="masculino"]').click();
      document.querySelector('#prox-1').click();
      
      document.querySelector('.quiz-opcao[data-valor="moderada"]').click();
      document.querySelector('#prox-2').click();
      
      document.querySelector('.quiz-opcao[data-valor="elegante"]').click();
      document.querySelector('#prox-3').click();
      
      document.querySelector('.quiz-opcao[data-valor="trabalho"]').click();
      document.querySelector('#prox-4').click();
      
      document.querySelector('.quiz-opcao[data-valor="amadeirada"]').click();
      document.querySelector('#prox-5').click();
      
      document.querySelector('.quiz-opcao[data-valor="ate_350"]').click();
      document.querySelector('#prox-6').click();
      
      document.querySelector('#btn-enviar-quiz').click();
    });

    await new Promise(r => setTimeout(r, 3000));
    console.log("Tests completed.");

  } catch (err) {
    console.error("Test execution failed:", err);
  } finally {
    await browser.close();
  }
})();
