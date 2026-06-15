const fs = require('fs');
const path = require('path');
const tesseract = require('tesseract.js');

const imagesDir = path.join(__dirname, 'public', 'assets', 'images', 'perfumes');
const files = fs.readdirSync(imagesDir).filter(f => f.endsWith('.jpeg') || f.endsWith('.jpg') || f.endsWith('.png'));

async function processImages() {
  console.log(`Processing ${files.length} images...`);
  const results = [];
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    console.log(`[${i+1}/${files.length}] OCR on ${file}...`);
    try {
      const { data: { text } } = await tesseract.recognize(
        path.join(imagesDir, file),
        'eng',
        { logger: m => {} }
      );
      // Clean up text
      const cleanText = text.replace(/\n/g, ' ').trim();
      results.push({ file, text: cleanText });
      console.log(`   -> ${cleanText.substring(0, 100)}`);
    } catch (e) {
      console.log(`   -> ERROR`);
    }
  }
  
  fs.writeFileSync('ocr_results.json', JSON.stringify(results, null, 2));
  console.log('Done!');
}

processImages();
