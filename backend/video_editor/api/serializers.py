
from django.contrib.auth.models import User
from rest_framework import serializers


class VideoProcessSerializer(serializers.Serializer):

    video = serializers.FileField()

    prompt = serializers.CharField(
        required=False,
        default=""
    )

    language = serializers.CharField(
        default="auto"
    )

    font_style = serializers.CharField(
        default="Poppins"
    )

    animation_style = serializers.CharField(
        default="pop"
    )

    template = serializers.CharField(
        default="hormozi"
    )

    subtitle_enabled = serializers.BooleanField(
        default=True
    )

    audio_enhancement = serializers.BooleanField(
        required=False,
        default=True
    )


class SignupSerializer(
    serializers.ModelSerializer
):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "password"
        ]

    def create(
        self,
        validated_data
    ):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user

