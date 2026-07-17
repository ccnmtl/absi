from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from absi.main.models import UserProfile


class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        up, _ = UserProfile.objects.get_or_create(user=user)
        voice_name = request.data['voice']

        if voice_name:
            up.voice = voice_name
            up.save()

        return Response(
            {
                'status': 'OK',
            },
            status=status.HTTP_200_OK,
        )
