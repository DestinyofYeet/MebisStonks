## MebisStonks Projekt

Dieses Projekt ist aus Protest enstanden um zu schlafen (weil keiner bock hat um 8 aufzustehen nur um dieses ding abzuhaken).

### Installation

Die Installation ist recht simpel.

1. Laden sie sich das git-cli für [windows] (https://github.com/git-for-windows/git/releases/download/v2.29.2.windows.3/Git-2.29.2.3-32-bit.exe) herunter.
2. Laden sie sich [Python 3.8] (https://www.python.org/ftp/python/3.8.6/python-3.8.6.exe) für windows herunter.
3. Installieren sie dieses, sie müssen eigentlich nur immer wieder auf 'Next' clicken, bis es sich installiert hat.
4. Suchen sie sich einen Speicherort für den bot, machen sie einen rechtsklick in diesen ordner und clicken sie auf 'Git Bash Here'. 
5. In dem erschienen Fenster diesen command eingeben `git clone https://github.com/DestinyofYeet/MebisStonks.git MebisStonks -b master` und drücken sie die enter taste.
6. Konfigurieren sie den Bot:
  - Sie müssen in den Ordner namens 'config' gehen und die Datei 'Benutzerdaten.ini' öffnen. Dort tragen sie ihren Benutzername und ihr passwort für mebis ein. Speichern 
  sie die Datei und schließen sie den editor wieder.
  - Öffnen sie nun die datei 'Einstellungen.ini' und tragen dort den direkten Link zur abstimmung ein.

7. Jetzt machen sie einen Doppelclick auf die run.bat datei und der bot sollte starten. Falls sie einen Fehler bekommen sollten, der so ähnlich ist wie dieser
```
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    from tools.interface import Interface
  File "X:\mebis_stonks_project\MebisStonks\tools\interface.py", line 1, in <module>
    from selenium import webdriver
ModuleNotFoundError: No module named 'selenium'
```
  machen sie einen doppelclick auf die Installer.bat datei bzw führen sie diese aus.
