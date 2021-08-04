# covid-19-notifier
Python app using the Twilio Python API for WhatsApp, the `requests` package for
Telegram and the Heroku Python script hosting solution to send WhatsApp and
Telegram messages once a new article related to COVID-19 is published on the
(State of Vaud website)[https://www.vd.ch].

## Table of contents
* [1. Description](#1-description)
* [2. Getting started](#2-getting-started)
    * [2.1 Dependencies](#21-dependencies)
    * [2.2 Installing](#22-installing)
    * [2.3 Executing program](#23-executing-program)
* [3. Version history](#3-version-history)

<!-- toc -->

## 1. Description
`covid-19-notifier` is a Python app running on the Heroku web server that
makes use of the `selenium` Python package to scrape the web and check every 12
hours if a new article related to COVID-19 has been published on the State of
Vaud website. If a new article concerning COVID-19 has effectively been
published, a COVID-19 recap WhatsApp and Telegram message is sent to my phone
(+41 79 884 18 17). The message contains some info about the number of new cases
and deaths due to COVID-19 in Switzerland and the web links to the [Canton of Vaud website](https://www.vd.ch)
and the [COVID-19 news for Switzerland](https://www.coronatracker.com/fr/country/switzerland).
To be sure to properly back up important info and COVID-19 statistics, the
program consults and updates the dedicated ["covid 19 notifier spreadsheet"](https://docs.google.com/spreadsheets/d/1FgfodftPV7pf9eSDPWmRXHDFBFH1GCjzj7s7fBFll7E/edit#gid=0)
Google spreadsheet (situated on my Google Drive in My Drive > Programmation >
Real-TimeNotificationsForCOVID-19Cases).

Here are other interesting websites regarding the current COVID-19 situation in the
State of Vaud:
- [Hotline et Informations sur le Coronavirus](https://www.vd.ch/toutes-les-actualites/hotline-et-informations-sur-le-coronavirus/)
(for a summary of the directives currently in force in Canton of Vaud)
- [CoTrack (for the Canton of Vaud)](https://monitoring.unisante.ch/d/gaymj_1Mz/cotrack?orgId=4&refresh=5m)

## 2. Getting started


### 2.1 Dependencies
Concerning `covid-19-notifier_test.py`:
* Tested on macOS Catalina version 10.15.7
* Python 3.6

### 2.2 Installing
For testing `covid-19-notifier_test.py`, install the required packages by typing
following Terminal command at the root of the project:

`pip install -r requirements.txt`

To deploy the `covid-19-notifier` Python web app on the Heroku web server,
please refer to the instructions in the `_ApproachToHostOnHeroku.rtfd` file
situated in the `_Resources` folder.


### 2.3 Executing program
The `covid-19-notifier_test.py` test script can be run by typing following
command at the root of the project:

`python3.6 covid-19-notifier_test.py`

Concerning the actual web app, once deployed, the app automatically and
continuously runs on the Heroku web server.

## 3. Version history
* 0.1
    * Initial release