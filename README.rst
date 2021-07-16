TaskQueue as a service for any gRPC service

Basically, you call ``taskqueue`` service to ask it to call you back later. And
retry that call if necessary. So you don't have to implement AMQP- or
Kafka-related stuff in every service you create.

Overview
~~~~~~~~

This repository consists of three sub-projects:

- ``/client`` - tiny and optional client library
- ``/server`` - server application
- ``/protobuf`` - message types definition for talking to ``taskqueue`` service

Client targets services, written using Python >=3.5 and `grpclib`_.

Server requires Python >=3.5 and is written using grpclib_ and aiokafka_.

Server consists of two services:

- gRPC handler: receives requests and produces events in Kafka
- Kafka consumer: receives events from Kafka and sends them as gRPC calls to
  callers

Server requires Kafka to produce and consume persistently stored events. Server
supports "at least once" and "at most once" delivery guaranties. If you need
"exactly once" guarantee, use Kafka or something else directly.


Client
~~~~~~

Clients can use already generated
``taskqueue.protobuf.service_grpc.TaskQueueStub`` for async
services (``grpclib``), or
``taskqueue.protobuf.service_pb2_grpc.TaskQueueStub`` for sync services
(``grpcio``).

There is a tiny client for async services: ``taskqueue.client``

.. code-block:: shell

    $ pip3 install taskqueue-client

Full working example can be found in ``example`` directory. Short overview:

.. code-block:: python

    import cafe_pb2  # client's messages

    from taskqueue.client.queue import QueueStub

    # `CoffeeMachine` is a client's service name
    CoffeeMachineQueue = QueueStub.for_(cafe_pb2, 'CoffeeMachine')

    queue = CoffeeMachineQueue(
        # authority, client is known to be reachable at this address
        'cafe.srv.prod:50051',
        # channel to the TaskQueue service
        Channel('taskqueue.srv.prod', 50051, loop=loop),
    )

    # ... and then, somewhere in your code:

    # `make_latte` - is a name of a method, which should be called by TaskQueue
    # later, to handle `LatteOrder` task. This method should accept
    # `LatteOrder` message and return `google.protobuf.Empty` message.
    await queue.make_latte.add(
        cafe_pb2.LatteOrder(size=cafe_pb2.SMALL, temperature=90, sugar=3),
        queue='default',  # here you can override default queue name
    )

In this example we have a service ``cafe``, which implements
``coffemachine.CoffeeMachine`` service protocol. This protocol has one gRPC
method: ``/coffemachine.CoffeeMachine/make_latte``.

We want to call this method, but we don't want to synchronously wait for it's
completion. So we're asking TaskQueue to make this call for us:

.. code-block:: text

    POST /taskqueue.service.TaskQueue/add
    :authority taskqueue.srv.prod:50051
    taskqueue.protobuf.service_pb2.Task(
        authority='cafe.srv.prod:50051',
        method='/coffemachine.CoffeeMachine/make_latte',
        argument=cafe_pb2.LatteOrder(size=cafe_pb2.SMALL,
                                     temperature=90, sugar=3),
    )

TaskQueue will append this task to the Kafka topic and then this task will be
consumed and our service will be called:

.. code-block:: text

    POST /coffemachine.CoffeeMachine/make_latte
    :authority cafe.srv.prod:50051
    cafe_pb2.LatteOrder(size=cafe_pb2.SMALL,
                        temperature=90, sugar=3)

Server
~~~~~~

Server assumes that Kafka configured to auto-create topics. TaskQueue uses
topics which are looks like this: ``taskqueue.{authority}.{queue}``. Usually
``queue`` is equal to ``default``, but clients can dynamically and implicitly
create as many queues as they require. ``authority`` looks like an address,
which is used to reach caller service, for example ``greeter.srv.prod.50051``.

To configure server edit ``config.yaml`` file. See this project for more
information: https://github.com/vmagamedov/strictconf

To start gRPC handler:

.. code-block:: shell

    $ python3 -m taskqueue.server config.yaml@dev rpc

To start Kafka consumer:

.. code-block:: shell

    $ python3 -m taskqueue.server config.yaml@dev worker

.. _grpclib: https://github.com/vmagamedov/grpclib
.. _aiokafka: https://github.com/aio-libs/aiokafka
