from rest_framework.test import APITestCase
from django.test import Client
from todolist.core.models import User
from todolist.goals.models import Board, BoardParticipant


class BoardsApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='new_user', password='qwerty', is_superuser=True)
        cls.test_client = Client()
        cls.response = cls.test_client.login(username='new_user', password='qwerty')

    def create_board(self):
        board = Board.objects.create(title='new_title')
        participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([participant])
        return board

    def test_to_create(self):
        """
        Проверка создания доски
        """

        url = '/goals/board/create'
        title = 'New_board'
        response = self.test_client.post(url, {'title': title})
        assert response.status_code == 201
        assert response.data.get('title'), title

    def test_delete_boards(self):
        """
        Проверка удаления доски
        """

        board = self.create_board()
        url = f'/goals/board/{board.id}'
        response = self.test_client.delete(url)
        assert response.status_code == 204
        assert Board.objects.get(id=board.id).is_deleted

    def test_list_boards(self):
        """
        Проверка получения списка досок
        """
        url = '/goals/board/list'
        board = self.create_board()
        response = self.test_client.get(url)
        assert response.status_code == 200
        assert response.data[0].get('id') == board.id

    def test_by_pk_boards(self):
        """
        Проверка получения доски по id
        """
        board = self.create_board()
        url = f'/goals/board/{board.id}'
        response = self.test_client.get(url)
        assert response.status_code == 200
        assert response.data.get('id') == board.id
