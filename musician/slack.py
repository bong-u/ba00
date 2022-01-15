import requests, json
from decouple import config


class UpdateMusician:
    
    __albums = []
    __musicians = []
    
    def __init__(self, musicians):
        self.__checkNewSong(musicians)
        
    
    def __checkNewSong(self, musicians):

        for musician in musicians:

            res = requests.get('https://www.music-flo.com/api/meta/v1/artist/'+ str(musician['value']) + '/album?sortType=RECENT&size=3&roleType=RELEASE')

            albums = json.loads(res.text)

            for album in albums['data']['list']:
                if musician['recent'] == album['id']:
                    break;

                needUpdate = True;
                self.__albums.append({
                    'artist' : musician['name'],
                    'title' : album['title'],
                    'releaseYmd' : album['releaseYmd'],
                    'image' : album['imgList'][4]['url'],
                    'tracks' : self.__getTracks(str(album['id']), musician['name'])
                })

            if needUpdate:
                musician['recent'] = albums['data']['list'][0]['id']
                self.__musicians.append(musician)
            break


    def __getTracks(self, album, musicianName):

        result = []

        res = requests.get ('https://www.music-flo.com/api/meta/v1/album/' + album + '/track')

        tracks = json.loads (res.text)

        for n, item in enumerate(tracks['data']['list']):

            artists = []

            for musician in item['artistList']:
                artists.append (musician['name'])

            value = '{0}. {1} - {2}'.format (str(n+1), item['name'], ', '.join(artists))

            result.append ({'value' : value})

        return result
    
    def getAlbums(self):
        return self.__albums
    
    def getMusicians(self):
        return self.__musicians
    
    def SendMessage(self):
        
        for album in self.__albums:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + config('SLACK_TOKEN')
            }
            msg = {
                'channel': 'C02TVSQ9XML',
                'attachments': [
                    {
                        'mrkdwn_in': ['text'],
                        'color': '#4929f2',
                        'title': album['artist'] + ' - ' + album['title'],
                        'thumb_url': album['image'],
                        'fields': album['tracks'],
                        'footer': 'FLO',
                        'footer_icon': 'https://www.music-flo.com/favicon.ico'
                    }
                ]
            }

            res = requests.post('https://slack.com/api/chat.postMessage', 
                headers = headers, 
                data = json.dumps(msg)
            )

            print (res.text);