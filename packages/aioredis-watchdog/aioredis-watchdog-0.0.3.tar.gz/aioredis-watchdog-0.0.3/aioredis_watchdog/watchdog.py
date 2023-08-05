import asyncio

from typing import List, Callable

import aioredis


async def watchdog(redis_pattern: str,
                   callbacks: List[Callable],
                   redis_connection: aioredis.commands.Redis,
                   count: int = -1):
    """
    Usage:

    >>> async def print_modified(key: str, value: bytes):
            print("Key: ", key, "- Value", value)
    >>> await watchdog("*", print_modified, redis)
    """
    # Config redis for callbacks
    await redis_connection.config_set("notify-keyspace-events", "KEA")

    mpsc = aioredis.pubsub.Receiver()
    await redis_connection.psubscribe(mpsc.pattern(redis_pattern))

    events_count = 0

    async for channel, msg in mpsc.iter():

        if count != -1 and events_count > count:
            break

        value, operation = msg

        if operation == b"set":

            events_count += 1

            _value = value.decode("UTF-8")
            modified_key = _value[_value.find("__:") + 3:]
            modified_value = await redis_connection.get(modified_key)

            for cb in callbacks:
                asyncio.create_task(cb(modified_key, modified_value))

__all__ = ("watchdog",)
