# User model
SOCIAL_AUTH_USER_MODEL = 'auth.User'

SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/chat/logged/'

SOCIAL_AUTH_LOGIN_URL = '/'
#AUTHENTICATION BACKENDS

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# PIPELINE
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    #'social.pipeline.mail.mail_validation',
    #'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

# Username field
#SOCIAL_AUTH_UUID_LENGTH = 4
#SOCIAL_AUTH_SLUGIFY_USERNAMES = True
#SOCIAL_AUTH_CLEAN_USERNAMES = True

# Redirects and urlopens
SOCIAL_AUTH_SANITIZE_REDIRECTS = True

#Admin
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']


# Google
# /google-oauth2/
# https://console.developers.google.com/
# Создаем , приложение, oauth2 для него, вебсайт, и включаем Google+
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '370622391189-pp8q6el92t7htf5o1de3iqs7u9gude1t.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'OpXEjxE8TJOiMX1mnzkGhSSq'


SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email',
}
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# Keys
SOCIAL_AUTH_FACEBOOK_KEY = '230287217332547'
SOCIAL_AUTH_FACEBOOK_SECRET = '57b9fdbe0c8f2b9e188587a1d9a6b70c'