#!/usr/local/bin/python3.6




# covid-19-notifier_test.py
# Inspired from "Real-time notification for COVID-19 cases using Python" (https://www.dataspoof.info/post/real-time-notifications-for-covid-19-cases-using-python)
# Using Twilio for sending WhatsApp messages, the "requests" package for sending
# Telegram messages and Heroku to have a permanent solution: a server




## Setting the current working directory automatically
# import os
# project_path = os.getcwd() # getting the path leading to the current working directory
# os.getcwd() # printing the path leading to the current working directory
# os.chdir(project_path) # setting the current working directory based on the path leading to the current working directory




## Required packages
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from PIL import ImageGrab
from time import perf_counter
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler




## Initializations

# 1) Initializing the program...
print('Initializing the program...')


# URLs
VD_URL= 'https://www.vd.ch'
CORONA_TRACKER_SWITZERLAND_URL = 'https://www.coronatracker.com/fr/country/switzerland'


# Whatsapp automation using Twilio API
# Cf.:
# YouTube video "How to Send a WhatsApp Message with Python" (https://www.youtube.com/watch?v=98OewpG8-yw)
# Twilio website: https://www.twilio.com/console/sms/whatsapp/learn
def whatsapp_bot_sendtext(bot_message):
    credentials_text_file = open('credentials.txt')
    lines = credentials_text_file.readlines()
    account_sid = lines[2].replace('\n', '') # Twilio credentials
    auth_token = lines[4].replace('\n', '') # creating a rest client object
    client = Client(account_sid, auth_token) # creating a rest client object
    from_whatsapp_number = lines[6].replace('\n', '') # Twilio from phone number
    to_whatsapp_number = lines[8].replace('\n', '') # My (to) phone number
    credentials_text_file.close()
    client.messages.create(body=bot_message, from_=from_whatsapp_number, to=to_whatsapp_number)


# Telegram automation using the requests python package
# Cf.: https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e)
def telegram_bot_sendtext(bot_message):
    credentials_text_file = open('credentials.txt')
    lines = credentials_text_file.readlines()
    bot_token = lines[12].replace('\n', '') # python_automation_bot
    bot_chatID = lines[14].replace('\n', '') # I.e. this is my user_id
    credentials_text_file.close()
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


# Initial setup message 1/3
# message1 = ' ✅ Initial setup 1/3: WhatsApp and Telegram bot functions defined!'
# print(message1)
# # WhatsApp message
# whatsapp_bot_sendtext(message1)
# # Telegram message
# telegram_bot_sendtext(message1)


try: # trying to work with the Google spreadsheet
    # Creating a scope on "spreadsheets.google.com/feeds"
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # Initial setup message 2/3
    # message2 = ' ✅ Initial setup 2/3: "scope" on "spreadsheets.google.com/feeds" created!'
    # print(message2)
    # # WhatsApp message
    # whatsapp_bot_sendtext(message2)
    # # Telegram message
    # telegram_bot_sendtext(message2)

    # Creating some credentials using that scope and the json file
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    # Creating a gspread client authorized to use those credentials
    client = gspread.authorize(creds)
    # Creating the access to the Google spreadsheet
    sheet = client.open('covid 19 notifier spreadsheet').sheet1

    # Launching time of the program
    launching_time = perf_counter()
    # Writing the launching time to the spreadsheet
    sheet.update_cell(3, 2, launching_time) # updating the cell (3,2) (i.e. row 3, column 2)

    # Initial setup message 3/3
    # message3 = ' ✅ Initial setup 3/3: Access to the Google spreadsheet created!\n'
    # print(message3)
    # # WhatsApp message
    # whatsapp_bot_sendtext(message3)
    # # Telegram message
    # telegram_bot_sendtext(message3)

except Exception as e:
    error_message = 'Error while trying to work with the "covid 19 notifier spreadsheet"...\nError message:\n{0}'.format(e)
    print(error_message)
    # Sending WhatsApp message
    whatsapp_bot_sendtext(error_message)
    # Sending Telegram message
    telegram_bot_sendtext(error_message)




