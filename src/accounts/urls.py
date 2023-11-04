from django.urls import path

from .views import RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    # path("login/", LoginView.as_view(), name='login'),
    # path("profile/view", ),
    # path("profile/edit", ),
]
