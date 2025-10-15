// # --------------------------------------------------------------------------------
// # AUTO SCRAPING ON BROWSER ONCE PASTED ON CONSOLE IT STARTS SCROLLING AND SCRAPE ALL THE REVIEWS
// # --------------------------------------------------------------------------------

(async () => {
    // Wait for reviews to appear
    while (!document.querySelector('[data-review-id], .jftiEf')) {
        console.log("Waiting for reviews to load...");
        await new Promise(r => setTimeout(r, 1000));
    }

    // Optional: Click "Sort" → "Newest"
    try {
        let sortButton = document.querySelector('button[jsaction*="sort"]') || 
                         [...document.querySelectorAll('button')].find(b => /sort|排序|クラス/i.test(b.innerText));
        if (sortButton && sortButton.offsetParent !== null) {
            sortButton.click();
            await new Promise(r => setTimeout(r, 1500));
            let newestOption = [...document.querySelectorAll('li, div, span')].find(el => 
                /newest|最新|neueste|plus récent/i.test(el.innerText)
            );
            if (newestOption) {
                newestOption.click();
                await new Promise(r => setTimeout(r, 3000)); // Let reviews reload
            }
        }
    } catch (e) {
        console.warn("Couldn't auto-sort by newest.", e);
    }

    // Find scroll container
    const containerSelectors = [
        '.m6QErb.DxyBCb.kA9KIf.dS8AEf',
        '.review-dialog-list',
        '[role="main"]'
    ];
    let scrollContainer = containerSelectors
        .map(sel => document.querySelector(sel))
        .find(el => el) || window;

    const capturedReviews = new Map();
    let stalledAttempts = 0;
    const MAX_STALL_ATTEMPTS = 5;

    // Expand "More" buttons
    const expandMoreButtons = () => {
        document.querySelectorAll('button.w8nwRe, button[aria-label*="More"], button[aria-label*="mehr"], button[aria-label*="更多"]')
            .forEach(btn => {
                if (btn.offsetHeight > 0 && getComputedStyle(btn).visibility !== 'hidden') {
                    btn.click();
                }
            });
    };

    // Start scrolling & capturing
    console.log("🚀 Starting to load all reviews...");

    return new Promise((resolve) => {
        const intervalId = setInterval(() => {
            expandMoreButtons();

            let foundNew = false;
            const reviews = document.querySelectorAll('[data-review-id], .jftiEf');

            for (const review of reviews) {
                const id = review.getAttribute('data-review-id') ||
                          review.getAttribute('data-id') ||
                          review.id ||
                          Array.from(review.classList).join(' ');

                if (!id || capturedReviews.has(id)) continue;

                const textEl = review.querySelector('.wiI7pd') ||
                               review.querySelector('[data-expandable-section]') ||
                               review.querySelector('.MyEned');
                const text = textEl?.innerText?.trim();
                if (!text) continue;

                const rating = review.querySelector('[role="img"]')?.getAttribute('aria-label') || '';
                const author = review.querySelector('.d4r55')?.innerText || '';
                const date = review.querySelector('.rsqaWe')?.innerText || '';

                capturedReviews.set(id, { text: text.replace(/"/g, '""'), rating, author, date });
                foundNew = true;
            }

            // Scroll
            if (scrollContainer === window) {
                window.scrollTo(0, document.body.scrollHeight);
            } else {
                scrollContainer.scrollTop = scrollContainer.scrollHeight;
            }

            console.log(`✅ Captured ${capturedReviews.size} unique reviews so far...`);

            if (!foundNew) {
                stalledAttempts++;
                if (stalledAttempts >= MAX_STALL_ATTEMPTS) {
                    clearInterval(intervalId);
                    console.log(`🎉 Done! Total reviews captured: ${capturedReviews.size}`);
                    resolve(Array.from(capturedReviews.values()));
                }
            } else {
                stalledAttempts = 0;
            }
        }, 2500); // 2.5s delay — safe for most connections
    }).then(reviews => {
        // Export as CSV
        const headers = ['Author', 'Rating', 'Date', 'Review'];
        const rows = reviews.map(r => `"${r.author}","${r.rating}","${r.date}","${r.text}"`);
        const csvContent = [headers.join(','), ...rows].join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'google_maps_reviews.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        console.log("📁 CSV file downloaded!");
    }).catch(err => {
        console.error("❌ Error:", err);
    });
})();