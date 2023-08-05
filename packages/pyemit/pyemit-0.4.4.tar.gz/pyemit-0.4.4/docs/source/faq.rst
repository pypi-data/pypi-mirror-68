Frequently asked questions
==========================

Q1. Why design `Emit.on` as decorator to bind event and it's handler, which sounds more nature?

A1. It's very hard to design such a decorator, while both plain python function or class member method could be decorated. Consider the following example:


.. code-block:: python
    :linenos:

    class Foo():
        @on('default', 'say_hi')
        async def foo(self, msg):
            print(msg)

The major task of on as a decorator is, to bind handler ( :meth:`Foo.foo`) , channel 'say_hi' to exchange 'default'. In most occasions, when the decorator (@on) is executed, we don't know if the exchange 'default' is instantiated and where the object is. This is not the hardest part yet. The most hard part is, decorator on will NEVER know which Foo object should the handler (:meth:`Foo.foo`) should bound to, because most likely,  Foo is not instantiated yet. Event though, there's no way for decorator to get the handle of the instantiated object. All things a decorator can got, is arguments (belongs to itself) and the function object to be decorated.

Q2. What type of msg can be pass through?
A2. Any objects that can be json serialized