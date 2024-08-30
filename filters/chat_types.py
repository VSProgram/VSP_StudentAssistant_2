from aiogram.filters import Filter
from aiogram import Bot, types
from aiogram.methods.get_chat_member import GetChatMember

chat_id = -1002168145795


# class IsAdmin(Filter):
#     def __init__(self) -> None:
#         pass
#
#     async def __call__(self, message: types.Message, bot: Bot) -> bool:
#         return message.from_user.id in bot.my_admins_list

class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        admins_list = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
        print(admins_list.status)

        return admins_list.status in [admins_list.status.CREATOR,admins_list.status.ADMINISTRATOR]


# class IsUser(Filter):
#     def __init__(self) -> None:
#         pass
#
#
#     async def __call__(self, message: types.Message, bot: Bot) -> bool:
#         admins_list = await bot.get_chat_member(-1002168145795, user_id=message.from_user.id)
#         if admins_list.status != 'left' or 'kicked':
#             print(admins_list.status)
#         if admins_list.status != 'left' or 'kicked':
#             return message

class IsUser(Filter):
    def __init__(self) -> None:
        pass


    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        admins_list = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
        print(admins_list.status)
        return admins_list.status not in [admins_list.status.LEFT,admins_list.status.KICKED,admins_list.status.CREATOR,admins_list.status.ADMINISTRATOR]