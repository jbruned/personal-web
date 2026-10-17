const puppeteer = require('puppeteer');
const fs = require('fs');

// The print layout (assets/print.css) is designed to fit exactly two A4 pages
const EXPECTED_PAGES = 2;

// Serve the web
rand_port = Math.floor(Math.random() * 10000) + 10000;
console.log(`Serving the web on port ${rand_port}...`);
const express = require('express');
const app = express();
app.use(express.static(__dirname.replace("/deployment/pdf", "")));
app.listen(rand_port);

// Get the lang from the command line arguments
const lang = process.argv.length === 3 ? process.argv[2] : null;

async function sleep(millis) {
    await new Promise(resolve => setTimeout(resolve, millis));
}

(async () => {
    // Delay
    await sleep(1000);

    // Print the page as PDF
    console.log("Initializing puppeteer...");
    const browser = await puppeteer.launch({
        headless: true, // Legacy (new headless mode times out in GitHub actions)
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    page.setViewport({width: 1280, height: 1280});

    console.log("Loading page...");
    await page.goto(
        `http://localhost:${rand_port}${lang != null ? `?lang=${lang}` : ''}#print`,
        {waitUntil: 'networkidle2'}
    );

    // Delay
    await sleep(1000);

    console.log("Rendering PDF...");
    const pdf_path = `../../CV_Jorge_Bruned${lang != null ? `_${lang.toUpperCase()}` : ''}.pdf`;
    const pdf = await page.pdf({
        path: pdf_path,
        format: 'A4',
        printBackground: true,
        displayHeaderFooter: false,
        preferCSSPageSize: true // Page size and margins are defined in print.css (@page)
    });

    // Fail (so the job does not publish a broken CV) if the content no longer fits the expected pages
    const pages = (pdf.toString('latin1').match(/\/Type\s*\/Page(?![a-z])/g) || []).length;
    if (pages !== EXPECTED_PAGES) {
        console.error(`ERROR: the PDF has ${pages} pages instead of ${EXPECTED_PAGES}. Shorten the content or adjust assets/print.css.`);
        fs.unlinkSync(pdf_path);
        await browser.close();
        process.exit(1);
    }

    console.log("Wrapping up...");
    await browser.close();

    // Exit
    process.exit(0);
})();