from django.urls import path

from .views import (CustomLoginView, CustomPasswordResetConfirmView,
                    CustomPasswordResetView, UserProfileView, UserRegisterView)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
