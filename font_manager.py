"""
font_manager.py
Resolves the right TTF/OTF font for a given target language.

Priority order:
  1. Already-cached font in project fonts/ folder
  2. Windows system fonts (broad Unicode coverage, no download needed)
  3. Linux/macOS system fonts
  4. Download from Google Fonts (Noto) and cache
  5. Bundled DejaVuSans (Latin/Cyrillic/Greek only — last resort)
"""

import logging
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)

FONTS_DIR = Path(__file__).parent / 'fonts'

# ── Remote font catalogue ─────────────────────────────────────────────────────
_GF   = 'https://fonts.gstatic.com/s'   # Google Fonts static CDN — stable
_BASE = 'https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf'
_CJK  = 'https://raw.githubusercontent.com/googlefonts/noto-cjk/main/Sans/SubsetOTF'

FONT_DOWNLOADS: dict[str, list[str]] = {
    # Multiple URLs tried in order (first success wins)
    'NotoSansDevanagari-Regular.ttf': [
        f'{_GF}/notosansdevanagari/v26/TuGoTUvROBcAhcRbB4KFcnALEAAAYklqFg.ttf',
        f'{_BASE}/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf',
    ],
    'NotoSansBengali-Regular.ttf': [
        f'{_GF}/notosansbengali/v21/Cn-SL0T8Towbjnh1h-YB3yoQHHnIUrI.ttf',
        f'{_BASE}/NotoSansBengali/NotoSansBengali-Regular.ttf',
    ],
    'NotoSansGujarati-Regular.ttf': [
        f'{_GF}/notosansgujarati/v22/3JnlSDv90Gmq2mr3blnHaTZXTihc8yNh.ttf',
        f'{_BASE}/NotoSansGujarati/NotoSansGujarati-Regular.ttf',
    ],
    'NotoSansGurmukhi-Regular.ttf': [
        f'{_GF}/notosansgurmukhi/v26/w8g9H3EvQP81sInb43inmyN9zZ7hc7Fh.ttf',
        f'{_BASE}/NotoSansGurmukhi/NotoSansGurmukhi-Regular.ttf',
    ],
    'NotoSansTamil-Regular.ttf': [
        f'{_GF}/notosanstamil/v20/ieVl2ZhZI2eCN5jzbjEETS9weq8-19K7DQ.ttf',
        f'{_BASE}/NotoSansTamil/NotoSansTamil-Regular.ttf',
    ],
    'NotoSansTelugu-Regular.ttf': [
        f'{_GF}/notosanstelugu/v22/0FlxfHd0YxB9SXKQ4pV7GQxDrFVJc_U.ttf',
        f'{_BASE}/NotoSansTelugu/NotoSansTelugu-Regular.ttf',
    ],
    'NotoSansKannada-Regular.ttf': [
        f'{_GF}/notosanskannada/v26/8vIs7xs32H97qzQKnzfeWzUyUpOJmz73.ttf',
        f'{_BASE}/NotoSansKannada/NotoSansKannada-Regular.ttf',
    ],
    'NotoSansMalayalam-Regular.ttf': [
        f'{_GF}/notosansmalayalam/v22/sJoi3K5XjsSdcnzn071rL37lpovuQDubFJ.ttf',
        f'{_BASE}/NotoSansMalayalam/NotoSansMalayalam-Regular.ttf',
    ],
    'NotoSansSinhala-Regular.ttf': [
        f'{_BASE}/NotoSansSinhala/NotoSansSinhala-Regular.ttf',
    ],
    'NotoSansArabic-Regular.ttf': [
        f'{_GF}/notosansarabic/v18/nwpxtLGrOAZMl5nJ_wfgRg3DrWFZWsnVBJ_sS6tlqHHFlhQ5l3sQWIHPqzCf.ttf',
        f'{_BASE}/NotoSansArabic/NotoSansArabic-Regular.ttf',
    ],
    'NotoSansThai-Regular.ttf': [
        f'{_GF}/notosansthai/v20/iJWnBXeUZi_OHPqn4wq6hQ2_hbJ1xyN9wd43SofCRg.ttf',
        f'{_BASE}/NotoSansThai/NotoSansThai-Regular.ttf',
    ],
    'NotoSansKhmer-Regular.ttf': [
        f'{_BASE}/NotoSansKhmer/NotoSansKhmer-Regular.ttf',
    ],
    'NotoSansMyanmarRegular.ttf': [
        f'{_BASE}/NotoSansMyanmar/NotoSansMyanmar-Regular.ttf',
    ],
    'NotoSansLao-Regular.ttf': [
        f'{_BASE}/NotoSansLao/NotoSansLao-Regular.ttf',
    ],
    'NotoSansSC-Regular.otf': [
        f'{_CJK}/SC/NotoSansSC-Regular.otf',
    ],
    'NotoSansTC-Regular.otf': [
        f'{_CJK}/TC/NotoSansTC-Regular.otf',
    ],
    'NotoSansJP-Regular.otf': [
        f'{_CJK}/JP/NotoSansJP-Regular.otf',
    ],
    'NotoSansKR-Regular.otf': [
        f'{_CJK}/KR/NotoSansKR-Regular.otf',
    ],
}

