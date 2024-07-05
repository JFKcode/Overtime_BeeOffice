import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import datetime
import logging
import os
from tkinter import messagebox

def add_overtime():
    # Sprawdzenie, czy plik data.csv istnieje
    if not os.path.exists('data.csv'):
        messagebox.showerror("Błąd", "Plik data.csv nie istnieje.")
        return

    # Konfiguracja logowania
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M',
                        filename='wprowadzone.log',
                        encoding='UTF-8',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    now = datetime.date.today()
    csvname = str(now) + ".csv"

    # Ładowanie danych z pliku data.csv
    nadgodziny = pd.read_csv('data.csv', header=None).rename(columns={
        0: 'ID',
        1: 'Data',
        2: 'GodzinaOd',
        3: 'GodzinaDo'
    })

    # Ładowanie danych logowania z pliku loginy.csv
    if not os.path.exists('loginy.csv'):
        messagebox.showerror("Błąd", "Plik loginy.csv nie istnieje.")
        return

    loginy = pd.read_csv('loginy.csv', header=None).rename(columns={
        0: 'ID',
        1: 'Login',
        2: 'Haslo'
    })

    driver = webdriver.Firefox()

    def enter_rcp(loginx, ngyx):
        driver.get("https://app.beeoffice.com/HRWorktime/HRWorktimeEdit.aspx?id=null&source=%7e%2fhrworktime%2fhrworktime.aspx&search1=&page1=1&all1=False&tab1=0")

        login = json.loads(loginx)
        for index in login:
            assert "BeeOffice" in driver.title
            elem = driver.find_element(By.ID, "UserName")
            elem.clear()
            elem.send_keys(login[index]['Login'])
            elem = driver.find_element(By.ID, "Password")
            elem.clear()
            elem.send_keys(login[index]['Haslo'])
            elem = driver.find_element(By.ID, "System")
            elem.clear()
            elem.send_keys("flexfilm")
            elem = driver.find_element(By.ID, "LoginButton")
            elem.click()

        ngy = json.loads(ngyx)

        for index in ngy:
            ng = ngy[index]
            driver.get("https://app.beeoffice.com/HRWorktime/HRWorktimeEdit.aspx?id=null&source=%7e%2fhrworktime%2fhrworktime.aspx&search1=&page1=1&all1=False&tab1=0")
            Select(driver.find_element(By.ID, "ctl00_ctl00_ContentBodyBase_ContentBody_DropDownListType")).select_by_value("6a1d06d0-1d45-4147-9e4f-f61ba63fd499")
            elem = driver.find_element(By.ID, "ctl00_ctl00_ContentBodyBase_ContentBody_NeODateTimeControlStart1_TextBoxDate")
            elem.clear()
            elem.send_keys(ng['Data'])
            elem = driver.find_element(By.ID, "ctl00_ctl00_ContentBodyBase_ContentBody_NeODateTimeControlStart1_TextBoxTime")
            elem.clear()
            elem.send_keys(ng['GodzinaOd'])
            elem = driver.find_element(By.ID, "ctl00_ctl00_ContentBodyBase_ContentBody_NeODateTimeControlEnd1_TextBoxTime")
            elem.clear()
            elem.send_keys(ng['GodzinaDo'])
            driver.execute_script("document.querySelector('#ctl00_ctl00_ContentBodyBase_SidePanel_NeoKomentarz_Comment').value = 'Overtime';")
            driver.find_element(By.ID, "ctl00_ctl00_ContentBodyBase_ContentBody_NeOWorkflowControl1_LinkButtonAccept").click()

            if driver.title == "Wniosek o zmianę czasu pracy":
                try:
                    elem = driver.find_element(By.CSS_SELECTOR, "#ctl00_ctl00_ContentBodyBase_ContentBody_NeOFormControl_divErrorText")
                    if elem.text == "Wniosek nakłada się z innym wnioskiem":
                        logging.warning(str(index) + " " + elem.text)
                    else:
                        logging.error(str(index) + " " + elem.text)
                except:
                    logging.error(f"{str(index)} Brak pola divErrorText")
            else:
                try:
                    elem = driver.find_element(By.CSS_SELECTOR, "#ctl00_ctl00_ContentBodyBase_ContentBody_NeOListControl1_divSuccessText")
                    if elem.text.startswith("Operacja wykonana pomyślnie!"):
                        logging.info(str(index) + " " + elem.text)
                except:
                    logging.error(f"{str(index)} Brak pola divSuccessText")
            logging.info(str(index) + " Done")

    starttime = datetime.datetime.now()
    driver = webdriver.Firefox()

    for a in nadgodziny['ID'].drop_duplicates():
        anad = nadgodziny.loc[nadgodziny['ID'].values == a].transpose().to_json()
        login = loginy.loc[loginy['ID'] == a].transpose().to_json()
        enter_rcp(login, anad)

    endtime = datetime.datetime.now()
    logging.info(f" Czas wykonywania: {endtime - starttime}")
    driver.close()
    driver.quit()