## Main function
def job_function():

    # 1) Setting up Chrome web driver using the predefined functions...
    print('1) Setting up Chrome web driver using the predefined functions...')
    # For PyCharm
    # ------
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    # Getting the resolution of the screen
    img = ImageGrab.grab()
    screen_width = img.size[0]
    screen_height = img.size[1]
    # Setting the size of the web driver window to half the size of the screen
    window_width = int(screen_width / 4)
    window_height = screen_height
    driver.set_window_size(window_width,window_height)  # (240, 160) # driver.minimize_window() # driver.maximize_window()
    # Positioning the web driver window on the right-hand side of the screen
    driver.set_window_position(window_width, 0)
    # ------

    # For Heroku
    # (cf.: https://www.youtube.com/watch?v=Ven-pqwk3ec)
    # ------
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # ------


    # 2) Accessing the Google Spreadsheet and retrieving stored values...
    print('2) Accessing the Google Spreadsheet and retrieving stored values...')
    # Computing elapsed time based on the value of the stored "launching_time" variable
    launching_time = float(sheet.cell(3,2).value)  # launching_time retrieved from the Google spreadsheet
    current_time = perf_counter()
    elapsed_time = round(current_time - launching_time)
    elapsed_time_string = str(timedelta(seconds=elapsed_time))
    # Retrieving the last_update_date from the Google spreadsheet
    last_update_date = sheet.cell(6, 1).value


    # 3) Retrieving the number of last day new cases in Switzerland
    print('3) Retrieving the number_of_last_day_new_cases in Switzerland')
    try:
        driver.get(CORONA_TRACKER_SWITZERLAND_URL) # launching Chrome on the website we want
        number_of_last_day_new_cases_encoded = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/main/div/div/div[1]/div[2]/div/div[2]/div[1]/p[3]')))
        number_of_last_day_new_cases = (re.findall('[\d]+', number_of_last_day_new_cases_encoded.text.replace(',', '')))[0]
    except Exception as e:
        number_of_last_day_new_cases = '(value not available)'
        error_message = "⚠️ Either CORONA_TRACKER_SWITZERLAND_URL ({0}) or the number of last day new cases is not available. Error message: {1}".format(CORONA_TRACKER_SWITZERLAND_URL, e)
        # WhatsApp message
        whatsapp_bot_sendtext(error_message)
        # Telegram message
        telegram_bot_sendtext(error_message)


    # 4) Checking if any change in the new directives in force in the Canton of Vaud
    print('4) Checking if any change in the new directives in force in the Canton of Vaud')
    try:
        driver.get(VD_URL)

        # Getting the most recent article date
        most_recent_article_date_encoded = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="c2000016"]/article[1]/header/p/time')))  # retrieving last update date
        most_recent_article_date = most_recent_article_date_encoded.text

        # Analyzing the title of the first article on top of the website of Canton of Vaud
        first_article_title_encoded = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="c2000016"]/article[1]/header/h3/a')))
        first_article_title = first_article_title_encoded.text
        keywords_list = [
                         'COVID-19',
                         'Covid-19',
                         'covid-19',
                         'COVID',
                         'Covid',
                         'covid',
                         'CORONAVIRUS',
                         'Coronavirus',
                         'coronavirus',
                         'CORONA',
                         'Corona',
                         'corona',
                         'Epidémie',
                         'Épidémie',
                         'épidémie',
                         'Règles',
                         'règles',
                         'Rules',
                         'rules',
                         'Vaccin',
                         'vaccin',
                         'Vaccination',
                         'vaccination',
                         'Confinement',
                         'confinement',
                         'Quatorzaine',
                         'quatorzaine',
                         'Quarantaine',
                         'quarantaine',
                         'Immunité',
                         'immunité',
                         'Distanciation',
                         'distanciation',
                         'Gestes barrières',
                         'gestes barrières',
                         'Cluster',
                         'cluster',
                         'Comorbidité',
                         'comorbidité',
                         'Asymptomatique',
                         'asymptomatique',
                         'Sanitaire',
                         'sanitaire',
                         'Grippe',
                         'grippe'
                         ]

        # Detecting any reference to COVID-19 in the title of the first article
        if any(possibilities in first_article_title for possibilities in keywords_list) and last_update_date!=most_recent_article_date: # if True
            # Updating the last_update_date value
            last_update_date = most_recent_article_date


            # 5) Retrieving useful information about COVID in Switzerland
            print('5) Retrieving useful information about COVID in Switzerland...')
            try:
                # 5.1) Retrieving the COVID statistics
                print(' 5.1) Retrieving the COVID statistics')
                driver.get(CORONA_TRACKER_SWITZERLAND_URL)

                corona_cases_total_encoded = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/main/div/div/div[1]/div[2]/div/div[2]/div[1]/p[1]'))) # full XPATH
                corona_cases_total = corona_cases_total_encoded.text.replace(',', '')

                recovered_total_encoded = driver.find_element_by_xpath('/html/body/div[1]/div/div/main/div/div/div[1]/div[2]/div/div[2]/div[2]/p[1]')  # full XPATH
                recovered_total = recovered_total_encoded.text.replace(',', '')

                deaths_total_encoded = driver.find_element_by_xpath('/html/body/div[1]/div/div/main/div/div/div[1]/div[2]/div/div[2]/div[3]/p[1]')  # full XPATH
                deaths_total = deaths_total_encoded.text.replace(',', '')

                # 5.2) Composing the new row to insert in the Google spreadsheet
                print(' 5.2) Composing the new row to insert in the Google spreadsheet')
                new_row = [last_update_date, number_of_last_day_new_cases, corona_cases_total, recovered_total, deaths_total]
                index = 6
                sheet.insert_row(new_row, index)

                # 5.3) Composing WhatsApp and Telegram message
                print(' 5.3) Composing WhatsApp and Telegram message')
                my_covid19_update = 'Hi Anthony!\n\nA new article about COVID-19 has been published on the State of Vaud website (date: {0}, title: {1}, link: {2}).\n\nHere are a few fresh numbers for Switzerland:\n- Number of last day new cases: {3}\n- Number of total laboratory-confirmed cases: {4}\n- Number of total deaths: {5}\n- Number of total recovered cases: {6}\n(Info taken from: {7})\n\nHave a nice day! See you! 😉'.format(
                    last_update_date,
                    first_article_title,
                    VD_URL,
                    number_of_last_day_new_cases,
                    corona_cases_total,
                    deaths_total,
                    recovered_total,
                    CORONA_TRACKER_SWITZERLAND_URL)

            except Exception as e:
                # 5.1) - 5.3) alternative...
                print(' 5.1) - 5.3) alternative...')
                my_covid19_update = "⚠️ Either CORONA_TRACKER_SWITZERLAND_URL ({0}) is not available or some statistics XPATHs have changed. Error message: {1}".format(
                    CORONA_TRACKER_SWITZERLAND_URL, e)


            # 5.4) Sending Whatsapp and Telegram  message to Anthony with updated COVID information...
            print(" 5.4) Sending Whatsapp and Telegram  message to Anthony with updated COVID information...")
            whatsapp_bot_sendtext(my_covid19_update)
            telegram_bot_sendtext(my_covid19_update)
            print("  ✅ Anthony has been notified!")


        else:
            still_alive_message_whatsapp = "App still running (since {0}), but no recent article about COVID-19 has been published on the State of Vaud website... (last article date: {1}). Number of last day new cases in 🇨🇭: {2}.\n(In case you haven't received messages for some time, you might be outside the free temporal Twilio window, please reconnect to the sandbox by sending 'join jack-full' to the Twilio number)".format(
                elapsed_time_string, last_update_date, number_of_last_day_new_cases)
            still_alive_message_telegram = "App still running (since {0}), but no recent article about COVID-19 has been published on the State of Vaud website... (last article date: {1}). Number of last day new cases in 🇨🇭: {2}.".format(
                elapsed_time_string, last_update_date, number_of_last_day_new_cases)

            # 5) Sending Whatsapp and Telegram message to Anthony to confirm that the app is still running...
            print("5) Sending Whatsapp and Telegram message to Anthony to confirm that the app is still running...")
            whatsapp_bot_sendtext(still_alive_message_whatsapp)
            telegram_bot_sendtext(still_alive_message_telegram)
            print(" ✅ Anthony has been notified!")


    except Exception as e: # Exception in case we can't get to the "VD_URL"
        error_message = "⚠️ Either VD_URL ({0}) or some XPATHs related to the most recent article on the State of Vaud website have changed. Error message: {1}".format(VD_URL, e)
        # WhatsApp message
        whatsapp_bot_sendtext(error_message)
        # Telegram message
        telegram_bot_sendtext(error_message)


    # 6) Quitting the web driver
    print('6) Quitting the web driver\n\n')
    driver.quit()




## Scheduling job_function to be called
sched = BlockingScheduler()
sched.add_job(func=job_function, trigger='interval', seconds=40) # hours=12
sched.start()