# ── Windows system font candidates per language ───────────────────────────────
# Listed best → worst. First existing file wins.
_WIN = Path('C:/Windows/Fonts')
_WIN_FONTS: dict[str, list[str]] = {
    'hindi':              ['mangal.ttf', 'aparajita.ttf', 'kokila.ttf', 'utsaah.ttf'],
    'nepali':             ['mangal.ttf', 'aparajita.ttf'],
    'marathi':            ['mangal.ttf', 'aparajita.ttf'],
    'bengali':            ['vrinda.ttf', 'shonar.ttf'],
    'gujarati':           ['shruti.ttf'],
    'punjabi':            ['raavi.ttf'],
    'tamil':              ['latha.ttf', 'vijaya.ttf'],
    'telugu':             ['gautami.ttf', 'vani.ttf'],
    'kannada':            ['tunga.ttf', 'kedage.ttf'],
    'malayalam':          ['kartika.ttf', 'karthika.ttf'],
    'arabic':             ['tahoma.ttf', 'arial.ttf', 'times.ttf'],
    'persian':            ['tahoma.ttf', 'arial.ttf'],
    'urdu':               ['tahoma.ttf'],
    'pashto':             ['tahoma.ttf'],
    'thai':               ['tahoma.ttf', 'leelawad.ttf', 'leelawui.ttf'],
    'chinese':            ['simsun.ttc', 'msyh.ttf', 'msyh.ttc', 'simhei.ttf'],
    'chinese simplified': ['simsun.ttc', 'msyh.ttf', 'msyh.ttc'],
    'chinese traditional':['mingliu.ttc', 'msjh.ttf', 'msjh.ttc'],
    'mandarin':           ['simsun.ttc', 'msyh.ttf'],
    'japanese':           ['meiryo.ttc', 'msgothic.ttc', 'YuGothM.ttc'],
    'korean':             ['malgun.ttf', 'malgunbd.ttf', 'gulim.ttc'],
}

# ── Linux system font candidates (Render / Ubuntu) ────────────────────────────
# After: apt-get install fonts-noto fonts-noto-cjk fonts-dejavu-core
_LINUX_FONT_DIRS = [
    Path('/usr/share/fonts/truetype/noto'),
    Path('/usr/share/fonts/opentype/noto'),
    Path('/usr/share/fonts/truetype/dejavu'),
    Path('/usr/share/fonts/truetype/liberation'),
    Path('/usr/share/fonts'),
]

