# 🔗 URL Shortener

A simple, client-side URL shortener built with vanilla JavaScript, HTML, and CSS. No server required!

## ✨ Features

- **URL Validation** - Validates URLs before shortening
- **Short Code Generation** - Creates unique 6-character codes
- **Local Storage** - Persists URLs in browser storage
- **Click Tracking** - Counts URL access statistics
- **Copy to Clipboard** - One-click copying functionality
- **Recent URLs Management** - View and manage your shortened URLs
- **Automatic Redirection** - Seamlessly redirects to original URLs
- **Responsive Design** - Works on all devices
- **Modern UI** - Beautiful gradient design with smooth animations

## 🚀 Quick Start

1. **Clone or download** this repository
2. **Open** `index.html` in your web browser
3. **Start shortening URLs!**

### Local Development Server

For the best experience, serve the files using a local server:

```bash
# Using Python
python3 -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server

# Using PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

## 📖 How It Works

1. **Enter a long URL** in the input field
2. **Click "Shorten URL"** or press Enter
3. **Copy the shortened URL** and share it
4. **Access the short URL** to automatically redirect to the original

### URL Format
- Short URLs follow the pattern: `your-domain.com#AbC123`
- The hash fragment (`#AbC123`) contains the unique short code
- Original URLs are stored in browser's localStorage

## 🛠️ Technical Details

- **Pure JavaScript** - No frameworks or dependencies
- **localStorage** - Client-side data persistence
- **Hash-based routing** - Uses URL fragments for redirection
- **Responsive CSS** - Mobile-first design approach
- **Modern ES6+** - Uses classes, arrow functions, and modern JavaScript features

## 📱 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🔧 Customization

### Changing the Base URL
Update the `baseUrl` property in `script.js`:

```javascript
this.baseUrl = 'https://your-domain.com';
```

### Modifying the Short Code Length
Change the loop in the `generateShortCode()` method:

```javascript
for (let i = 0; i < 8; i++) { // Change 6 to desired length
```

### Styling
All styles are in `style.css`. The design uses CSS custom properties and modern layout techniques.

## 📊 Data Storage

URLs are stored in browser's localStorage with the following structure:

```javascript
{
  "AbC123": {
    "originalUrl": "https://example.com/very/long/url",
    "createdAt": "2024-01-01T00:00:00.000Z",
    "clickCount": 5
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with vanilla JavaScript for maximum compatibility
- Inspired by popular URL shorteners like bit.ly and tinyurl.com
- Uses modern web standards for optimal performance
