from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date
import json

## Getting Books ##
def get_books():
    books = []
    i = 0
    elements = driver.find_elements(By.CLASS_NAME, 'txt_azul')
    for el in elements:
        if el.text != ' ':
            title = el.text[0:el.text.find('/')-1]
            books.append({'title': title})
    
    elements = driver.find_elements(By.CLASS_NAME, 'txt_cinza_10')
    for el in elements:
        if len(el.text) == 10:
            due = el.text
            year = int(due[6:])
            month = int(due[3:5])
            day = int(due[0:2])
            due_date = date(year, month, day)
            books[i]['return'] = due_date
            remaining_days = due_date - date.today()
            books[i]['remaining_days']= remaining_days.days     
        if len(el.text) == 6:
            renewals = int(el.text[0:1])
            books[i]['renewals'] = renewals
            i += 1
    return books

## Renewal Method ##
def renew_book(index):
    renew_buttons = driver.find_elements(By.CLASS_NAME, 'btn_renovar')
    renew_buttons[index].click()
    alert = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'box_alert_renovado')))
    need_renew = 'NãO' in alert.text
    return_button = driver.find_element(By.CLASS_NAME, 'btn_voltar')
    return_button.click()
    return not need_renew

## Starting Driver ##
driver = webdriver.Firefox()
driver.get('https://catalogobiblioteca.ufmg.br/pergamum/biblioteca_s/php/login_usu.php?flag=index.php')

## Logging in ##
with open('login_info.json') as login_file:
    login_information = json.load(login_file)
    for info in login_information.keys():
        element = driver.find_element(By.NAME, info)
        element.clear()
        element.send_keys(login_information[info])

button = driver.find_element(By.NAME, 'button')
button.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn_renovar')))

## Getting Books ##
books = get_books()

log_entry = []
for i, book in enumerate(books):
    status = ''
    print(f"Book {book['title']} expires in {book['remaining_days']} days")
    if book['remaining_days'] <= 2:
        print(f"Processing renewal of book...")
        need_renewal = renew_book(i)
        if need_renewal:
            print(f'Success on renovation of book: {book["title"]}')
            status = 'Success'
        else:
            print(f"Failed to renewal book {book['title']}")
            status = '**RENOVATION FAILED**'
    if status:
        current_log = {'title': book['title']}
        current_log['status'] = status
        log_entry.append(current_log)

## Creating Log ##
with open('log.txt', 'a') as log:
    if log_entry:
        formated_date = f'{date.today().day}/{date.today().month}/{date.today().year}'
        log.write(f"-------------Renovations Log for {formated_date}-------------\n")
        for book in log_entry:
            log.write(f"{book['title']} status of renovation: {book['status']}\n")
        log.write(f"-------------------------------------------------------\n")
    else:
        formated_date = f'{date.today().day}/{date.today().month}/{date.today().year}'
        log.write(f"-------------Renovations Log for {formated_date}-------------\n")
        log.write(f'No books needed renewal\n')
        log.write(f"-------------------------------------------------------\n")

## Closing Driver ##
driver.close()
