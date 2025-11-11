from django.test import TestCase
from django.contrib.auth.models import User
from music.models import Album, Song
from django.urls import reverse

class AlbumModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create an album for testing
        self.album = Album.objects.create(
            user=self.user,
            artist='Test Artist',
            album_title='Test Album',
            genre='Test Genre',
            album_logo='path/to/album_logo.png',
            is_favorite=True
        )

    def test_album_str(self):
        self.assertEqual(str(self.album), 'Test Album-Test Artist')

    def test_album_defaults(self):
        self.assertTrue(self.album.is_favorite)

    # Add more test methods for other functionality of the Album model

class SongModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create an album for testing
        self.album = Album.objects.create(
            user=self.user,
            artist='Test Artist',
            album_title='Test Album',
            genre='Test Genre',
            album_logo='test/test.jpg',
            is_favorite=True
        )

        # Create a song for testing
        self.song = Song.objects.create(
            album=self.album,
            song_title='Test Song',
            audio_file='test/test.mp3',
            is_favorite=False
        )

    def test_song_str(self):
        self.assertEqual(str(self.song), 'Test Song')

    def test_song_defaults(self):
        self.assertFalse(self.song.is_favorite)

    # Add more test methods for other functionality of the Song model

class IndexViewTestCase(TestCase):
    def test_index_view_with_authenticated_user(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create albums for the user
        album1 = Album.objects.create(user=user, album_title='Album 1', artist='Artist 1')
        album2 = Album.objects.create(user=user, album_title='Album 2', artist='Artist 2')

        # Make a GET request to the index page
        response = self.client.get(reverse('music:index'))

        # Check if the response has the albums in the context
        self.assertEqual(response.status_code, 200)

    def test_index_view_with_unauthenticated_user(self):
        # Make a GET request to the index page
        response = self.client.get(reverse('music:index'))

        # Check if the response redirects to the login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/login.html')

class LoginUserViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_user_with_valid_credentials(self):
        # Make a POST request to the login_user view with valid credentials
        response = self.client.post(reverse('music:login_user'), {'username': self.username, 'password': self.password})

        # Check if the response redirects to the index page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/index.html')

    def test_login_user_with_invalid_credentials(self):
        # Make a POST request to the login_user view with invalid credentials
        response = self.client.post(reverse('music:login_user'), {'username': self.username, 'password': 'wrongpassword'})

        # Check if the response renders the login page with an error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/login.html')
        self.assertContains(response, 'Invalid login')

    def test_login_user_with_inactive_account(self):
        # Deactivate the user account
        self.user.is_active = False
        self.user.save()

        # Make a POST request to the login_user view
        response = self.client.post(reverse('music:login_user'), {'username': self.username, 'password': self.password})

        # Check if the response renders the login page with an error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/login.html')