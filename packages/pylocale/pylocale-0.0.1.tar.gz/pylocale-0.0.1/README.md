# pylocale
A Python 3 library that allows adding static files with translations to the application, and then apply them to dynamically change text in the application.

Installing
----------

**Python 3.6.9 or higher is recommended**

To install the library, you can just run the following command:

```shell script
# Linux/macOS
python3 -m pip install pylocale

# Windows
pip install pylocale
```

Translation files
--------------
You must provide a folder in your project directory where your translation files will be located.
```
your-app-root
|--translations
   |----en-us
   |----de-de
   |----zh-cn
   ...
...
```
The struture can be any, but the translation files must be accessible from the program.
Translation files must be text files of .env-like format ```<KEY> = <TRANSLATION>``` **(spaces are required or you will get a parsing error)**:

```
# en-us file example
HELP = Get help
SETTINGS = Settings
EXIT = Exit
```
```
# de-de file example
HELP = Hilfe bekommen
SETTINGS = Einstellungen
EXIT = Ausfahrt
```
It's recommended for the translation files to have the same keys, but it's not necessary.

Usage
--------------
You can use pylocal as follows:
```python
from pylocal import PyLocal

translator = PyLocal(
    at='translations/',  # Your translations directory path.
    root='en',  # Default locale.
    silent=True  # Tell PyLocal not to raise exceptions in case of errors.
)
```
To get translation:
```python
translator['HELP']  # >>> Help
```
To switch to another locale:
```python
translator.switch('de-de')
translator['HELP']  # >>> Hilfe bekommen
```
Any translation you switch to covers the root translation file. That means If there was no help key, it would be taken from the root translation file:
```
# en-us file example
HELP = Get help
SETTINGS = Settings
EXIT = Exit
COLOR = Color
```
```
# en-gb file example
COLOR = Colour
```
```python
translator = PyLocale(at='transaltions/', root='en-us')
tanslator['COLOR']  # >>> Color
translator.switch('en-gb')
tanslator['COLOR']  # >>> Colour
# SETTINGS is not defined in en-gb. It will be taken from en-us, which is the root translation file.
tanslator['SETTINGS']  # >>> Settings
```

Raising exceptions
--------------
If the silent mode is turned off (default) your app will break down with exceptions in case of errors. If you want the translator to try to return something, you may pass a True to silent parameter as shown above. In that case, the translator will return an empty string.
```python
translator = PyLocale(
    at='transaltions/',
    root='blablabla',
    silent=True
)
tanslator['SETTINGS']  # >>> ''
```