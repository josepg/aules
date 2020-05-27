# aules
Aquest script es connecta a aules i recorre totes les tasques de cada curs per a mostrar quines tasques tenen entregues que encara han de ser avaluades.

# instal·lació
Es requereix Python (qualsevol versió) i els següents complements:
* mechanize (pip install mechanize)
* termcolor (pip install termcolor)
* colorama (pip install colorama)

Tots es poden instal·lar fàcilment amb el gestor de paquets de Python: pip.

# configuració
Per a configurar el programa, heu d'obrir l'arxiu config.py amb un editor de text (bloc de notes, o similar) per a canviar les dades amb la vostra informació. Molt important: no compartiu mai aquest fitxer, perquè conté la vostra contrasenya.
 
Opcional: la variable de cursosExclosos és per a posar id de cursos que no es vulguen comprovar. D'aquesta manera l'script no entra al curs a revisar les tasques (i així, guanyeu temps, perquè no va visitant totes les pàgines). Aleshores cal posar en compte d'123, 234 els números dels cursos que vulgues excloure separats per comes (si només és un, poseu-lo sense coma). Per exemple:
cursosExclosos = set([3])

# execució
Per a executar el programa crideu l'interpret d'scripts (python) i tot seguit el nom de l'script.

`python tasques.py`
