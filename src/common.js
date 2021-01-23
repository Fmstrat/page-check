class Common {

	assert(test, bool) {
		if (bool) 
			console.log(`  Success: ${test}`);
		else
			console.log(`  -=- FAIL -=- : ${test}`);
		return bool;
	}

	announce(title) {
		console.log(`Browser: ${title}`);
	}

	async getPage(page) {
		await this.sleep(500);
		return {
			title: await page.title(),
			body: await page.evaluate(() => document.body.innerHTML)
		}
	}

	capitalizeFirst(str) { 
		return str[0].toUpperCase() + str.slice(1); 
	}

	async sleep(ms) {
		return new Promise(resolve => setTimeout(resolve, ms));
	}

}

module.exports = Common;