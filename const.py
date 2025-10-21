
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
    'meari': {
        'name': 'Meari',
        'url': 'https://www.meari.com/',

        'init_type': '1',    # TODO

        'app_version': '5.10.4',
        'app_version_code': '5104',
        'source_app': '81',  # TODO

        'partner_key': 'e84740f8629245b5892fab115c6d08aa',
        'partner_secret': '1ed87fee47984baba5326190dfff8ab0',
    }
}
