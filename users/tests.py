from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


class UserManagerTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@test.com",
            name="Test",
            last_name="User",
            password='test'
        )
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='', password='test', name="", last_name="")

    def test_create_superuser(self):
        User = get_user_model()
        super_user = User.objects.create_superuser(
            email="test@test.com",
            name="Test",
            last_name="User",
            password='test'
        )
        self.assertEqual(super_user.email, 'test@test.com')
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        self.assertIsNone(super_user.username)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='test@test.com', password='test', name="", last_name="", is_superuser=False)
