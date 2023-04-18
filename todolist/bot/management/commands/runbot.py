from django.conf import settings
from django.core.management import BaseCommand

from todolist.bot.models import TgUser
from todolist.bot.tg.client import TgClient
from todolist.bot.tg.schemas import Message
from todolist.goals.models import Goal, GoalCategory

user_states = {'state': {}}
cat_id = []


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1

                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        if tg_user.user:
            self.handle_authorized(tg_user, msg)
        else:
            self.handle_unauthorized(tg_user, msg)

    def handle_unauthorized(self, tg_user: TgUser, msg: Message):
        self.tg_client.send_message(msg.chat.id, 'Подтвердите, пожалуйста, свой аккаунт')
        code = tg_user.set_verification_code()
        self.tg_client.send_message(tg_user.chat_id, f'верификационный код: {code}')

    def handle_authorized(self, tg_user: TgUser, msg: Message):
        allowed_commands = ['/goals', '/create', '/cancel']

        if '/goals' in msg.text:
            self.get_tasks(msg, tg_user)

        elif '/create' in msg.text:
            self.handle_categories(msg, tg_user)

        elif '/cancel' in msg.text:
            self.get_cancel(msg, tg_user)

        elif ('user' not in user_states['state']) and (msg.text not in allowed_commands):
            self.tg_client.send_message(tg_user.chat_id, 'Неизвестная команда')

        elif (msg.text not in allowed_commands) and (user_states['state']['user']) and \
                ('category' not in user_states['state']):
            category = self.handle_save_category(msg, tg_user)
            if category:
                user_states['state']['category'] = category
                self.tg_client.send_message(tg_user.chat_id, f'Выбрана категория {category}. Введите заголовок цели.')

        elif (msg.text not in allowed_commands) and (user_states['state']['user']) and \
                (user_states['state']['category']) and ('goal_title' not in user_states['state']):
            user_states['state']['goal_title'] = msg.text
            goal = Goal.objects.create(title=user_states['state']['goal_title'],
                                       user=user_states['state']['user'],
                                       category=user_states['state']['category'])
            self.tg_client.send_message(tg_user.chat_id, f'Цель {goal} создана в БД')
            del user_states['state']['user']
            del user_states['state']['msg_chat_id']
            del user_states['state']['category']
            del user_states['state']['goal_title']
            cat_id.clear()

    def get_tasks(self, msg: Message, tg_user: TgUser):
        goals = Goal.objects.filter(user=tg_user.user)
        if goals.count() > 0:
            response = [f'#{item.id} {item.title}' for item in goals]
            self.tg_client.send_message(msg.chat.id, '\n'.join(response))
        else:
            self.tg_client.send_message(msg.chat.id, 'список целей пуст')

    def handle_categories(self, msg: Message, tg_user: TgUser):
        categories = GoalCategory.objects.filter(user=tg_user.user)

        if categories.count() > 0:
            cat_text = ''
            for cat in categories:
                cat_text += f'{cat.id}: {cat.title} \n'
                cat_id.append(cat.id)
            self.tg_client.send_message(
                chat_id=tg_user.chat_id,
                text=f'Выберите номер категории для новой цели:\n{cat_text}'
            )
            if 'user' not in user_states['state']:
                user_states['state']['user'] = tg_user.user
                user_states['state']['msg_chat_id'] = tg_user.chat_id

        else:
            self.tg_client.send_message(msg.chat.id, 'список категорий пуст')

    def handle_save_category(self, msg: Message, tg_user: TgUser):
        category_id = int(msg.text)
        category_data = GoalCategory.objects.filter(user=tg_user.user).get(pk=category_id)
        return category_data

    def get_cancel(self, msg: Message, tg_user: TgUser):
        if 'user' in user_states['state']:
            del user_states['state']['user']
            del user_states['state']['msg_chat_id']
            if 'category' in user_states['state']:
                del user_states['state']['category']
            if 'goal_title' in user_states['state']:
                del user_states['state']['goal_title']
        self.tg_client.send_message(tg_user.chat_id, 'Операция отменена')
