from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Musician
from .serializers import MusicianSerializer

from .slack import checkNewSong
import requests, json

class UpdateView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permissions_classes = [IsAuthenticated]

    def post(self, req):
        data = list(Musician.objects.values())
        
        checkNewSong(data)
        
        return Response(data)
    
class MusicianView(APIView):
    
    # authentication_classes = [TokenAuthentication]
    # permissions_classes = [IsAuthenticated]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Musician.html'
    
    def get(self, req):
        queryset = Musician.objects.all()
        return Response({'musician': queryset})
    
class SearchView(APIView):
    
    # authentication_classes = [TokenAuthentication]
    # permissions_classes = [IsAuthenticated]
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'SearchMusician.html'
    
    def get(self, req):
        
        query = req.GET.get('q')
        
        if query:
            response = self.search(query)
            return Response({'result': response})
        else:
            return Response()
    
    def search(self, query):
        
        result = requests.get('https://www.music-flo.com/api/search/v2/search?keyword='+query+'&searchType=ARTIST&sortType=ACCURACY&size=10&page=1')

        if not result.json()['data']:
            return []

        result_list = result.json()['data']['list'][0]['list']
        response = []

        for item in result_list:
            response.append({
                'value': item['id'],
                'name': item['name'],
                'recent' : 0,
                'image': item['imgList'][3]['url'],
            })
        
        return response

class AddMusicianView(APIView):
    
    def post(self, req):
        serializer = MusicianSerializer(data=req.data)
        
        if serializer.is_valid():
            item = serializer.save()
            print (item.name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)