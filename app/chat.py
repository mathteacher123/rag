from typing import cast

import chainlit as cl
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from llama_index.core.query_engine import RetrieverQueryEngine

# Must be set before the engine module is imported so its singletons
# (retriever + response synthesizer) pick up the Chainlit handler.
Settings.callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])

from app.services.rag.engine import query_engine  # noqa: E402


@cl.on_chat_start
async def start() -> None:
    cl.user_session.set("query_engine", query_engine)
    await cl.Message(
        author="Assistant",
        content="Hello! Im an AI assistant. How may I help you?",
    ).send()


@cl.on_message
async def main(message: cl.Message) -> None:
    query_engine = cast(
        "RetrieverQueryEngine",
        cl.user_session.get("query_engine"),
    )
    msg = cl.Message(content="", author="Assistant")

    try:
        res = await cl.make_async(query_engine.query)(message.content)
        for token in res.response_gen:
            await msg.stream_token(token)
    except Exception as exc:  # surface DB/LLM errors in-chat instead of crashing
        await msg.stream_token(f"Error: {exc}")

    await msg.send()
