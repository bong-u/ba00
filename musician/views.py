from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from .slack import SendMessage

class TestView(APIView):
    authentication_classes = [TokenAuthentication]
    permissions_classes = [IsAuthenticated]

    def post(self, req):
        SendMessage()
        return Response(str(req.user))