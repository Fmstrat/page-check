const puppeteer = require('puppeteer');
const Common = require('./common');
const Pushover = require('node-pushover');

let checks = JSON.parse(process.env.CHECKS);
let pushoverApi = process.env.PUSHOVERAPI;
let pushoverUser = process.env.PUSHOVERUSER;
let intervalMin = process.env.INTERVALMIN;
let smtpServer = process.env.SMTPSERVER;
let smtpFrom = process.env.SMTPFROM;
let smtpTo = process.env.SMTPTO;

let page;
const push = new Pushover({
	token: pushoverApi,
	user: pushoverUser
});

async function checkPage(check) {
    try {
        let c = new Common();
        await page.goto(check.url);
        let web = await c.getPage(page);
        if (check.reverse) {
            console.log(`Checking if "${check.url}" does not include "${check.string}":`)
            if (!web.body.includes(check.string)) {
                console.log("  String is missing now - Sending Pushover")
                check.alerted = true;
                push.send("Page Check", check.url);
            } else {
                console.log("  String exists")
            }
        } else {
            console.log(`Checking if "${check.url}" includes "${check.string}":`)
            if (!web.body.includes(check.string)) {
                console.log("  String does not exist")
            } else {
                console.log("  String was found - Sending Pushover")
                check.alerted = true;
                push.send("Page Check", check.url);
            }
        }
    } catch (e) {
        console.log(e);
    }
}

async function main() {
    let c = new Common();
    let browser = await puppeteer.launch({
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage'
        ]
    })
    page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36");
    await page.setViewport({
        width: 1920,
        height: 1080,
        deviceScaleFactor: 1,
    });
    for (let x = 0; x < checks.length; x++) {
        checks[x].alerted = false;
    }
    while (true) {
        for (let x = 0; x < checks.length; x++) {
            if (!checks[x].alerted)
                await checkPage(checks[x]);
        }
        console.log(`Sleeping ${intervalMin} minutes`)
        await c.sleep(intervalMin*60*1000);
    }
}

main();


