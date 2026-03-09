from django.contrib import admin
from django.urls import path
from .import views as v
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", v.index, name="index"),
    path("category-details/<int:id>", v.category_details, name="category_details"),
    path("about/", v.about_page, name="about"),
    path("contact/", v.contact_page, name="contact"),
    path("comics/<int:id>/", v.comic_detail, name="comic_detail"),
    path("read/<int:id>/first/", v.read_first, name="comic_reader_first"),
    path("read/<int:id>/last/", v.read_last, name="comic_reader_last"),
    path("register/", v.register, name="register"),
    path("login/", v.login_user, name="login"),
    path("forgot-password/", auth_views.PasswordResetView.as_view(template_name="forgot_password.html"), name="password_reset"),
    path("forgot-password/done/", auth_views.PasswordResetDoneView.as_view(template_name="forgot_password_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="reset_password.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_done.html"), name="password_reset_complete"),
    path("logout/", v.logout_user, name="logout"),
    path("profile/", v.profile_view, name="profile"),
    path("add-comic/", v.add_comic, name="add_comic"),
    path("edit-comic/<int:id>/", v.edit_comic, name="edit_comic"),
    path("delete-comic/<int:id>/", v.delete_comic, name="delete_comic"),

]
