import random,time,os
cwd = os.getcwd()
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
 
name_card = random.choice(["Bellamy","Nurman","Herman","Michael","Michelle","Jeniffer","Robby"])
mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 650, "pixelRatio": 3.4 },
    }

firefox_options = webdriver.ChromeOptions()
firefox_options.add_argument('--no-sandbox')
 
firefox_options.headless = True
firefox_options.add_argument('--disable-setuid-sandbox')
firefox_options.add_argument('disable-infobars')
firefox_options.add_argument('--ignore-certifcate-errors')
firefox_options.add_argument('--ignore-certifcate-errors-spki-list')

firefox_options.add_argument("--incognito")
firefox_options.add_argument('--no-first-run')
firefox_options.add_argument('--disable-dev-shm-usage')
firefox_options.add_argument("--disable-infobars")
firefox_options.add_argument("--disable-extensions")
firefox_options.add_argument("--disable-popup-blocking")
firefox_options.add_argument('--log-level=3') 
firefox_options.add_argument("--window-size=500,1090")
firefox_options.add_argument('--disable-blink-features=AutomationControlled')
firefox_options.add_experimental_option("useAutomationExtension", False)
firefox_options.add_experimental_option("excludeSwitches",["enable-automation"])
firefox_options.add_experimental_option('excludeSwitches', ['enable-logging'])
firefox_options.add_argument('--disable-notifications')
from selenium.webdriver.common.action_chains import ActionChains
random_angka = random.randint(100,999)
random_angka_dua = random.randint(10,99)


def scrape(url):
     
    global browser
    
    firefox_options.add_experimental_option("mobileEmulation", mobile_emulation)
    firefox_options.add_argument(f"user-agent=Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1")
    browser = webdriver.Chrome(options=firefox_options,executable_path=f"{cwd}\\chromedriver.exe")
    myfile = open(f"{cwd}/limit.txt","r")
    limit = myfile.read()
    browser.get(url)
    
    
    for i in range(1,int(limit)):
        try:
            from selenium.webdriver.common.action_chains import ActionChains

            
            el = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, f"(//a[contains(@href,'/item')])[{i}]")))
            browser.execute_script("return document.body.scrollHeight")
         
            actions = ActionChains(browser)
            actions.move_to_element(el).perform()
            get_url = el.get_attribute("href")
            get_text = el.text
            split_text = get_text.split('\n')
            price = split_text[1]
            title = split_text[0]
            print(f"[*] {title} | {price}")
            with open('data_ress.txt','a',encoding='utf-8') as f:
                f.write(f"{title}|{get_url}|{price}\n")
        except:
            break
    browser.quit()
if __name__ == '__main__':
    print("[*] Auto Scrape Product Aliexpress")
    jumlah = int(input("[*] Multiprocessing: "))
    limit = input("[*] Limit: ")
    with open('limit.txt','w') as f:
        f.write(limit)
   
    myfile = open(f"{cwd}\\list.txt","r")
    list_account = myfile.read()
    list_accountsplit = list_account.split("\n")
    url= list_accountsplit
    end = time.time()
    with Pool(jumlah) as p:  
        p.map(scrape, url)
    myfile = open(f"{cwd}\\data_ress.txt","r",encoding='utf-8')
    op_file = myfile.read()
    get_list = op_file.split("\n")
    total_data= get_list
    start = time.time()
    print(f"[*] Total Data Scrape: {len(total_data)}")
    print(f"[*] Time Elapsed: {round(start-end, 2)}s")
