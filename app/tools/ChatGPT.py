import orjson
import redis
from revChatGPT.V1 import Chatbot


class ChatBot:
    CONF_KEY = 'ChatBot:AccessToken:{}'

    def __init__(self, redis_client, access_token: str):
        self.redis = redis_client
        self.access_token = access_token
        self.chat_bot = Chatbot(config={"access_token": access_token})
        self.chat_conf = self.get_chat_conf()

    def get_chat_conf(self) -> dict:
        chat_conf = self.redis.get(self.CONF_KEY.format(self.access_token))
        if chat_conf:
            return orjson.loads(chat_conf)
        return {}

    def set_chat_conf(self, data):
        chat_conf = {"conversation_id": data["conversation_id"], }
        self.redis.set(self.CONF_KEY.format(self.access_token), orjson.dumps(chat_conf))
        self.chat_conf = chat_conf

    def ask(self, prompt: str):

        prev_text = ""
        for data in self.chat_bot.ask(
                prompt,
                conversation_id=self.chat_conf.get("conversation_id"),
        ):
            if not self.chat_conf:
                self.set_chat_conf(data)

            prev_text = data["message"]

        return prev_text

    def ask_stream(self, prompt: str):
        yield from self.chat_bot.ask(
            prompt,
            conversation_id=self.chat_conf.get("conversation_id"),
        )


if __name__ == '__main__':
    redis = redis.Redis()
    _access_token = ""
    bot = ChatBot(redis, _access_token)
    print(bot.ask("How do you today"))
