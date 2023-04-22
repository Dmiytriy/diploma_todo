import json
from rest_framework.test import APITestCase
from todolist.core.models import User


class CoreApiTestCase(APITestCase):

    def create_user(self):
        password = 'qwerty123!'
        user = User.objects.create_user(username='test', password=password)
        return user, password

    def test_signup(self):
        url = '/core/signup'
        response = self.client.post(url,
                                    {'username': 'test', 'password': 'qwerty123!', 'password_repeat': 'qwerty123!'})
        assert response.status_code == 201

    def test_login(self):
        """
        Проверка успешной аутентификации пользователя
        """
        url = '/core/login'
        user, password = self.create_user()
        response = self.client.post(url, {'username': user.username, 'password': password})
        assert response.status_code == 200
        assert response.data.get('username') == user.username

    def test_profile_get(self):
        """
        Проверка получения профиля пользователя
        """
        url = '/core/profile'
        user, password = self.create_user()
        self.client.login(username=user, password=password)
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data.get('id') == user.id

    def test_profile(self):
        """
        Проверка успешного обновления параметров пользователя
        """
        url = '/core/profile'
        user, password = self.create_user()
        self.client.login(username=user, password=password)
        first_name = 'test'
        last_name = 'test'
        response = self.client.put(url, json.dumps({'username': user.username, 'first_name': first_name,
                                                    'last_name': last_name}), content_type='application/json')
        assert response.status_code == 200
        assert User.objects.get(id=user.id).first_name == first_name

    def test_update_password(self):
        """
        Проверка успешного обновления пароля пользователя
        """
        url = '/core/update_password'
        user, password = self.create_user()
        self.client.login(username=user, password=password)
        new_password = 'qwerty111!'
        response = self.client.put(url, json.dumps({'old_password': password, 'new_password': new_password}),
                                                    content_type='application/json')

        assert response.status_code == 200
        logged_in = self.client.login(username=user.username, password=new_password)
        assert logged_in