_LINUX_FONTS: dict[str, list[str]] = {
    'hindi':               ['NotoSansDevanagari-Regular.ttf', 'NotoSans-Regular.ttf'],
    'nepali':              ['NotoSansDevanagari-Regular.ttf'],
    'marathi':             ['NotoSansDevanagari-Regular.ttf'],
    'bengali':             ['NotoSansBengali-Regular.ttf'],
    'gujarati':            ['NotoSansGujarati-Regular.ttf'],
    'punjabi':             ['NotoSansGurmukhi-Regular.ttf'],
    'tamil':               ['NotoSansTamil-Regular.ttf'],
    'telugu':              ['NotoSansTelugu-Regular.ttf'],
    'kannada':             ['NotoSansKannada-Regular.ttf'],
    'malayalam':           ['NotoSansMalayalam-Regular.ttf'],
    'sinhala':             ['NotoSansSinhala-Regular.ttf'],
    'arabic':              ['NotoSansArabic-Regular.ttf', 'NotoNaskhArabic-Regular.ttf'],
    'persian':             ['NotoSansArabic-Regular.ttf'],
    'urdu':                ['NotoSansArabic-Regular.ttf'],
    'pashto':              ['NotoSansArabic-Regular.ttf'],
    'thai':                ['NotoSansThai-Regular.ttf'],
    'khmer':               ['NotoSansKhmer-Regular.ttf'],
    'myanmar':             ['NotoSansMyanmar-Regular.ttf'],
    'lao':                 ['NotoSansLao-Regular.ttf'],
    'chinese':             ['NotoSansCJK-Regular.ttc', 'NotoSansSC-Regular.otf', 'NotoSansCJKsc-Regular.otf'],
    'chinese simplified':  ['NotoSansCJK-Regular.ttc', 'NotoSansSC-Regular.otf'],
    'chinese traditional': ['NotoSansCJK-Regular.ttc', 'NotoSansTC-Regular.otf'],
    'mandarin':            ['NotoSansCJK-Regular.ttc', 'NotoSansSC-Regular.otf'],
    'japanese':            ['NotoSansCJK-Regular.ttc', 'NotoSansJP-Regular.otf', 'NotoSansCJKjp-Regular.otf'],
    'korean':              ['NotoSansCJK-Regular.ttc', 'NotoSansKR-Regular.otf', 'NotoSansCJKkr-Regular.otf'],
}

# ── Language → preferred Noto font file ──────────────────────────────────────
LANGUAGE_FONT: dict[str, str] = {
    'hindi':               'NotoSansDevanagari-Regular.ttf',
    'nepali':              'NotoSansDevanagari-Regular.ttf',
    'marathi':             'NotoSansDevanagari-Regular.ttf',
    'sanskrit':            'NotoSansDevanagari-Regular.ttf',
    'bengali':             'NotoSansBengali-Regular.ttf',
    'gujarati':            'NotoSansGujarati-Regular.ttf',
    'punjabi':             'NotoSansGurmukhi-Regular.ttf',
    'tamil':               'NotoSansTamil-Regular.ttf',
    'telugu':              'NotoSansTelugu-Regular.ttf',
    'kannada':             'NotoSansKannada-Regular.ttf',
    'malayalam':           'NotoSansMalayalam-Regular.ttf',
    'sinhala':             'NotoSansSinhala-Regular.ttf',
    'arabic':              'NotoSansArabic-Regular.ttf',
    'persian':             'NotoSansArabic-Regular.ttf',
    'urdu':                'NotoSansArabic-Regular.ttf',
    'pashto':              'NotoSansArabic-Regular.ttf',
    'sindhi':              'NotoSansArabic-Regular.ttf',
    'uyghur':              'NotoSansArabic-Regular.ttf',
    'thai':                'NotoSansThai-Regular.ttf',
    'khmer':               'NotoSansKhmer-Regular.ttf',
    'myanmar':             'NotoSansMyanmarRegular.ttf',
    'lao':                 'NotoSansLao-Regular.ttf',
    'chinese':             'NotoSansSC-Regular.otf',
    'chinese simplified':  'NotoSansSC-Regular.otf',
    'chinese traditional': 'NotoSansTC-Regular.otf',
    'mandarin':            'NotoSansSC-Regular.otf',
    'cantonese':           'NotoSansSC-Regular.otf',
    'japanese':            'NotoSansJP-Regular.otf',
    'korean':              'NotoSansKR-Regular.otf',
}

