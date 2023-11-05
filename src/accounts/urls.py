from django.urls import path

from .views import LoginView, ProfileEditView, ProfileView, RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/view/", ProfileView.as_view()),
    path("profile/edit/", ProfileEditView.as_view()),
]
