========================================================================
Django CRUD React js FAGSOFT
========================================================================

Django Apps for my personal Django app to be used in my projects.

Detailed documentation is in the "docs" directory.

Quick start
-----------
1. Install Dependecies:
    pip install pilkit==2.0
    pip install Pillow==7.1.0
    pip install djangorestframework==3.11.0
    pip install Django==3.0.5
    pip install django-imagekit==4.0.2
    pip install django-rest-knox==4.1.0
    pip install pycrypto==2.6.1

2. Add to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'knox',
        'imagekit',
        'users_extended',
        'permissions',
        'app_configurations',
        'countries',
    ]

3. To get apis urls::

    from utils.apis.apis_utilities import DefaultRouter
    from users_extended.urls import router as users_router
    from permissions.urls import router as permissions_router
    from app_configurations.urls import router as app_configurations_router
    from countries.urls import router as countries_router

    router = DefaultRouter()
    router.extend(countries_router)
    router.extend(users_router)
    router.extend(permissions_router)
    router.extend(app_configurations_router)

    urlpatterns = [
        path('api/', include(router.urls)),
        ...
    ]

4. Add to settings::

    KEY_ENCRY = '$3ST_43sl4C0ntr4_s3n4m4_sFu3rt3$'
    VECTOR_ENCRY = 'n$3rt3$4m4_ntr4_'
