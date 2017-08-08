- 1. settings.py
```
from django.utils.translation import ugettext_lazy as _
# The LocaleMiddleware check's the incoming request for the 
# user's preferred language settings. Add the LocaleMiddleware
# after SessionMiddleware and CacheMiddleware, and before the 
# CommonMiddleware.
MIDDLEWARE_CLASSES = (
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.locale.LocaleMiddleware',
   'django.middleware.common.CommonMiddleware',
)
# Provide a lists of languages which your site supports.
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
)
# Set the default language for your site.
LANGUAGE_CODE = 'en'
# Tell Django where the project's translation files should be.
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
```

- 2. templates
```
# Loads the D
{% load i18n %}
<h1>{% trans 'Log in' %}</h1>
<label>{% trans 'Username' %}</label>
<input id='password' type='text'/>
<label>{% trans 'Password' %}</label>
<input id='password' type='password'/>

```

- 3. making the files

```
python manage.py makemessages -l 'fr'

myproject/
    myproject/
    templates/
        login.html
    locale/
        fr/
            LOCALE_MESSAGES/
                django.mo
 #: login.html:2
msgid "Log in"
msgstr "Connexion"
#: login.html:4
msgid "Username"
msgstr "Nom d'utilisateur"
#: login.html:7
msgid "Password"
msgstr "Mot de passe"               
                              
 ```
 
 - 4. from .mo files to .po files
```
python manage.py compilemessages
```
