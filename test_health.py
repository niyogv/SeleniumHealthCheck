import time
import os
from selenium import webdriver
import pytest
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#Chrome running in headless mode
url=os.environ['URL']
chrome_options=Options()
chrome_options.add_argument('--headless')

eth_add=os.environ.get('ETH')
pkey=os.environ.get('PKEY')

@pytest.mark.flaky(rerun=2)
def test_dashboard():
    driver = webdriver.Chrome(options=chrome_options)
    wait=WebDriverWait(driver,10)
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)
    driver.find_element(By.XPATH, '//button').click()
    username = ''.join(random.choices(string.ascii_lowercase, k=5))
    password_characters = string.ascii_uppercase + string.digits + string.punctuation +string.ascii_lowercase
    password_length=10
    password = ''.join(random.samples(password_characters, password_length))
    time.sleep(1)

    #sign up page
    driver.find_element(By.LINK_TEXT, 'Create new.').click()
    time.sleep(2)
    check=driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div/div/div[2]/article')
    assert check.text=='Create a new account', 'sign up page is broken'
    driver.find_element(By.XPATH, '//input[@placeholder="Pick a username (5 or more characters)"]').send_keys(username)
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@type="checkbox"]').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(4)

    #srp page
    check1=driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div/div/div[6]/button/span')
    assert check1.text=='Create secret recovery phrase for me', 'srp page is broken'
    driver.find_element(By.XPATH, '//button').click()
    time.sleep(3)

    #cp srp page
    check2=driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div/div/a/div/article')
    assert check2.text=="I'll do this later", 'copy srp page is broken'
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div/div/a/div/article').click()
    time.sleep(2)

    #skip srp page
    check3=driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div/div/div[2]/article')
    assert check3.text=='Skip saving your secret recovery phrase?', 'Skipping srp page is broken'
    driver.find_element(By.XPATH, '//input').click()
    driver.find_element(By.XPATH, '//button[2]').click()
    time.sleep(10)

    #TOS page
    check4=driver.find_element(By.TAG_NAME, 'button')
    assert check4.text=='Create IOMe account', 'Tos page is broken'
    driver.find_element(By.XPATH, '//input').click()
    driver.find_element(By.XPATH, '//button').click()
    time.sleep(20)
    driver.find_element(By.XPATH, '//div[@class="ant-modal-content"]/button').click()
    time.sleep(2)

    #Check whether the dashboard page is good
    check5=driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/section/section/div/div[1]')
    assert check5.text=='Hello!', 'signup passed but dashboard seems to be broken'

    #edit profile
    fname=''.join(random.choices(string.ascii_lowercase,k=4))
    lname=''.join(random.choices(string.ascii_letters,k=1))
    number=''.join(random.choices(string.digits,k=10))
    mail=fname+'@'+lname+'.com'
    driver.find_element(By.XPATH, '//button[2]').click()
    time.sleep(2)
    check6=driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/button')
    assert check6.text=='Save information', 'Edit profile page is broken'
    driver.find_element(By.XPATH, '//input[@placeholder="What is your first name?"]').send_keys(fname)
    driver.find_element(By.XPATH, '//input[@placeholder="What is your last name?"]').send_keys(lname)
    driver.find_element(By.XPATH, '//input[@placeholder="unique@rmail.com"]').send_keys(mail)
    driver.find_element(By.CLASS_NAME, 'arrow').click()
    driver.find_element(By.XPATH, '//li[@class="country"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter phone number"]').send_keys(number)
    save=wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ant-btn css-htwhyh ant-btn-default bg-primary-100 text-[white] rounded-none px-10 w-auto h-10 rounded-none !font-poppins"]')))
    driver.execute_script("arguments[0].click();", save)

    #bio
    bio=''.join(random.choices(string.ascii_lowercase,k=4))
    time.sleep(2)
    driver.find_element(By.XPATH, '//textarea').send_keys(bio)
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/section/section/section/main/div/div[2]/div[2]/div/div/div/div/div[3]/div[2]/button').click()

    #avatar
    name=''.join(random.choices(string.ascii_letters,k=6))
    description=''.join(random.choices(string.ascii_lowercase,k=4))
    driver.find_element(By.LINK_TEXT, 'Avatars').click()
    time.sleep(1)
    check7=driver.find_element(By.XPATH, '//div[@class="pt-[62px] "]/div/article')
    assert check7.text=='Your Avatars', 'avatar page is broken'
    driver.find_element(By.XPATH, '//div[@class="ant-card-body"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//input').click()
    driver.find_element(By.XPATH, '//div[@class="py-8"]/button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@placeholder="Avatar Name"]').send_keys(name)
    driver.find_element(By.TAG_NAME, 'textarea').send_keys(description)
    driver.find_element(By.XPATH,'//div[@class="flex"]/div[2]/span').click()
    driver.find_element(By.XPATH, '//div[@class="pt-8"]/button').click()
    time.sleep(2)

    #create account
    eth_alias=''.join(random.choices(string.ascii_letters,k=4))
    driver.find_element(By.LINK_TEXT, 'Accounts').click()
    time.sleep(1)
    check8=driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/section/section/section/main/div/div[1]/div[1]/div/article')
    assert check8.text=='My Accounts', 'Account page is broken'
    driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'ant-select-selector').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@title="Ethereum Network"]/div').click()
    driver.find_element(By.XPATH, '//input[@Placeholder="Alias"]').send_keys(eth_alias)
    driver.find_element(By.XPATH, '//div[@class="pt-4"]/button').click()
    time.sleep(6)
    poly_alias=''.join(random.choices(string.ascii_lowercase,k=4))
    driver.find_element(By.LINK_TEXT, 'Accounts').click()
    time.sleep(1)
    driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'ant-select-selector').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@title="Polygon Network"]/div').click()
    driver.find_element(By.XPATH, '//input[@Placeholder="Alias"]').send_keys(poly_alias)
    driver.find_element(By.XPATH, '//div[@class="pt-4"]/button').click()
    time.sleep(6)

    #import account
    alias=''.join(random.choices(string.ascii_uppercase,k=4))
    driver.find_element(By.XPATH, '//button[2]').click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'ant-select-selector').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@title="Ethereum Network"]/div').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Your wallet address"]').send_keys(eth_add)
    driver.find_element(By.XPATH, '//input[@placeholder="Enter private key here"]').send_keys(pkey)
    driver.find_element(By.XPATH, '//input[@placeholder="Alias"]').send_keys(alias)
    driver.find_element(By.XPATH, '//div[@class="pt-4"]/button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@class="pt-4"]/button').click()
    time.sleep(6)
    alias1=''.join(random.choices(string.ascii_letters,k=4))
    driver.find_element(By.XPATH, '//button[2]').click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'ant-select-selector').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@title="Polygon Network"]/div').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Your wallet address"]').send_keys(eth_add)
    driver.find_element(By.XPATH, '//input[@placeholder="Enter private key here"]').send_keys(pkey)
    driver.find_element(By.XPATH, '//input[@placeholder="Alias"]').send_keys(alias1)
    driver.find_element(By.XPATH, '//div[@class="pt-4"]/button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@class="pt-4"]/button').click()
    time.sleep(6)

   #contact us
    name=''.join(random.choices(string.ascii_letters,k=4))
    des=''.join(random.choices(string.ascii_letters,k=2))
    e_mail=name+'@'+des+'.com'
    driver.find_element(By.XPATH, '//div[@class="fixed bottom-0 pl-[24px]"]/div/article').click()
    time.sleep(1)
    mail=driver.find_element(By.XPATH, '//input[@placeholder="Email"]')
    mail.send_keys(e_mail)
    user=driver.find_element(By.XPATH, '//input[@placeholder="Username"]')
    user.send_keys(name)
    description=driver.find_element(By.XPATH, '//textarea[@placeholder="Description"]')
    description.send_keys(des)
    driver.find_element(By.XPATH, '//div[@class="pt-4"]/button').click()
    time.sleep(6)
