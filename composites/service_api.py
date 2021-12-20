import falcon
from falcon import App

from adapters.api.user_controllers import UserResource, UsersResource
from adapters.api.message_controllers import MessageResource, MessagesResource
from adapters.db.user.storage import UserStorage
from adapters.db.message.storage import MessageStorage
from domain.message.service import MessageService
from domain.user.service import UserService

user_storage = UserStorage()
user_service = UserService(storage=user_storage)

message_storage = MessageStorage()
message_service = MessageService(storage=message_storage)


def create_app() -> App:
    app = falcon.App()

    users_view = UsersResource(service=user_service)
    user_view = UserResource(service=user_service)
    message_view = MessageResource(service=message_service)
    messages_view = MessagesResource(service=message_service)

    app.add_route('/users/', users_view)
    app.add_route('/users/{user_id}', user_view)
    app.add_route('/messages/', messages_view)
    app.add_route('/messages/{message_id}', message_view)
    return app
