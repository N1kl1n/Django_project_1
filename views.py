from rest_framework import generics, permissions
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorLDetailSerializer,
)
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft = False).annotate(
            rating_user=models.Count(
                "ratings",
                filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies



class MovieDetailtView(generics.RetrieveAPIView):
    """Вывод фильма"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer



class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзывов к фильму"""

    serializer_class = ReviewCreateSerializer



class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга к фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorsListView(generics.ListAPIView):
    """Вывод спсиска актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorsDetailView(generics.RetrieveAPIView):
    """Вывод описания актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorLDetailSerializer