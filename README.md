# 🧩 JS Source Map Extractor

This tool downloads `.js.map` files from a list of JavaScript URLs, then extracts the original source files from each sourcemap.

✅ Use cases:
- Reverse engineering bundled JS
- Reviewing minified frontend apps
- Recon in bug bounty & security research

---

## ✨ Features

- Automatically appends `.map` to JS URLs
- Concurrent downloads for speed
- Extracts embedded sources using `sourcesContent`
- Preserves original folder structure
- CLI-friendly for automation

---

## 📽 Demo

[![Watch the demo](https://i.vimeocdn.com/video/960805645-f3e53de96cbb9624a816cf73d5d36b038a5c3eb208c758b8d77c3f95f2833fd6-d_640)](https://vimeo.com/45830194)

> ▶️ Click the image above to watch the demo on Vimeo  
> *(Note: GitHub markdown does **not** support direct video embedding — only links/previews)*

---

## 🛠 Installation

```bash
git clone https://github.com/yourusername/js-source-extractor.git
cd js-source-extractor
pip install -r requirements.txt
```

### Options:

| Flag         | Description                                     |
| ------------ | ----------------------------------------------- |
| `-l`         | Path to `.txt` file containing JS URLs          |
| `-o`         | Directory to save extracted sources             |
| `-c` *(opt)* | Number of concurrent downloads (default: CPU×2) |

---

## 📥 Input Example

Create a text file named `js_urls.txt` with the following content:

```
https://example.com/static/js/main.abc123.js
https://cdn.site.com/assets/app.min.js
https://myapp.net/scripts/dashboard.js
```

The script will attempt to download these files:

```
https://example.com/static/js/main.abc123.js.map
https://cdn.site.com/assets/app.min.js.map
https://myapp.net/scripts/dashboard.js.map
```

Make sure the `.map` files exist and are accessible.

---

## 📁 Output

* Extracted `.js` / `.ts` files are stored in the given `output_folder`
* Source files retain their folder structure
* Downloaded `.js.map` files are saved in `sourcemap-download/`

---

## ⚖️ License

MIT — use freely, but attribution is appreciated.
Made with ❤️ for researchers, devs, and hackers.

---

## 💬 Contribute or Suggest

Feel free to open an issue or PR if you have improvements or ideas!

```

Let me know if you want this README localized (e.g., in Bahasa Indonesia) or the example updated with real URLs you use.
```
