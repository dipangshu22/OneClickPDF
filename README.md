# PDF Converter & Translator

A web application that converts **DOCX, Excel, and Image** files to PDF and translates **PDF and DOCX** documents into 50+ languages — with layout preservation. Built with Flask and deployable to Render in one click.

---

## Features

- **Convert to PDF** — supports DOCX, DOC, XLSX, XLS, XLSM, PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP
- **Multi-file upload** — convert multiple files at once and receive a single merged PDF
- **PDF Translation** — translates PDFs into 50+ languages while preserving the original layout (text positions, font sizes, colors)
- **DOCX Translation** — translates Word documents while preserving paragraph and run-level formatting
- **Smart page matching** — output PDF always matches the page count of the input file
- **Unicode font support** — automatically resolves the correct font for each language (Indic, Arabic, CJK, Cyrillic, etc.) using system fonts or downloaded Noto fonts

---

## Conversion Engines

| Input | Engine |
|---|---|
| DOCX → PDF | `python-docx` + `xhtml2pdf` |
| Excel → PDF | `openpyxl` + `reportlab` |
| Image → PDF | `Pillow` + `img2pdf` |
| PDF Translation | `PyMuPDF` + `deep-translator` (Google Translate) |
| DOCX Translation | `python-docx` + `deep-translator` (Google Translate) |

---

## Supported Languages for Translation

Arabic, Bengali, Chinese (Simplified & Traditional), French, German, Gujarati, Hindi, Indonesian, Italian, Japanese, Kannada, Korean, Malayalam, Marathi, Nepali, Persian, Polish, Portuguese, Punjabi, Russian, Spanish, Swahili, Tamil, Telugu, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and 30+ more.

---

## Tech Stack

- **Backend** — Python 3.11, Flask
- **PDF generation** — xhtml2pdf, reportlab, img2pdf
- **PDF manipulation** — PyMuPDF (fitz), pypdf
- **Document parsing** — python-docx, openpyxl
- **Translation** — deep-translator (Google Translate API)
- **Font management** — DejaVu (bundled), Noto (system or auto-downloaded)
- **Server** — Gunicorn
- **Deployment** — Render

---

## Project Structure

```
pdf_converter/
├── app.py                  # Flask routes: /convert, /translate, /download
├── font_manager.py         # Language → font resolution (Windows + Linux + download)
├── requirements.txt
├── render.yaml             # Render deployment config
├── fonts/                  # Bundled DejaVu fonts
├── converters/
│   ├── doc_converter.py    # DOCX → PDF
│   ├── excel_converter.py  # Excel → PDF
│   └── image_converter.py  # Image → PDF
└── templates/
    └── index.html          # Frontend UI
```

---

## Local Setup

**Requirements:** Python 3.11+

```bash
# Clone the repo
git clone https://github.com/your-username/pdf-converter.git
cd pdf-converter

# Install dependencies
pip install -r requirements.txt

# Create a .env file
echo "SECRET_KEY=your-secret-key" > .env

# Run the app
python app.py
```

The app will be available at `http://localhost:5000`.

---

## Deploy to Render

This project includes a `render.yaml` for one-click deployment.

1. Push this repository to GitHub
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repository
4. Render detects `render.yaml` automatically — click **Apply**
5. The build installs all Python packages and system fonts (~3–4 minutes)
6. Your app goes live at `https://your-service.onrender.com`

> **Note:** The free tier on Render spins down after inactivity. The first request after a cold start may take 30–60 seconds.

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Flask session secret (auto-generated on Render) | Yes |

---

## How Translation Works

**PDF translation** uses PyMuPDF to extract each text line with its exact bounding box, font size, and color. The original text is redacted (painted over with white) and the translated text is inserted back at the same position using the appropriate Unicode font for the target language.

**DOCX translation** rewrites each paragraph in-place using python-docx, preserving the formatting of every run (bold, italic, font size, color).

Font selection follows this priority: cached Noto font → Windows system font → Linux system font (Render/apt) → download from Google Fonts CDN → DejaVu fallback.

---

## License

MIT
