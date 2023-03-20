import time
import uuid

from fastapi import BackgroundTasks
from loguru import logger
from redis import Redis
from sqlmodel import Session

from app.core.config import settings
from app.core.response import SuccessResult
from app.tools.ChatGPT import ChatBot
from app.tools.tts import tts


class ChatServices:
    def __init__(
        self, session: Session, redis: Redis, background_tasks: BackgroundTasks
    ):
        self.session = session
        self.bot = ChatBot(redis, settings.CHAT_GPT_ACCESS_TOKEN)
        self.tasks = background_tasks

    async def ask(self, message: str):
        logger.info("start ask")
        st = time.time()
        reply = await self.bot.ask(message)

        logger.info(
            f"time: {int(time.time() - st)} seconds",
        )
        return SuccessResult(data={"reply": reply})

    async def ask_stream(self, message: str):
        audio_key = uuid.uuid4().hex
        prev_text = ""
        for data in self.bot.ask_stream(message):
            if not self.bot.chat_conf:
                self.bot.set_chat_conf(data)

            yield data["message"][len(prev_text) :]
            prev_text = data["message"]
        yield f"[AUDIO_KEY]{audio_key}"
        # tts
        self.tasks.add_task(self.reply_to_speech, prev_text, audio_key)

    @classmethod
    async def reply_to_speech(cls, reply_text: str, audio_key: str):
        logger.info("task create tts audio file: {0}".format(audio_key))
        await tts(reply_text, audio_key)
