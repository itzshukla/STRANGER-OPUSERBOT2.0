from pytgcalls.types import Update

from . import queues
from ..clients.clients import app, call
from .streams import run_stream, close_stream


async def run_async_calls():
    @call.on_left()
    @call.on_kicked()
    @call.on_closed_voice_chat()
    async def stream_services_handler(_, chat_id: int):
        await close_stream(chat_id)

    @call.on_stream_end()
    async def stream_end_handler(_, update: Update):
        chat_id = update.chat_id
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            await close_stream(chat_id)
            return

        next_stream = queues.get(chat_id)
        if not next_stream:
            return await close_stream(chat_id)

        file = next_stream.get("file")
        type_ = next_stream.get("type", "Audio")  # Default to Audio if not specified

        try:
            stream = await run_stream(file, type_)
            await call.change_stream(chat_id, stream)
        except Exception as e:
            print(f"[stream_end_handler] Error changing stream in {chat_id}: {e}")
            await close_stream(chat_id)
