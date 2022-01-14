from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from .slack import SendMessage
import requests, json

class TestView(APIView):
    authentication_classes = [TokenAuthentication]
    permissions_classes = [IsAuthenticated]

    def post(self, req):
        SendMessage()
        return Response(str(req.user))
    
class SearchView(APIView):
    
    # authentication_classes = [TokenAuthentication]
    # permissions_classes = [IsAuthenticated]
    
    def get(self, req):
        query = req.GET.get('q', '')
        result = requests.get('https://www.music-flo.com/api/search/v2/search?keyword='+query+'&searchType=ARTIST&sortType=ACCURACY&size=5')
        
        result_list = result.json()['data']['list'][0]['list']
        response = []
        
        for item in result_list:
            response.append({
                'id': item['id'],
                'name': item['name'],
                'image': item['imgList'][3]['url'],
            })
            
        return Response(response)
