# -*- coding: utf-8 -*-
import cookielib, config, colorama, mechanize, re, ssl
from termcolor import colored, cprint

colorama.init()

#Això evita errors amb els certificats autosignats d'aules:
try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	pass # Legacy Python that doesn't verify HTTPS certificates by default
else:
	ssl._create_default_https_context = _create_unverified_https_context # Handle target environment that doesn't support HTTPS verification

br = mechanize.Browser()
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar(cookiejar)

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
br.addheaders = [( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' )]
br.open("https://aules" + config.NumAules + ".edu.gva.es/moodle/login/index.php")

br.select_form(nr=1)
br.form['username'] = config.usuariAules
br.form['password'] = config.contrasenyaAules
br.submit(id="loginbtn")

url = br.open("https://aules" + config.NumAules + ".edu.gva.es/moodle/my/")
returnPage = url.read()

pattern = re.compile(r'(https\:\/\/aules' + config.NumAules + '.edu.gva.es\/moodle\/course\/view.php\?id=[0-9]+)">(.*)</a>')

totalTasks = 0

for courseURL, courseName in re.findall(pattern, returnPage):
	result = courseURL.split("id=")
	if int(result[1]) not in config.cursosExclosos:
		cprint(courseName.decode('utf-8'), 'grey', 'on_cyan')
		url = br.open("https://aules" + config.NumAules + ".edu.gva.es/moodle/mod/assign/index.php?id=" + result[1])
		returnPage = url.read()
		pattern2 = re.compile(r'(https\:\/\/aules' + config.NumAules + '.edu.gva.es\/moodle\/mod\/assign\/view.php\?id=[0-9]+)">(.*)</a>')
		for tascaURL, tascaName in re.findall(pattern2, returnPage):
			url = br.open(tascaURL)
			returnPage3 = url.read()
			pattern3 = re.compile(r'Necessiten qualificació</td>\n<td [a-zA-Z=" 1]+>([0-9]+)</td>')
			m = re.search(pattern3, returnPage3)
			if m:
				myQnt = m.group(1)
				if int(myQnt) > 0:
					totalTasks += int(myQnt)
					print(tascaName.decode('utf-8') + ": " + m.group(1) + ' ' + tascaURL + '&action=grader' )
cprint("Total de tasques per corregir: " + str(totalTasks), 'grey', 'on_green')