import edge_tts

# en-US-AnaNeural
# en-US-GuyNeural
# VOICE = "en-US-AnaNeural"
VOICE = "zh-CN-XiaoxiaoNeural"


async def tts_audio_streamer(text: str, voice: str = VOICE):
    communicate = edge_tts.Communicate(text, voice)

    async def audio_streamer():
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")

    return audio_streamer()


async def tts(text: str, key: str, voice: str = VOICE):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(f"./tts_audio/{key}.mp3")
