import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HEADLESS = True  # Test için False yapabilirsin

def load_cookies(driver, cookies_str):
    driver.get("https://www.facebook.com/")
    time.sleep(5)  # Sayfanın tamamen yüklenmesini bekle

    cookies = cookies_str.split("; ")
    for c in cookies:
        try:
            name, value = c.split("=", 1)
            driver.add_cookie({
                "name": name,
                "value": value,
                "domain": "facebook.com"  # .facebook.com yerine facebook.com
            })
        except Exception as e:
            print("Cookie hatası:", e)

    driver.refresh()
    time.sleep(5)

def share_post_to_group(driver, post_url, group_id, message=""):
    driver.get(post_url)
    time.sleep(5)

    try:
        # Paylaş butonunu bul
        share_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label,'Paylaş')]"))
        )
        share_button.click()
        time.sleep(3)

        # "Bir grupta paylaş" seçeneğini seç
        in_group_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Bir grupta paylaş')]"))
        )
        in_group_option.click()
        time.sleep(3)

        # Grup adını yaz
        group_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Grup adı']"))
        )
        group_input.send_keys(group_id)
        time.sleep(2)

        # Mesaj ekle (opsiyonel)
        if message:
            text_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            text_box.send_keys(message)
            time.sleep(2)

        # Paylaş butonuna tıkla
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Gönder']"))
        )
        post_button.click()
        time.sleep(5)

        print(f"✅ Paylaşıldı: {group_id}")

    except Exception as e:
        print(f"⚠️ Hata: {group_id} -> {e}")

if __name__ == "__main__":
    cookies_str = os.getenv("FB_COOKIES")
    post_url = os.getenv("FB_POST_URL")  # Paylaşmak istediğin gönderi linki
    groups = os.getenv("FB_GROUPS").split(",")
    message = os.getenv("FB_MESSAGE", "")

    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    # Cookie ile giriş
    load_cookies(driver, cookies_str)

    # Gruplara paylaş
    for g in groups:
        group_id = g.strip().split("/")[-1]  # URL’den ID veya isim al
        share_post_to_group(driver, post_url, group_id, message)

        # Gruplar arası 10–50 saniye random bekleme
        wait_seconds = random.randint(10, 50)
        print(f"{wait_seconds} saniye bekleniyor...")
        time.sleep(wait_seconds)

    driver.quit()
