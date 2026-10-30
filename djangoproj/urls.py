from django.contrib import admin
from django.urls import path

from djangoapp import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("dealer/<int:dealer_id>/", views.dealer_detail, name="dealer_detail"),
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path("login", views.login_api, name="login_api"),
    path("register", views.register_api, name="register_api"),
    path("logout", views.logout_api, name="logout_api"),
]
