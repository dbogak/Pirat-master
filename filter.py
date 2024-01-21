from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()


class IsBot(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return types.ChatType.PRIVATE



class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        try:
            supergroup = types.ChatType.SUPERGROUP
        except:
            supergroup = types.ChatType.SUPER_GROUP

        return message.chat.type in (
            types.ChatType.CHANNEL,
            types.ChatType.GROUP,
            supergroup
        )