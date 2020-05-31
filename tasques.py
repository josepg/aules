# -*- coding: utf-8 -*-
import colorama, config, mechanize, re, ssl, sys
from termcolor import colored, cprint

major_version = sys.version_info.major
if major_version == 2:
	import cookielib
elif major_version == 3:
	import http.cookiejar as cookielib
colorama.init()

cprint("Benvinguts a l'script de tasques d'aules. Versió 1.2. (twitter: @josep_g)", 'green', 'on_grey')

#Això evita errors amb els certificats autosignats d'aules:
try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	pass # Legacy Python that doesn't verify HTTPS certificates by default
else:
	ssl._create_default_https_context = _create_unverified_https_context # Handle target environment that doesn't support HTTPS verification

br = mechanize.Browser() # Inicialitzem el navegador
br.set_cookiejar(cookielib.LWPCookieJar()) # Assignem un contenidor per a les cookies (navegador)
br.set_handle_robots(False) # Li indiquem a mechanize que ignore l'arxiu robots.txt que impeteix l'ús de robots.

br.open("https://aules.edu.gva.es/moodle/login/index.php") # Obrim la pàgina d'inici d'aules.

br.select_form(nr=1) # Seleccionem el formulari d'inici de sessió
br.form['username'] = config.usuariAules # Escrivim el nom d'usuari en el formulari d'inici de sessió
br.form['password'] = config.contrasenyaAules # Escrivim la contrasenya en el formulari d'inici de sessió
response = br.submit(id="loginbtn") # Enviem el formulari d'inici de sessió
returnPage = response.read().decode('utf-8') # Resposta del formulari, pàgina inicial amb el llistat de cursos

if 'loginerrormessage' in returnPage: # Si aules dona algún error (normalment usuari/contrasenya incorrectes) d'inici de sessió, eixim i avisem
	cprint("Error iniciant la sessió en aules: heu configurat correctament l'usuari i la contrasenya?", 'red', 'on_white')
	sys.exit()

totalTasks = 0

pattern = re.compile(r'(https\:\/\/aules[0-9]?.edu.gva.es\/moodle\/course\/view.php\?id=[0-9]+)">(.*)</a>')
for courseURL, courseName in re.findall(pattern, returnPage):
	result = courseURL.split("id=")
	if int(result[1]) not in config.cursosExclosos:
		cprint(courseName, 'grey', 'on_cyan')
		url = br.open(courseURL.split('moodle')[0] + 'moodle/mod/assign/index.php?id=' + result[1]) # amb aquest codi ens assegurem d'acabar en l'aules (aules 2, 3, etc.) correcte
		returnPage = url.read() if major_version == 2 else url.read().decode('utf-8')
		pattern2 = re.compile(r'(https\:\/\/aules[0-9]?.edu.gva.es\/moodle\/mod\/assign\/view.php\?id=[0-9]+)">(.*)</a>')
		for tascaURL, tascaName in re.findall(pattern2, returnPage):
			url = br.open(tascaURL)
			returnPage3 = url.read() if major_version == 2 else url.read().decode('utf-8')
			pattern3 = re.compile(r'Necessiten qualificació</td>\n<td [a-zA-Z=" 1]+>([0-9]+)</td>')
			m = re.search(pattern3, returnPage3)
			if m:
				myQnt = m.group(1)
				if int(myQnt) > 0:
					totalTasks += int(myQnt)
					print(" └>" + tascaName + ": " + m.group(1) + ' ' + tascaURL + '&action=grader' )
cprint("Total de tasques per corregir: " + str(totalTasks), 'grey', 'on_green')