_BUNDLED = 'DejaVuSans.ttf'


def _resolve_win_system_font(lang: str) -> str | None:
    """Return path to a Windows system font that supports *lang*, or None."""
    candidates = _WIN_FONTS.get(lang, [])
    for fname in candidates:
        p = _WIN / fname
        if p.exists():
            logger.info(f'Using Windows system font: {p}')
            return str(p)
    return None


def _resolve_linux_system_font(lang: str) -> str | None:
    """Return path to a Linux system font that supports *lang*, or None."""
    candidates = _LINUX_FONTS.get(lang, [])
    for fname in candidates:
        for font_dir in _LINUX_FONT_DIRS:
            p = font_dir / fname
            if p.exists() and p.stat().st_size > 1000:
                logger.info(f'Using Linux system font: {p}')
                return str(p)
    return None


def _try_download(font_file: str) -> str | None:
    """Try every URL for *font_file*. Return local path on success, None on failure."""
    urls = FONT_DOWNLOADS.get(font_file, [])
    dest = FONTS_DIR / font_file
    for url in urls:
        try:
            logger.info(f'Downloading {font_file} from {url} …')
            req = urllib.request.Request(url, headers={'User-Agent': 'pdf-converter/1.0'})
            with urllib.request.urlopen(req, timeout=30) as resp, \
                 open(dest, 'wb') as out:
                data = resp.read()
                if len(data) < 1000:
                    raise ValueError(f'Response too small ({len(data)} bytes) — probably an error page')
                out.write(data)
            logger.info(f'Font saved: {dest}')
            return str(dest)
        except Exception as exc:
            logger.warning(f'  ✗ {url}: {exc}')
            dest.unlink(missing_ok=True)
    return None


def get_font_path(target_language: str) -> str:
    """
    Return the absolute path to the best font for *target_language*.

    Priority:
      1. Cached Noto font in fonts/ folder
      2. Windows system font
      3. Linux system font (Render/Ubuntu — needs fonts-noto installed)
      4. Download Noto font and cache it
      5. Bundled DejaVuSans (Latin/Cyrillic/Greek only — last resort)
    """
    FONTS_DIR.mkdir(exist_ok=True)
    lang = target_language.lower().strip()

    # Which Noto font do we want?
    font_file = LANGUAGE_FONT.get(lang)
    if not font_file:
        for key, fname in LANGUAGE_FONT.items():
            if key in lang or lang in key:
                font_file = fname
                break

    # 1. Already cached
    if font_file:
        cached = FONTS_DIR / font_file
        if cached.exists() and cached.stat().st_size > 1000:
            logger.info(f'Using cached font: {font_file}')
            return str(cached)

    # 2. Windows system font
    sys_font = _resolve_win_system_font(lang)
    if sys_font:
        return sys_font

    # 3. Linux system font (Render / Ubuntu)
    sys_font = _resolve_linux_system_font(lang)
    if sys_font:
        return sys_font

    # 4. Download Noto font
    if font_file:
        downloaded = _try_download(font_file)
        if downloaded:
            return downloaded

    # 5. Bundled DejaVuSans (warns — will show boxes for non-Latin scripts)
    fallback = FONTS_DIR / _BUNDLED
    if fallback.exists():
        logger.warning(
            f'No specific font found for "{target_language}". '
            f'Falling back to DejaVuSans — non-Latin characters may appear as boxes. '
            f'Ensure internet access so Noto fonts can be downloaded.'
        )
        return str(fallback)

    raise RuntimeError(
        f'No font available for "{target_language}" and bundled DejaVuSans is missing. '
        f'Please ensure fonts/DejaVuSans.ttf exists in the project directory.'
    )

