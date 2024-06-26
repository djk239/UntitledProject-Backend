from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer, SongSerializer, QuizSerializer, ScoreSerializer
from .models import Quiz, Song, Score
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
import spotipy, json, random
from spotipy.oauth2 import SpotifyClientCredentials
from fuzzywuzzy import fuzz
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view

# Initialize Spotipy with credentials
SPOTIPY_CLIENT_ID = '92c197ccced844e0afb389001abc394b'
SPOTIPY_CLIENT_SECRET = 'b71745f784df4b2398557d04a71a7378'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_CLIENT_SECRET))

class SongListCreateAPIView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

class ScoreListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RandomClip(request):
    songs = Song.objects.all()
    if(songs):
        randomClip = random.choice(songs)
        data = {
            'url' : randomClip.audio_link,
            'id' : randomClip.id,
        }
    else:
        data = {
            'error:' : 'None available', 
        }

    return JsonResponse(data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CheckGuess(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            song_id = data.get('id')
            title = data.get('title')
            
            if song_id is None or title is None:
                return JsonResponse({'error': 'ID and title are required.'}, status=400)

            songs = Song.objects.filter(id=song_id)
            matched_song = None
            for song in songs:
                if fuzz.ratio(song.title.lower(), title.lower()) > 80:  # Adjust threshold as needed
                    matched_song = song
                    break

            if matched_song:
                # Update user score (using authenticated user)
                user = request.user  # User object is available due to authentication
                try:
                    score = Score.objects.get(user=user)  # Get existing score object
                    score.score += 1  # Increment score by 1
                    score.save()
                except Score.DoesNotExist:
                    # Create a new score object if it doesn't exist yet
                    score = Score.objects.create(user=user, score=1)
                    score.save()
                return JsonResponse({'message': 'correct.', 'song': {'id': matched_song.id, 'title': matched_song.title, 'artist' : matched_song.artist}}, status=200)
            else:
                return JsonResponse({'message': 'incorrect.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_audio_source(request):
    if request.method == 'GET':
        url = request.GET.get('spotify_url', None)
        if url:
            url = url.split('?')[0]

            track_id = url.split('/')[-1]

            # Get track details
            track_info = sp.track(track_id)

            # Get audio source
            audio_source = track_info['preview_url']
            
            if audio_source:
                return JsonResponse({'audio_source': audio_source})
            else:
                return JsonResponse({'error': 'Audio source not found.'}, status=400)
        else:
            return JsonResponse({'error': 'Missing Spotify URL parameter.'}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are supported.'}, status=405)

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@permission_classes([IsAuthenticated])
def top_scores(request):
    top_users = Score.objects.order_by('-score')[:10]
    serializer = ScoreSerializer(top_users, many=True)
    return JsonResponse(serializer.data, safe=False)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_score(request):
    user = request.user
    try:
        user_score = Score.objects.get(user=user)
        serializer = ScoreSerializer(user_score)
        return JsonResponse(serializer.data)
    except Score.DoesNotExist:
        return JsonResponse({'error': 'User score not found'}, status=404)

