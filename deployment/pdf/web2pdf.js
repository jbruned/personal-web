const puppeteer = require('puppeteer');

// Serve the web
rand_port = Math.floor(Math.random() * 10000) + 10000;
console.log(`Serving the web on port ${rand_port}...`);
const express = require('express');
const app = express();
app.use(express.static(__dirname.replace("/deployment/pdf", "")));
app.listen(rand_port);

(async () => {
    // Delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Print the page as PDF
    console.log("Initializing puppeteer...");
    const browser = await puppeteer.launch({headless: "new"});
    const page = await browser.newPage();
    page.setViewport({width: 1280, height: 1280});

    console.log("Loading page...");
    await page.goto(
        //"file://" + __dirname.replace("/deployment/pdf", "") + "/index.html",
        `http://localhost:${rand_port}#print`,
        {waitUntil: 'networkidle2'}
    );

    // Delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    console.log("Rendering PDF...");
    await page.pdf({
        path: '../../CV_Jorge_Bruned.pdf',
        format: 'A4',
        //margin: 0,
        printBackground: true,
        displayHeaderFooter: false,
        scale: 0.7,
        //preferCSSPageSize: true
    });

    console.log("Wrapping up...");
    await browser.close();

    // Exit
    process.exit(0);
})();