#!/usr/bin/env python3

# todo: 
	# - Dokumentation in eigener Excel
	# - Auswertung von Soll und Haben
	# - Grafische Darstellung der Arbeitszeit pro Werktag


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
from random import randrange
import time
import sys

def entry_function(pausestart, pauseende):

	# Websiteaufruf
	s = Service ("/Users/henrikpeperkorn/chromedriver")
	driver = webdriver.Chrome(service=s)
	driver.get("https://timebutler.de/do?ha=zee&ac=1")

	# Login auf Website
	driver.find_element(By.ID, "login").send_keys(username)
	driver.find_element(By.ID, "passwort").send_keys(password)
	driver.find_element(By.CSS_SELECTOR, "#loginform > div.form-group.mar-t-m.mar-b-s > button > i").click()

	# Eintragen der Arbeits- und Pausenzeiten
	driver.find_element(By.CSS_SELECTOR, "#formNewEntry > div.form-group.mar-t-l > div > a.btn.selentertype.btn-default").click()
	driver.find_element(By.ID, "start").send_keys(arbeitsbeginn)
	driver.find_element(By.ID, "ende").send_keys(arbeitsende)
	time.sleep(5)
	if pausestart == 0:
		driver.find_element(By.ID, "bemerkung").send_keys("keine Pause.")
	else:
		driver.find_element(By.ID,"pausefrom1").send_keys(pausestart)
		driver.find_element(By.ID, "pauseto1").send_keys(pauseende)
		time.sleep(5)
		
	# Bestätigung der Arbeitszeiten und Ende
	driver.find_element(By.CSS_SELECTOR, "#newEntrySubmitBtn").click()

	time.sleep(10)

#Aktuelle Uhrzeit
now = datetime.now()

#Login-Daten
username = "USERNAME" # Benutzername/E-Mail eintragen
password = "PASSWORD" # Passwort eintragen

#Arbeitszeitdaten
#Arbeitsbeginn um 08:00 Uhr, alternative Dateneingabe per Konsolen Argument
try:
	arbeitsbeginn = str(sys.argv[1])
except IndexError:
	arbeitsbeginn = "8:00"
#Arbeitsende aktuelle Uhrzeit
arbeitsende = now.strftime("%H:%M")

#Pausendaten
#Zufallsauswahl, wann am Tag mit Pause begonnen wird
pausentimer = (randrange(5))
pausenzeiten_anfang = ["12:00", "12:15", "12:30", "12:45", "13:00"]
##Ende Pflichtpause bei 8 Stunden Arbeit
pausenzeiten30_ende = ["12:30", "12:45", "13:00", "13:15", "13:30"]
##Ende Pflichtpause bei mehr als 9 Stunden Arbeit
pausenzeiten45_ende = ["12:45", "13:00", "13:15", "13:30", "13:45"]
pausenanfang = pausenzeiten_anfang[pausentimer]
pausenende30 = pausenzeiten30_ende[pausentimer]
pausenende45 = pausenzeiten45_ende[pausentimer]

#Berechnung der Arbeitszeit 
start_time = datetime.strptime(arbeitsbeginn, "%H:%M")
end_time = datetime.strptime(arbeitsende, "%H:%M")
delta = end_time - start_time
sec = delta.total_seconds()
pflicht_restarbeitszeit = round((30600 - sec) / (60 *60),2)
# Wenn weniger als acht Stunden gearbeitet wurde
if sec < 21600:
	entry_function(0, 0)
# Wenn eine Mindestarbeitszeit von acht Stunden + 30 Minuten Pause erreicht ist
elif 21600 < sec < 34200:
	entry_function(pausenanfang, pausenende30)
# Wenn die reguläre Arbeitszeit neun Stunden überschreitet (Berechnung unter Berücksichtigung der Pflichtpause von 30m ab einer Arbeitszeit von mehr als sechs Stunden)
elif sec > 34200:
	entry_function(pausenanfang, pausenende45)