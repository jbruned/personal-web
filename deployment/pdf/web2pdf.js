const puppeteer = require('puppeteer');

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
    await page.pdf({
        path: `../../CV_Jorge_Bruned${lang != null ? `_${lang.toUpperCase()}` : ''}.pdf`,
        format: 'A4',
        // margin: 0,
        printBackground: true,
        displayHeaderFooter: false,
        scale: 0.7,
        // preferCSSPageSize: true
    });

    console.log("Wrapping up...");
    await browser.close();

    // Exit
    process.exit(0);
})();