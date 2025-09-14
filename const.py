
DEFAULT_INTEGRATION_LANGUAGE: str = 'en'
INTEGRATION_LANGUAGES = {
    'en': {
        'lang': 'English',
        'country_code': 'US',
        'phone_code': '1',
    },
    'it': {
        'lang': 'Italiano',
        'country_code': 'IT',
        'phone_code': '39',
    },
}

KNOWN_PARTNERS: dict = {
    'iegeek': {
        'name': 'ieGeek',
        'url': 'https://www.iegeek.com/',

        'init_type': '1',

        'app_version': '5.5.2',
        'app_version_code': '552',
        'source_app': '81',

        'partner_key': 'aTCOXp79xCGLFdb1HfBAPgXHnoVf9WlZ',
        'partner_secret': 'aTCOXp79xCGLFdb1HfBAPgXHnoVf9WlZ',

    },
}
