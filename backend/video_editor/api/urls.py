from django.urls import path

from .views import (
    test_api,
    process_video,
    SignupView,
    LoginView
)

urlpatterns = [

    path(
        "test/",
        test_api
    ),

    path(
        "signup/",
        SignupView.as_view(),
        name="signup"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "process-video/",
        process_video,
        name="process_video"
    ),
]

