from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

import calendarweek.django
import debug_toolbar
from django_js_reverse.views import urls_js
from two_factor.urls import urlpatterns as tf_urls

from . import views

urlpatterns = [
    path("", include("pwa.urls"), name="pwa"),
    path("about/", views.about, name="about_aleksis"),
    path("admin/", admin.site.urls),
    path("data_management/", views.data_management, name="data_management"),
    path("status/", views.system_status, name="system_status"),
    path("", include(tf_urls)),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("persons", views.persons, name="persons"),
    path("persons/accounts", views.persons_accounts, name="persons_accounts"),
    path("person", views.person, name="person"),
    path("person/<int:id_>", views.person, name="person_by_id"),
    path("person/<int:id_>/edit", views.edit_person, name="edit_person_by_id"),
    path("groups", views.groups, name="groups"),
    path("groups/child_groups/", views.groups_child_groups, name="groups_child_groups"),
    path("group/create", views.edit_group, name="create_group"),
    path("group/<int:id_>", views.group, name="group_by_id"),
    path("group/<int:id_>/edit", views.edit_group, name="edit_group_by_id"),
    path("", views.index, name="index"),
    path(
        "notifications/mark-read/<int:id_>",
        views.notification_mark_read,
        name="notification_mark_read",
    ),
    path("announcements/", views.announcements, name="announcements"),
    path("announcement/create/", views.announcement_form, name="add_announcement"),
    path("announcement/edit/<int:id_>/", views.announcement_form, name="edit_announcement"),
    path("announcement/delete/<int:id_>/", views.delete_announcement, name="delete_announcement"),
    path("search/searchbar/", views.searchbar_snippets, name="searchbar_snippets"),
    path("search/", views.PermissionSearchView(), name="haystack_search"),
    path("maintenance-mode/", include("maintenance_mode.urls")),
    path("impersonate/", include("impersonate.urls")),
    path("__i18n__/", include("django.conf.urls.i18n")),
    path("select2/", include("django_select2.urls")),
    path("jsreverse.js", urls_js, name="js_reverse"),
    path("calendarweek_i18n.js", calendarweek.django.i18n_js, name="calendarweek_i18n_js"),
    path("gettext.js", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path(
        "preferences/site/", views.preferences, {"registry_name": "site"}, name="preferences_site"
    ),
    path(
        "preferences/person/",
        views.preferences,
        {"registry_name": "person"},
        name="preferences_person",
    ),
    path(
        "preferences/group/",
        views.preferences,
        {"registry_name": "group"},
        name="preferences_group",
    ),
    path(
        "preferences/site/<int:pk>/",
        views.preferences,
        {"registry_name": "site"},
        name="preferences_site",
    ),
    path(
        "preferences/person/<int:pk>/",
        views.preferences,
        {"registry_name": "person"},
        name="preferences_person",
    ),
    path(
        "preferences/group/<int:pk>/",
        views.preferences,
        {"registry_name": "group"},
        name="preferences_group",
    ),
    path(
        "preferences/site/<int:pk>/<str:section>/",
        views.preferences,
        {"registry_name": "site"},
        name="preferences_site",
    ),
    path(
        "preferences/person/<int:pk>/<str:section>/",
        views.preferences,
        {"registry_name": "person"},
        name="preferences_person",
    ),
    path(
        "preferences/group/<int:pk>/<str:section>/",
        views.preferences,
        {"registry_name": "group"},
        name="preferences_group",
    ),
    path(
        "preferences/site/<str:section>/",
        views.preferences,
        {"registry_name": "site"},
        name="preferences_site",
    ),
    path(
        "preferences/person/<str:section>/",
        views.preferences,
        {"registry_name": "person"},
        name="preferences_person",
    ),
    path(
        "preferences/group/<str:section>/",
        views.preferences,
        {"registry_name": "group"},
        name="preferences_group",
    ),
]

# Serve static files from STATIC_ROOT to make it work with runserver
# collectstatic is also required in development for this
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files from MEDIA_ROOT to make it work with runserver
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add URLs for optional features
if hasattr(settings, "TWILIO_ACCOUNT_SID"):
    from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls  # noqa

    urlpatterns += [path("", include(tf_twilio_urls))]

# Serve javascript-common if in development
if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

# Automatically mount URLs from all installed AlekSIS apps
for app_config in apps.app_configs.values():
    if not app_config.name.startswith("aleksis.apps."):
        continue

    try:
        urlpatterns.append(path(f"app/{app_config.label}/", include(f"{app_config.name}.urls")))
    except ModuleNotFoundError:
        # Ignore exception as app just has no URLs
        pass  # noqa
