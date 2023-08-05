Python seems lack of some common building blocks, like convenient config (auto-reload without restart, overriding), in-process event emit and catch mechanism, and etc.

The name py-commons-xxx is inspired by java open source packages -- apache.commons.

py-commons-config
^^^^^^^^^^^^^^^^^^
Features
.........
#. support dev, deployment and test environment
#. auto-reload if config file changed
#. use cfg.settingx.settingy to access config instead of cfg["settingsx"]["settingsy"]

py-commons-emit
^^^^^^^^^^^^^^^^^^^
Features
.........
    A light way for python to fire and consume events.

#. support both in-process and message-server (REDIS for the moment), so if one choose use REDIS as the engine, fire event can communicate inter-process.
#. support multiple message queue(Exchange) by creating multiple Emit instance.
#. easy to use, just on (to bind event and its handler), emit(to fire an event), and start (the start the engine)

py-commons-async-wrapper
^^^^^^^^^^^^^^^^^^^^^^^^^
Features
.........

#. turn obsolete blocking call into asynchronous call, so they can be used with asyncio
