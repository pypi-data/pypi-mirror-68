Redis Watchdog
==============

This project allow to monitor Redis keys for changes and launch callbacks.

Install
=======

.. code-block:: console

    $ pip install aioredis-watchdog


Concepts
========

Redis pattern
-------------

You can configure which Redis keys you wish to watch by using a *redis pattern*.

Callbacks
---------

Each time a key was changed in Redis, `aioredis-watchdog` will call the list of callbacks.

Using as library
================

For monitoring all Redis keys that starts by *user-*:

.. code-block:: python

    import asyncio

    from aioredis_watchdog import watchdog

    async def callback1(key: str, data: bytes):
        print("Key callback 1: ", key, "#", data)

    async def callback2(key: str, data: bytes):
        print("Key callback 2: ", key, "#", data)

    async def monitoring(connection_string: str):
        redis = await aioredis.create_redis_pool(connection_string)

        callbacks = [callback1, callback2]

        await watchdog("user-*", callbacks, redis)

    asyncio.run(monitoring("redis://localhost"))

Callbacks must have this signature:

.. code-block:: python

    async def FUNCTION_NAME(KEY: str, VALUE: bytes):
        ...

Where:

- Function is a coroutine
- KEY: is the key name in redis and is plain string
- VALUE: is the value for this key in Redis. It's in bytes format.

You also can config the maximum number of processing packages for `watchdog`.

In this example only 10 changes will be processed:

.. code-block:: python

    ...

    await watchdog("user-*", callbacks, redis, count=10)

    ...

Using as CLI
============

You also can use the library as cli. When you install the package a new command will be available: `redis-watchdog`:

.. code-block:: console

    $ redis-watchdog -h

Usage in a pipeline
-------------------

You can use redis-watchdog in a *NIX pipeline. You only must set the parameter `-P` to activate it.

At the next step in the pipeline the string "KEY VALUE" will be received. Let me illustrate using an example:

.. code-block:: console

    $ redis-watcher -q -P -c 10 | awk '{print $1" ### "$2}'
    x6777 ### 80c853a94a0d41ac886ad77ab6441484
    x6778 ### afd97f42cbad45a08468e03b3189f753
    x6779 ### 26a62f14e9224ed2a429f946a0712f57
    x6780 ### b1da88cf24354f77a8ebefc960db1dcc
    x6781 ### 2aac5c5f60884025b307f1639ac0392f
    x6782 ### 0657604ac8b247e099a6ff1ea7087dc6
    x6783 ### f582353a5b3544109fec1a49624fe6bd
    x6784 ### 09deb8da158a4ab5bd45d889fb3907b0
    x6785 ### 82c8e99b83cf47b0928cabce67a24c54
    x6786 ### 541a36e4efee4a65a4c84c95af23ecee
    x6787 ### 77c89aaec0e94e588726ab3dbf71a6d4

Oks, let explain the rest of the flags:

- `-q` to enable quiet mode.
- `-P` to enable pipeline mode
- `-c` to limit events to process to 10.

To generate data the script `data_producer.py` at the `examples/` folder was used.

Another example:

Call an end-point by each key:

.. code-block:: console

    $ redis-watcher -q -P -c 10 | awk '{print "http://mysite.com/callback?key="$1"&value="$2}' | xargs -n1 wget -O - -q



