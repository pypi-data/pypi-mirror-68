How to use?
=============

You can use Emit in 5 steps:

.. code-block:: python
    :linenos:

    from emit import Emit, Engine

    async def on_say_hi(msg):
        print(f"{msg} from py-commons-emit!")

    # 1. instantiate Emit exchange
    async def test():
        f = Emit("default")

        # 2. register events and its handler
        await sf.on('say_hi', on_say_hi)

        # 3. start the engine
        await f.start(Engine.IN_PROCESS)

        # or use redis as engine
        # await f.start(Engine.REDIS, dsn="redis://127.0.0.1:6379")

        # 4. emit the event
        await f.emit('say_hi', 'greetings')

    # 5. Now you should get 'greetings from py-commons-emit!' in on_say_hi function.
    asyncio.get_event_loop().run_until_complete(test())
