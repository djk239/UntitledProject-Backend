from django.urls import path
from .views import SongListCreateAPIView, RandomClip, get_audio_source, CheckGuess, SignupView, ScoreListCreateAPIView, top_scores, user_score
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('songs/', SongListCreateAPIView.as_view(), name='song-list-create'),
    path('songs/<int:pk>/', SongListCreateAPIView.as_view(), name='song-playable-update'),
    path('score/', ScoreListCreateAPIView.as_view(), name='score-list-create'),
    path('songs/random/', RandomClip, name='random-clip'),
    path('getsource/', get_audio_source, name='get_audio_source'),
    path('songs/check/', CheckGuess, name='check_guess'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('top-scores/', top_scores, name='top_scores'),
    path('user-score/', user_score, name='userscore'),
]