
# coding: utf-8
import time
import re
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from pprint import pprint


def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver

driver = init_driver()


# This portion of the code is used to scrape the post-dispatch.
df_anual = pd.DataFrame()
df_totals = pd.DataFrame()
driver.get("http://appcenter.grupoice.com/CenceWeb/CencePosdespachoNacional.jsf")

calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))

calendar.click()

box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
box.click()

y = 1
for year_i in range(2013, 2016):

    print "Year Loop"
    print year_i

    year = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDateEditorLayoutY" + str(y))))
    year.click()

    time.sleep(1)

    df_month = pd.DataFrame()
    for month_i in range(1, 13):

        print ' Month loop ' + str(month_i)

        month = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDateEditorLayoutM" + str(month_i - 1))))
        month.click()

        time.sleep(1)

        ok = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDateEditorButtonOk")))
        ok.click()

        time.sleep(1)

        day_i = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDayCell15")))
        day_i.click()
        calendar.click()
        calendar.send_keys(Keys.RETURN)

        time.sleep(1)

        print ' day loop post-dispatch'

        if month_i == 1:
            number_of_days = 31
        elif month_i == 2:
            number_of_days = 28
        elif month_i == 3:
            number_of_days = 31
        elif month_i == 4:
            number_of_days = 30
        elif month_i == 5:
            number_of_days = 31
        elif month_i == 6:
            number_of_days = 30
        elif month_i == 7:
            number_of_days = 31
        elif month_i == 8:
            number_of_days = 31
        elif month_i == 9:
            number_of_days = 30
        elif month_i == 10:
            number_of_days = 31
        elif month_i == 11:
            number_of_days = 30
        elif month_i == 12:
            number_of_days = 31

        for day_i in range(1, (number_of_days + 1)):

            print "     " + str(day_i) + " " + str(month_i) + " " + str(year_i)

            calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))
            calendar.click()
            day = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDayCell" + str(day_i + (datetime(year_i, month_i, 1).weekday() - 1)))))
            day.click()
            calendar.click()
            calendar.send_keys(Keys.RETURN)
            time.sleep(5)
            html = driver.page_source
            # Download into Python
            soup = BeautifulSoup(html, 'html.parser')
            # Searches through HTML
            table = soup.find('table', {"class": "tablaDatos"})
            # looks for the table, I have to look into the name or class.
            df_day = pd.DataFrame()
            for row in table.tbody.findAll("tr"):
                plant = []
                df_plant = pd.DataFrame()
                for val in row.findAll("td"):
                    plant.append(val.text)
                df_plant = pd.DataFrame(plant)
                df_plant.columns = df_plant.iloc[0]
                df_plant = df_plant.drop(df_plant.index[[0, 25]])
                df_day = df_day.T.append(df_plant.T)
                df_day = df_day.T
            datetime_list = []
            for hour in range(0, 24):
                datetime_list.append(datetime(year_i, month_i, day_i, int(hour)))
            df_day['datetime'] = datetime_list
            df_day = df_day.set_index('datetime')
            # These two loops go around the cells and form the table of interest.
            df_month = df_month.append(df_day)
        calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))
        calendar.click()
        box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
        box.click()

    time.sleep(5)
    df_anual = df_anual.append(df_month)
    y = 5
df_anual_Post = df_anual.fillna(0)
df_anual_Post.to_csv('df_anual_Post.csv', encoding='utf-8')

# This portion of the code is used to scrape the pre-dispatch.

df_anual = pd.DataFrame()
df_totals = pd.DataFrame()
driver.quit()
driver = init_driver()
driver.get("http://appcenter.grupoice.com/CenceWeb/CencePredespachoTecnicoNacional.jsf")
calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaInputDate")))

calendar.click()

box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
box.click()

