from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import logging

from shop.models import Album, Artist, Label, About, Review
from shop.serializers import AlbumSerializer, TrackSerializer, ArtistSerializer, LabelSerializer, AboutSerializer, \
    ReviewSerializer

logger = logging.getLogger(__name__)


@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        return Response({'message': 'Hello World!'})


class AlbumListPublic(APIView):
    def get(self, request, format=None):
        albums = Album.objects.all()

        search_query = request.query_params.get('search')
        if search_query:
            albums = albums.filter(
                Q(title__icontains=search_query) |
                Q(artist__name__icontains=search_query) |
                Q(genre__icontains=search_query)
            )

        sort_param = request.query_params.get('sort')
        if sort_param == 'price_asc':
            albums = albums.order_by('price')
        elif sort_param == 'price_desc':
            albums = albums.order_by('-price')
        elif sort_param == 'release_date_asc':
            albums = albums.order_by('year')
        elif sort_param == 'release_date_desc':
            albums = albums.order_by('-year')
        elif sort_param == 'genre':
            albums = albums.order_by('genre')

        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)


class AlbumListAdmin(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetailPublic(APIView):
    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)


class AlbumDetailAdmin(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk, format=None):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumTracksView(APIView):
    def get(self, request, pk, format=None):
        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

        tracks = album.tracks.all()
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)


class ArtistListPublic(APIView):
    def get(self, request, format=None):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)


class ArtistListAdmin(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistDetailPublic(APIView):
    def get_object(self, pk):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        artist = self.get_object(pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)


class ArtistDetailAdmin(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk, format=None):
        artist = self.get_object(pk)
        serializer = ArtistSerializer(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        artist = self.get_object(pk)
        if artist.albums.exists():
            return Response({"error": "Cannot delete artist with existing albums."},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LabelListPublic(APIView):
    def get(self, request, format=None):
        labels = Label.objects.all()
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)


class LabelListAdmin(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabelDetailPublic(APIView):
    def get_object(self, pk):
        try:
            return Label.objects.all().get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        label = self.get_object(pk)
        serializer = LabelSerializer(label)
        return Response(serializer.data)


class LabelDetailAdmin(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk, format=None):
        label = self.get_object(pk)
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        label = self.get_object(pk)
        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AboutView(APIView):
    def get(self, request):
        about = About.objects.first()
        serializer = AboutSerializer(about)
        return Response(serializer.data)


class AlbumReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object_album(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        album = self.get_object_album(pk)
        reviews = Review.objects.filter(album=album)
        serializer = ReviewSerializer(reviews, many=True)
        logger.info(f"{len(reviews)} reviews for album {pk}")
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        album = self.get_object_album(pk)

        try:
            from shop.models import Review
            test_review = Review.objects.create(
                user=request.user,
                album=album,
                rating=5,
                comment="Test"
            )
            logger.info(f"Manual creation successful: {test_review.id}")
            test_review.delete()
        except Exception as e:
            logger.error(f"Manual creation failed: {e}")

        logger.info(f"User type: {type(request.user)}")
        logger.info(f"User value: {request.user}")
        logger.info(f"User id: {getattr(request.user, 'id', 'NO ID')}")

        logger.info(f"Album type: {type(album)}")
        logger.info(f"Album value: {album}")
        logger.info(f"Album id: {album.id}")

        if isinstance(request.user, str):
            try:
                user = User.objects.get(username=request.user)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = request.user

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, album=album)
            logger.info(f"Review created for album {pk} by user {request.user.username}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Failed to create: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
