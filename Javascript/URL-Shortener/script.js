class URLShortener {
    constructor() {
        this.urlStorage = this.loadFromStorage();
        this.baseUrl = window.location.origin + window.location.pathname;
        this.initializeElements();
        this.bindEvents();
        this.displayRecentUrls();
    }

    initializeElements() {
        this.urlInput = document.getElementById('urlInput');
        this.shortenBtn = document.getElementById('shortenBtn');
        this.result = document.getElementById('result');
        this.shortUrl = document.getElementById('shortUrl');
        this.originalUrl = document.getElementById('originalUrl');
        this.copyBtn = document.getElementById('copyBtn');
        this.error = document.getElementById('error');
        this.urlList = document.getElementById('urlList');
    }

    bindEvents() {
        this.shortenBtn.addEventListener('click', () => this.shortenUrl());
        this.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.shortenUrl();
        });
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    generateShortCode() {
        // Generate a random 6-character code
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < 6; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    shortenUrl() {
        const longUrl = this.urlInput.value.trim();
        
        // Hide previous results
        this.result.style.display = 'none';
        this.error.style.display = 'none';

        if (!longUrl) {
            this.showError('Please enter a URL');
            return;
        }

        if (!this.isValidUrl(longUrl)) {
            this.showError('Please enter a valid URL');
            return;
        }

        // Check if URL already exists
        const existingEntry = this.findExistingUrl(longUrl);
        if (existingEntry) {
            this.displayResult(existingEntry.shortCode, longUrl);
            return;
        }

        // Generate new short code
        let shortCode;
        do {
            shortCode = this.generateShortCode();
        } while (this.urlStorage[shortCode]); // Ensure uniqueness

        // Store the URL
        this.urlStorage[shortCode] = {
            originalUrl: longUrl,
            createdAt: new Date().toISOString(),
            clickCount: 0
        };

        this.saveToStorage();
        this.displayResult(shortCode, longUrl);
        this.displayRecentUrls();
    }

    findExistingUrl(url) {
        for (const [code, data] of Object.entries(this.urlStorage)) {
            if (data.originalUrl === url) {
                return { shortCode: code, ...data };
            }
        }
        return null;
    }

    displayResult(shortCode, originalUrl) {
        const shortUrl = `${this.baseUrl}#${shortCode}`;
        this.shortUrl.value = shortUrl;
        this.originalUrl.textContent = originalUrl;
        this.result.style.display = 'block';
        this.urlInput.value = '';
    }

    showError(message) {
        this.error.querySelector('p').textContent = message;
        this.error.style.display = 'block';
    }

    copyToClipboard() {
        this.shortUrl.select();
        this.shortUrl.setSelectionRange(0, 99999); // For mobile devices
        document.execCommand('copy');
        
        // Visual feedback
        const originalText = this.copyBtn.textContent;
        this.copyBtn.textContent = 'Copied!';
        this.copyBtn.style.backgroundColor = '#28a745';
        
        setTimeout(() => {
            this.copyBtn.textContent = originalText;
            this.copyBtn.style.backgroundColor = '';
        }, 2000);
    }

    displayRecentUrls() {
        const entries = Object.entries(this.urlStorage)
            .sort((a, b) => new Date(b[1].createdAt) - new Date(a[1].createdAt))
            .slice(0, 10); // Show only last 10

        if (entries.length === 0) {
            this.urlList.innerHTML = '<p class="no-urls">No URLs shortened yet</p>';
            return;
        }

        this.urlList.innerHTML = entries.map(([code, data]) => `
            <div class="url-item">
                <div class="url-info">
                    <div class="short-url">
                        <a href="${this.baseUrl}#${code}" target="_blank">${this.baseUrl}#${code}</a>
                    </div>
                    <div class="original-url">${data.originalUrl}</div>
                    <div class="url-meta">
                        Created: ${new Date(data.createdAt).toLocaleDateString()} | 
                        Clicks: ${data.clickCount}
                    </div>
                </div>
                <button class="delete-btn" onclick="urlShortener.deleteUrl('${code}')">Delete</button>
            </div>
        `).join('');
    }

    deleteUrl(shortCode) {
        if (confirm('Are you sure you want to delete this URL?')) {
            delete this.urlStorage[shortCode];
            this.saveToStorage();
            this.displayRecentUrls();
        }
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem('urlShortener');
            return stored ? JSON.parse(stored) : {};
        } catch (e) {
            console.error('Error loading from storage:', e);
            return {};
        }
    }

    saveToStorage() {
        try {
            localStorage.setItem('urlShortener', JSON.stringify(this.urlStorage));
        } catch (e) {
            console.error('Error saving to storage:', e);
        }
    }

    // Handle URL redirection
    handleRedirect() {
        const hash = window.location.hash.substring(1);
        if (hash && this.urlStorage[hash]) {
            // Increment click count
            this.urlStorage[hash].clickCount++;
            this.saveToStorage();
            
            // Redirect to original URL
            window.location.href = this.urlStorage[hash].originalUrl;
        }
    }
}

// Initialize the URL shortener
const urlShortener = new URLShortener();

// Handle page load for redirects
window.addEventListener('load', () => {
    urlShortener.handleRedirect();
});

// Handle hash changes
window.addEventListener('hashchange', () => {
    urlShortener.handleRedirect();
});
