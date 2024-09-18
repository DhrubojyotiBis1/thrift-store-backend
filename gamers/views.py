from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Gamers

#Global Constants
SUCESS = 'Sucess'

#API Functions
@api_view(['GET'])
def getAll(request):
    ''' API to get all gamers '''
    
    gamers = Gamers.objects.all().values()
    return Response({'message': SUCESS, 'gamers': gamers}, 200)