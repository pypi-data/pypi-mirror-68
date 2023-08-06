# x-django-app

django application for all my custom stuff

The application content of on search view and several tags

Add "x_django_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'x_django_app',
    ]

To use XListView for search and sort options

    from x_django_app.views import XListView

To use x_tags in your templates

  {% load x_tags %}

To use pagination template on your templates

  {% include 'x_django_app/_pagination.html' %}
