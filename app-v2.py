from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from random import randint
import json
import os
import shutil

# Beállítások
page_name = "telexhu"  # Az oldal neve, amit scrapelni szeretnénk
posts_count = 10       # Hány posztot szeretnénk lementeni
headless = False       # False = látható böngésző, True = háttérben futás

# Cookie fájl elérési útja
cookie_file = "facebook_cookies.json"

def save_cookies(driver):
    """Cookie-k mentése fájlba"""
    cookies = driver.get_cookies()
    with open(cookie_file, 'w') as f:
        json.dump(cookies, f)
    print("Cookie-k elmentve")

def load_cookies(driver):
    """Cookie-k betöltése fájlból"""
    try:
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
            print("Cookie-k betöltve")
            return True
    except Exception as e:
        print(f"Hiba a cookie-k betöltése során: {str(e)}")
    return False

def close_error_popup(driver):
    """Felugró hibaüzenetek bezárása"""
    try:
        popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.layerCancel'))
        )
        popup.click()
        print("Hibaüzenet bezárva")
    except:
        pass

def extract_post_content(element):
    """Poszt tartalmának kinyerése"""
    try:
        # Próbáljuk meg először a paragrafusokat
        paragraphs = element.find_elements(By.TAG_NAME, "p")
        if paragraphs:
            return " ".join([p.get_attribute("textContent") for p in paragraphs])
        # Ha nincs paragrafus, használjuk a teljes szöveget
        return element.text.strip()
    except:
        return ""

def main():
    print("ChromeDriver telepítése...")
    # Chrome opciók beállítása
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--log-level=3")  # Csak a kritikus hibákat mutatja
    chrome_options.add_argument("--silent")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Kikapcsolja a DevTools üzeneteket
    chrome_options.add_argument("--disable-web-security")  # WebGL figyelmeztetések kikapcsolása
    chrome_options.add_argument("--enable-unsafe-swiftshader")  # SwiftShader engedélyezése

    try:
        # Webdriver inicializálása
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        print("Chrome sikeresen elindítva!")

        print("Böngésző elindítva...")
        driver.get("https://www.facebook.com")
        time.sleep(randint(2, 4))

        # Megpróbáljuk betölteni a mentett cookie-kat
        has_cookies = load_cookies(driver)

        if not has_cookies:
            print("\nKérlek, fogadd el a cookie-kat, majd jelentkezz be manuálisan a Facebook-ba.")
            print("Ha bejelentkeztél, nyomj egy Enter-t...")
            input()
            
            # Cookie-k mentése a sikeres bejelentkezés után
            save_cookies(driver)

        # Céloldal megnyitása
        print(f"Navigálás a {page_name} oldalra...")
        driver.get(f"https://www.facebook.com/{page_name}")
        time.sleep(randint(3, 5))

        # Görgetés az oldalon
        posts = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scroll_attempts = 10

        while len(posts) < posts_count and scroll_attempts < max_scroll_attempts:
            # Görgetés
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(randint(2, 4))
            scroll_attempts += 1

            # Hibaüzenetek kezelése
            close_error_popup(driver)

            # Új posztok keresése
            try:
                # Várunk, hogy megjelenjenek a posztok
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='article']"))
                )

                # Különböző CSS selectorok kipróbálása a posztokhoz
                selectors = [
                    "div[data-ad-preview='message']",
                    "div[data-ad-comet-preview='message']",
                    "div[role='article'] div[dir='auto']",
                    "div.x1iorvi4.x1pi30zi",
                    "div[role='article'] p",
                    "div[data-ad-comet-preview='message'] span"
                ]

                post_elements = []
                for selector in selectors:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        post_elements = elements
                        print(f"Posztok találva: {selector}")
                        break

                for post in post_elements:
                    if len(posts) >= posts_count:
                        break

                    try:
                        post_text = extract_post_content(post)
                        if post_text and post_text not in posts:
                            posts.append(post_text)
                            print(f"Új poszt találva ({len(posts)}/{posts_count}): {post_text[:100]}...")
                    except Exception as e:
                        print(f"Hiba egy poszt feldolgozása során: {str(e)}")
                        continue

            except Exception as e:
                print(f"Hiba a posztok keresése során: {str(e)}")

            # Ellenőrizzük, hogy van-e még új tartalom
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f"Nincs több új tartalom ({scroll_attempts}/{max_scroll_attempts} görgetési kísérlet)")
                time.sleep(randint(2, 4))
            last_height = new_height

        # Eredmények mentése
        if posts:
            with open('facebook_posts.json', 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=4)
            print(f"\nSikeresen lementve {len(posts)} poszt a facebook_posts.json fájlba!")
        else:
            print("Nem sikerült posztokat találni.")

    except Exception as e:
        print(f"Hiba történt: {str(e)}")

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
