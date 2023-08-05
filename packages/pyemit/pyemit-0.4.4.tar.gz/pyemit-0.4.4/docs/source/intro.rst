Introduction
=============

Features
^^^^^^^^^^^
    A light way for python to fire and consume events.

    * support both in-process and message-server (REDIS for the moment), so if one choose use REDIS as the engine, fire event can communicate inter-process.
    * support multiple message queue(Exchange) by creating multiple Emit instance.
    * simple APIs, just on (to bind event and its handler), emit(to fire an event), and start (the start the engine)

How Emit works?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    First of wall, you register events and its handler by using :meth:`Emit.on`, then your start the Emit exchange. Emit will create communication channels under the hood, and bind channel name, handler to the channel.

    All these information are stored at the exchange (A Emit instance). When the under layer communication channel received information, Emit find the handler according to the registry, then invoke handler with received data.

    Each channel(event) may have one or more handler bound, they will be called by the order they're registered.

    Now you fire an event. The event will go to either an asyncio queue, or redis server, and be bounced back to bounded channels, which are created by :meth:`Emit.bind_channel` previously, and your events( messages) will be put into these channels, with each queue, we'll have an asyncio task :meth:`Emit.receiver` to dispacth events to bounded handlers.

    when you need to shutdown a channel, send a None to this channel.

    To shutdown the exchange itself, please call :meth:`Emit.stop`.

