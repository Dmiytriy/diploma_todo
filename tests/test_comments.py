from django.test import Client
from rest_framework.test import APITestCase
from todolist.core.models import User
from todolist.goals.models import Board, GoalCategory, Goal, BoardParticipant, GoalComment


class GoalApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='new_test', password='test', is_superuser=True)
        cls.test_client = Client()
        cls.response = cls.test_client.login(username='new_test', password='test')

    def create_goal(self):
        board = Board.objects.create(title='test')
        participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([participant])
        category = GoalCategory.objects.create(title='Test', board=board, user=self.user)
        goal = Goal.objects.create(title='Test_goal', category=category, user=self.user)
        return goal

    def create_comment(self):
        goal = self.create_goal()
        comm = GoalComment.objects.create(text='text', goal=goal, user=self.user)
        return comm

    def test_create_comment(self):
        """
        Проверка создания комментария
        """
        url = '/goals/goal_comment/create'
        goal = self.create_goal()
        data = {'text': 'text', 'goal': goal.id, 'user': self.user}
        response = self.test_client.post(url, data)
        assert response.status_code == 201
        assert response.data.get('id') == goal.id

    def test_delete_comment(self):
        """
        Проверка удаления созданного комментария
        """
        comm = self.create_comment()
        url = f'/goals/goal_comment/{comm.id}'
        response = self.test_client.delete(url)
        assert response.status_code == 204
        assert GoalComment.DoesNotExist

    def test_list_comments(self):
        """
        Проверка получения списка комментариев
        """
        url = '/goals/goal_comment/list'
        comm = self.create_comment()
        response = self.test_client.get(url)
        assert response.status_code == 200
        assert response.data[0].get('id') == comm.id

    def test_get_comment_by_id(self):
        """
        Проверка получения комментария пользователя по id
        """
        comm = self.create_comment()
        url = f'/goals/goal_comment/{comm.id}'
        response = self.test_client.get(url)
        assert response.status_code == 200
        assert response.data.get('id') == comm.id
