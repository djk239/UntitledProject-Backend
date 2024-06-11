from django.urls import path
from .views import SongListCreateAPIView, RandomClip, get_audio_source, CheckGuess, SignupView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('songs/', SongListCreateAPIView.as_view(), name='song-list-create'),
    path('songs/random/', RandomClip, name='random-clip'),
    path('getsource/', get_audio_source, name='get_audio_source'),
    path('songs/check/', CheckGuess, name='check_guess'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]