y = 1
for year_i in range(2013, 2016):

    print "Year Loop"
    print year_i

    year = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDateEditorLayoutY" + str(y))))
    year.click()

    time.sleep(1)

    df_month = pd.DataFrame()
    for month_i in range(1, 13):

        print ' Month loop ' + str(month_i)

        month = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDateEditorLayoutM" + str(month_i - 1))))
        month.click()

        time.sleep(1)

        ok = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDateEditorButtonOk")))
        ok.click()

        time.sleep(1)

        day_i = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDayCell15")))
        day_i.click()
        calendar.click()
        calendar.send_keys(Keys.RETURN)

        time.sleep(1)

        if month_i == 1:
            number_of_days = 31
        elif month_i == 2:
            number_of_days = 29
        elif month_i == 3:
            number_of_days = 31
        elif month_i == 4:
            number_of_days = 30
        elif month_i == 5:
            number_of_days = 31
        elif month_i == 6:
            number_of_days = 30
        elif month_i == 7:
            number_of_days = 31
        elif month_i == 8:
            number_of_days = 31
        elif month_i == 9:
            number_of_days = 30
        elif month_i == 10:
            number_of_days = 31
        elif month_i == 11:
            number_of_days = 30
        elif month_i == 12:
            number_of_days = 31

        print ' day loop pre-dispatch'
        for day_i in range(1, (number_of_days + 1)):

            print "     " + str(day_i) + " " + str(month_i) + " " + str(year_i)

            calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaInputDate")))
            calendar.click()
            day = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDayCell" + str(day_i + (datetime(year_i, month_i, 1).weekday() - 1)))))
            day.click()
            calendar.click()
            calendar.send_keys(Keys.RETURN)
            time.sleep(1)
            html = driver.page_source
            # Download into Python
            soup = BeautifulSoup(html, 'html.parser')
            # Searches through HTML
            table = soup.find('table', {"class": "tablaDatos"})
            # looks for the table, I have to look into the name or class.
            df_day = pd.DataFrame()
            for row in table.tbody.findAll("tr"):
                plant = []
                df_plant = pd.DataFrame()
                for val in row.findAll("td"):
                    plant.append(val.text)
                df_plant = pd.DataFrame(plant)
                df_plant.columns = df_plant.iloc[0]
                df_plant = df_plant.drop(df_plant.index[[0, 25]])
                df_day = df_day.T.append(df_plant.T)
                df_day = df_day.T
            datetime_list = []
            for hour in range(0, 24):
                datetime_list.append(datetime(year_i, month_i, day_i, int(hour)))
            df_day['datetime'] = datetime_list
            df_day = df_day.set_index('datetime')
            # These two loops go around the cells and form the table of interest.
            df_month = df_month.append(df_day)
        calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaInputDate")))
        calendar.click()
        box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
        box.click()

    time.sleep(5)
    df_anual = df_anual.append(df_month)
    y = 5
df_anual_pre = df_anual.fillna(0)
df_anual_pre.to_csv('df_anual_pre.csv', encoding='utf-8')


# Code for the exchanges
# driver.quit()


def proc_html_data(transfer):
    transfer = transfer.replace(",", ".")
    try:
        found = re.findall('&lt;set value=\'(.+?)\'/&gt;', transfer)
    except AttributeError:
        found = ''

    nfound = []
    for x in found:
        nfound.append(float(x.encode('ascii', 'ignore')))

    df_transfer = pd.DataFrame(nfound)
    return df_transfer

df_anual = pd.DataFrame()
driver.get("http://appcenter.grupoice.com/CenceWeb/CenceIntercambios.jsf?init=true")
calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formIntercambios:pickFechaInputDate")))
calendar.click()

box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
box.click()

