from typing import Any, Dict

from django.conf import settings
from rest_framework.settings import APISettings

SPECTACULAR_DEFAULTS: Dict[str, Any] = {
    # path prefix is used for tagging the discovered operations.
    # use '/api/v[0-9]' for tagging apis like '/api/v1/albums' with ['albums']
    'SCHEMA_PATH_PREFIX': r'',
    # Sorting the operations
    #   alpha: alphanumerically and then METHOD,
    #   method: DRF default sorting just by METHOD
    'OPERATION_SORTER': 'alpha',
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',

    # Configuration for serving the schema with SpectacularAPIView
    'SERVE_URLCONF': None,
    # complete public schema or a subset based on the requesting user
    'SERVE_PUBLIC': True,
    # is the
    'SERVE_INCLUDE_SCHEMA': True,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],

    # Append OpenAPI objects to path and components in addition to the generated objects
    'APPEND_PATHS': {},
    'APPEND_COMPONENTS': {},

    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    'TITLE': '',
    'DESCRIPTION': '',
    'TOS': None,
    # Optional: MAY contain "name", "url", "email"
    'CONTACT': {},
    # Optional: MUST contain "name", MAY contain URL
    'LICENSE': {},
    'VERSION': '0.0.0',
    # Optional list of servers.
    # Each entry MUST contain "url", MAY contain "description", "variables"
    'SERVERS': [],
    'SECURITY': None,
    # Tags defined in the global scope
    'TAGS': [],
    # Optional: MUST contain 'url', may contain "description"
    'EXTERNAL_DOCS': {},

    # Oauth2 related settings. used for example by django-oauth2-toolkit.
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#oauth-flows-object
    'OAUTH2_FLOWS': [],
    'OAUTH2_AUTHORIZATION_URL': None,
    'OAUTH2_TOKEN_URL': None,
    'OAUTH2_REFRESH_URL': None,
    'OAUTH2_SCOPES': None,
}

IMPORT_STRINGS = [
    'SCHEMA_AUTHENTICATION_CLASSES',
    'DEFAULT_GENERATOR_CLASS',
    'SERVE_PERMISSIONS',
]

spectacular_settings = APISettings(
    user_settings=getattr(settings, 'SPECTACULAR_SETTINGS', {}),
    defaults=SPECTACULAR_DEFAULTS,
    import_strings=IMPORT_STRINGS,
)
