
import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .serializers import (
    VideoProcessSerializer,
    SignupSerializer
)

from video_editor.services.orchestrator import (
    handle_video_edit
)


@api_view(["GET"])
def test_api(request):

    return Response({
        "message": "AI Video Backend Working"
    })


class SignupView(
    APIView
):

    def post(
        self,
        request
    ):

        serializer = SignupSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User created successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
class LoginView(
    APIView
):

    def post(
        self,
        request
    ):

        username = request.data.get(
            "username"
        )

        password = request.data.get(
            "password"
        )

        user = authenticate(
            username=username,
            password=password
        )

        if not user:

            return Response(
                {
                    "error": "Invalid credentials"
                },
                status=401
            )

        refresh = RefreshToken.for_user(
            user
        )

        return Response({

            "message": "Login successful",

            "access": str(
                refresh.access_token
            ),

            "refresh": str(
                refresh
            ),

            "username": user.username
        })




@api_view(["POST"])
def process_video(request):

    serializer = VideoProcessSerializer(
        data=request.data
    )

    if not serializer.is_valid():

        return Response(
            serializer.errors,
            status=400
        )

    data = serializer.validated_data

    video = data["video"]

    upload_dir = "media/uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    video_path = os.path.join(
        upload_dir,
        video.name
    )

    with open(
        video_path,
        "wb+"
    ) as destination:

        for chunk in video.chunks():

            destination.write(
                chunk
            )

    safe_config = {
        "prompt": data.get("prompt"),
        "language": data.get("language"),
        "font_style": data.get("font_style"),
        "animation_style": data.get("animation_style"),
        "template": data.get("template"),
        "subtitle_enabled": data.get("subtitle_enabled"),
        "audio_enhancement": data.get("audio_enhancement"),
    }

    output = handle_video_edit(
        video_path=video_path,
        config=safe_config
    )

    return Response({
        "message": "Video uploaded successfully",
        "output": output
    })

