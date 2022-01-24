from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from . import models

class SignUpView(APIView):
    
    def post(self, req):
        user = User.objects.create_user (username=req.data['id'], password=req.data['password'])
        profile = models.Profile(user=user, nickname=req.data['nickname'])
        
        user.save()
        profile.save()
        
        token = Token.objects.create(user=user)
        
        return Response({'token' : token.key})


class AuthView(APIView):
    
    def post(self, req):
        user = authenticate(username=req.data['id'], password=req.data['password'])

        if user is not None:
            token = Token.objects.get(user=user)
            token.delete()
            token = Token.objects.create(user=user)
            
            return Response({'token': 'token '+token.key})
        else:
            return Response(status=401)
