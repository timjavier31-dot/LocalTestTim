const puppeteer = require('puppeteer');
const path      = require('path');
const fs        = require('fs');

const BASE_URL       = 'http://testsite.local';
const SCREENSHOTS_DIR = path.join(__dirname, 'wp-content', 'screenshots');

const PAGES = [
    {
        name  : 'home',
        url   : '/',
        title : 'Homepage',
    },
    {
        name  : 'multiplication',
        url   : '/?page=topic&topic=multiplication',
        title : 'Multiplication Topic',
    },
    {
        name  : 'division',
        url   : '/?page=topic&topic=division',
        title : 'Division Topic',
    },
    {
        name  : 'fractions',
        url   : '/?page=topic&topic=fractions',
        title : 'Fractions Topic',
    },
    {
        name  : 'practice',
        url   : '/?page=practice',
        title : 'Practice Problems',
    },
    {
        name  : 'quiz',
        url   : '/?page=quiz',
        title : 'Quiz Page',
    },
    {
        name  : 'easy-level',
        url   : '/easy-level/',
        title : 'Easy Level Page',
    },
];

async function run() {
    if ( ! fs.existsSync( SCREENSHOTS_DIR ) ) {
        fs.mkdirSync( SCREENSHOTS_DIR, { recursive: true } );
    }

    console.log( '🚀 Launching browser...\n' );

    const browser = await puppeteer.launch( {
        headless : true,
        args     : [ '--no-sandbox', '--disable-setuid-sandbox' ],
    } );

    for ( const page of PAGES ) {
        const tab = await browser.newPage();
        await tab.setViewport( { width: 1280, height: 900 } );

        try {
            console.log( `📸 Capturing: ${ page.title }...` );
            await tab.goto( BASE_URL + page.url, {
                waitUntil : 'networkidle2',
                timeout   : 20000,
            } );

            /* slight delay so JS-rendered content (practice/quiz) loads */
            await new Promise( r => setTimeout( r, 1000 ) );

            const filePath = path.join( SCREENSHOTS_DIR, `${ page.name }.png` );
            await tab.screenshot( { path: filePath, fullPage: true } );
            console.log( `   ✅ Saved → wp-content/screenshots/${ page.name }.png` );
        } catch ( err ) {
            console.error( `   ❌ Failed: ${ page.title } — ${ err.message }` );
        }

        await tab.close();
    }

    await browser.close();
    console.log( '\n🎉 Done! All screenshots saved to wp-content/screenshots/' );
    console.log( '   Now run: git add wp-content/screenshots/ && git commit -m "Add screenshots" && git push' );
}

run();
