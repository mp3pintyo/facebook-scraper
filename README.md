<h1> Facebook Page Scraper </h1>

[![Python >=3.6.9](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![GitHub](https://img.shields.io/github/license/mp3pintyo/facebook-scraper)](https://github.com/mp3pintyo/facebook-scraper/blob/main/LICENSE)

<p>Egyszerű és hatékony Facebook oldal bejegyzés gyűjtő script Selenium WebDriver használatával.</p>

<!--TABLE of contents-->
<h2> Tartalomjegyzék </h2>
<details open="open">
  <summary>Tartalomjegyzék</summary>
  <ol>
    <li>
      <a href="#getting-started">Kezdő lépések</a>
      <ul>
        <li><a href="#prerequisites">Követelmények</a></li>
        <li><a href="#installation">Telepítés</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Használat</a>
      <ul>
        <li><a href="#configuration">Konfigurációs beállítások</a></li>
        <li><a href="#features">Főbb funkciók</a></li>
        <li><a href="#output">Kimenet formátuma</a></li>
      </ul>
    </li>
    <li><a href="#technical-details">Technikai részletek</a></li>
    <li><a href="#known-issues">Ismert problémák</a></li>
  </ol>
</details>

<h2 id="prerequisites">Követelmények</h2>

- Python 3.7+
- Chrome böngésző
- Internet kapcsolat
- Szükséges Python csomagok:
  - selenium
  - webdriver_manager
  - json
  - time
  - os

<h2 id="installation">Telepítés</h2>

1. Klónozza le a repository-t:
```bash
git clone https://github.com/mp3pintyo/facebook-scraper.git
```

2. Telepítse a szükséges függőségeket:
```bash
pip install -r requirements.txt
```

<h2 id="usage">Használat</h2>

<h3 id="configuration">Konfigurációs beállítások</h3>

A script az alábbi fő beállításokat tartalmazza:

```python
# Beállítások
page_name = "telexhu"  # A Facebook oldal neve
posts_count = 10       # Letöltendő posztok száma
headless = False       # Headless mód kikapcsolva (látható böngésző)
```

<h3 id="features">Főbb funkciók</h3>

1. **Cookie kezelés**
   - Automatikus cookie mentés és betöltés
   - Perzisztens bejelentkezés támogatása
   - Cookie-k tárolása `facebook_cookies.json` fájlban

2. **Intelligens várakozás**
   - Véletlenszerű várakozási idők (2-5 másodperc között)
   - Blokkolás elkerülése
   - Dinamikus oldalbetöltés kezelése

3. **Robosztus post kinyerés**
   - Többféle CSS selector használata
   - Paragrafus alapú szöveg kinyerés
   - Duplikációk kiszűrése

4. **Hibakezés**
   - Automatikus popup ablak bezárás
   - Részletes hibaüzenetek
   - Újrapróbálkozás sikertelen műveletek esetén

5. **Biztonsági funkciók**
   - Manuális bejelentkezés támogatása
   - Kétfaktoros hitelesítés kezelése
   - Cookie alapú session kezelés

<h3 id="output">Kimenet formátuma</h3>

A script a begyűjtött posztokat JSON formátumban menti:

```json
[
    "Poszt szöveg 1",
    "Poszt szöveg 2",
    ...
]
```

<h2 id="technical-details">Technikai részletek</h2>

1. **Post keresési stratégia**
   ```python
   selectors = [
       "div[data-ad-preview='message']",
       "div[data-ad-comet-preview='message']",
       "div[role='article'] div[dir='auto']",
       "div.x1iorvi4.x1pi30zi",
       "div[role='article'] p",
       "div[data-ad-comet-preview='message'] span"
   ]
   ```

2. **Görgetési logika**
   - Dinamikus oldalbetöltés kezelése
   - Maximum görgetési kísérletek számának korlátozása
   - Új tartalom ellenőrzése

3. **Hibaüzenet kezelés**
   ```python
   def close_error_popup(driver):
       try:
           popup = WebDriverWait(driver, 5).until(
               EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.layerCancel'))
           )
           popup.click()
       except:
           pass
   ```

<h2 id="known-issues">Ismert problémák</h2>

1. **Facebook változások**
   - A CSS selectorok változhatnak
   - Új biztonsági intézkedések jelenhetnek meg
   - Oldal struktúra módosulhat

2. **Bejelentkezési korlátozások**
   - Kétfaktoros hitelesítés szükséges
   - Automatikus bejelentkezés nem támogatott
   - Cookie-k érvényessége lejárhat

3. **Teljesítmény korlátok**
   - Nagy mennyiségű poszt esetén lassabb működés
   - Memória használat növekedhet
   - Hálózati késleltetés befolyásolhatja a működést

4. **Biztonsági megfontolások**
   - A script használata sértheti a Facebook felhasználási feltételeit
   - IP cím blokkolás lehetséges
   - Fiók korlátozás előfordulhat

<hr>

> **Megjegyzés**: A script használata során mindig tartsa be a Facebook felhasználási feltételeit és adatvédelmi irányelveit. A túlzott vagy agresszív használat fiók korlátozáshoz vezethet.