y = 3
for year_i in range(2015, 2016):

    print "Year Loop"
    print year_i

    year = driver.wait.until(EC.presence_of_element_located((By.ID, "formIntercambios:pickFechaDateEditorLayoutY" + str(y))))
    year.click()

    time.sleep(1)

    df_month = pd.DataFrame()
    for month_i in range(1, 13):

        print ' Month loop ' + str(month_i)

        month = driver.wait.until(EC.presence_of_element_located((By.ID, "formIntercambios:pickFechaDateEditorLayoutM" + str(month_i - 1))))
        month.click()

        time.sleep(1)

        ok = driver.wait.until(EC.presence_of_element_located((By.ID, "formIntercambios:pickFechaDateEditorButtonOk")))
        ok.click()

        time.sleep(1)

        day_i = driver.wait.until(EC.presence_of_element_located((By.ID, "formIntercambios:pickFechaDayCell15")))
        day_i.click()
        calendar.click()
        calendar.send_keys(Keys.RETURN)

        time.sleep(1)

        print ' day loop Transfers'

        if month_i == 1:
            number_of_days = 31
        elif month_i == 2:
            number_of_days = 28
        elif month_i == 3:
            number_of_days = 31
        elif month_i == 4:
            number_of_days = 30
        elif month_i == 5:
            number_of_days = 31
        elif month_i == 6:
            number_of_days = 30
        elif month_i == 7:
            number_of_days = 31
        elif month_i == 8:
            number_of_days = 31
        elif month_i == 9:
            number_of_days = 30
        elif month_i == 10:
            number_of_days = 31
        elif month_i == 11:
            number_of_days = 30
        elif month_i == 12:
            number_of_days = 31

        for day_i in range(1, (number_of_days + 1)):

            print "     " + str(day_i) + " " + str(month_i) + " " + str(year_i)

            calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formIntercambios:pickFechaInputDate")))
            calendar.click()
            day = driver.wait.until(EC.presence_of_element_located((By.ID, "formIntercambios:pickFechaDayCell" + str(day_i + (datetime(year_i, month_i, 1).weekday() - 1)))))
            time.sleep(1)
            day.click()
            calendar.click()
            calendar.send_keys(Keys.RETURN)
            time.sleep(1)
            html = driver.page_source
            df_day = pd.DataFrame()
            Real_Norte_html = html[html.find('seriesName=\'Real Norte\''):html.find(';dataset seriesName=\'Real Sur\'')]
            Real_Sur_html = html[html.find('seriesName=\'Real Sur\''):html.find(';dataset seriesName=\'Programado Norte\'')]
            Programado_Norte_html = html[html.find('seriesName=\'Programado Norte\''):html.find(';dataset seriesName=\'Programado Sur\'')]
            Programado_Sur_html = html[html.find('seriesName=\'Programado Sur\''):html.find(';/dataset&gt;&lt;styles&gt;&lt;definition&gt;&lt;stylename=\'EstiloTitulo\'')]
            df_real_norte = proc_html_data(Real_Norte_html)
            df_real_sur = proc_html_data(Real_Sur_html)
            df_programado_norte = proc_html_data(Programado_Norte_html)
            df_programado_sur = proc_html_data(Programado_Sur_html)
            df_day = df_day.append(df_real_norte.T)
            df_day = df_day.append(df_real_sur.T)
            df_day = df_day.append(df_programado_norte.T)
            df_day = df_day.append(df_programado_sur.T)
            df_day = df_day.T
            datetime_list = []
            for hour in range(0, 24):
                for minute in range(0, 46, 15):
                    datetime_list.append(datetime(year_i, month_i, day_i, int(hour), int(minute)))
            df_day['datetime'] = datetime_list
            df_day = df_day.set_index('datetime')
            df_month = df_month.append(df_day)
        calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formIntercambios:pickFechaInputDate")))
        calendar.click()
        box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
        box.click()

    time.sleep(5)
    df_anual = df_anual.append(df_month)
    y = 5
df_intercambios = df_anual.fillna(0)
df_intercambios.columns = ['Real_Norte', 'Real_Sur', 'Programado_Norte', 'Programado_Sur']
df_intercambios.to_csv('df_intercambios.csv', encoding='utf-8')
