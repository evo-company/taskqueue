import re
import logging
import asyncio

from aiokafka import AIOKafkaConsumer, ConsumerRebalanceListener
from grpclib.const import Cardinality
from grpclib.utils import graceful_exit
from grpclib.client import Channel
from grpclib.exceptions import GRPCError
from grpclib.encoding.proto import ProtoCodec
from google.protobuf.any_pb2 import Any
from google.protobuf.empty_pb2 import Empty

from taskqueue.protobuf.service_pb2 import Task

from .utils import delay_gen
from .config import Config


log = logging.getLogger(__name__)


class Pool:
    """
    TODO:
    - implement multitasking
    """
    _low_water_mark = 5
    _high_water_mark = 20

    def __init__(self, *, loop):
        self._loop = loop
        self._queues = {}
        self._tasks = {}

    def partitions(self):
        # TODO: fair partitions selection
        return [queue for queue in self._queues.values()
                if self._low_water_mark < queue.qsize() < self._high_water_mark]

    def start(self, partition):
        pass

    def stop(self, partition):
        pass


class AnyCodec(ProtoCodec):

    def encode(self, message, message_type):
        assert message_type is Any, message_type
        return message.value


class Listener(ConsumerRebalanceListener):

    def __init__(self, pool):
        self._pool = pool

    def on_partitions_assigned(self, assigned):
        for partition in assigned:
            self._pool.start(partition)

    def on_partitions_revoked(self, revoked):
        for partition in revoked:
            self._pool.stop(partition)


class MessageWrapper:

    def __init__(self, value):
        self._value = value

    def SerializeToString(self):
        return self._value


class Sender:
    """
    TODO:
    - resolve IPs and create less channels
    """
    def __init__(self, *, loop):
        self._loop = loop
        self._channels = {}
        self._channel_lock = asyncio.Lock(loop=loop)

    async def send(self, authority, method, message: Any, *, timeout=None):
        if authority not in self._channels:
            async with self._channel_lock:
                if authority not in self._channels:
                    host, _, port = authority.partition(':')
                    self._channels[authority] = Channel(
                        host, port,
                        loop=self._loop,
                        codec=AnyCodec(),
                    )
        channel = self._channels[authority]
        stream_ctx = channel.request(
            method, Cardinality.UNARY_UNARY, Any, Empty, timeout=timeout,
        )
        async with stream_ctx as stream:
            await stream.send_message(message, end=True)
            await stream.recv_message()


class Worker:
    _task = None
    _send_timeout = 30

    def __init__(self, consumer, group, *, loop):
        self._consumer = consumer
        self._group_id = group
        self._loop = loop
        self._sender = Sender(loop=loop)
        self._pool = Pool(loop=self._loop)
        self._listener = Listener(pool=self._pool)

    async def _body(self):
        self._consumer.subscribe(pattern=rf'^{re.escape(self._group_id)}\.',
                                 listener=self._listener)
        async for message in self._consumer:
            delay = delay_gen()
            while True:
                task: Task = Task.FromString(message.value)
                log.info('Received task %s%s', task.authority, task.method)
                try:
                    await self._sender.send(
                        task.authority,
                        task.method,
                        task.argument,
                        timeout=self._send_timeout,
                    )
                except (GRPCError, asyncio.TimeoutError) as exc:
                    retry_interval = next(delay)
                    log.error('Failed to push the task: %s%s, %r, retry in %ds',
                              task.authority, task.method, exc, retry_interval)
                    await asyncio.sleep(retry_interval, loop=self._loop)
                else:
                    log.info('Successfully pushed task: %s%s',
                             task.authority, task.method)
                    await self._consumer.commit()
                    break

    async def _body_wrapper(self):
        try:
            await self._body()
        except asyncio.CancelledError:
            log.info('Exit complete')
        except Exception:
            log.exception('Unexpected error, exiting...')

    async def start(self):
        self._task = self._loop.create_task(self._body_wrapper())

    def close(self):
        self._task.cancel()

    async def wait_closed(self):
        await asyncio.wait([self._task], loop=self._loop)


async def main(cfg: Config):
    loop = asyncio.get_event_loop()

    consumer = AIOKafkaConsumer(
        loop=loop,
        bootstrap_servers=cfg.main.kafka_hosts,
        group_id=cfg.main.kafka_group,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
    )
    await consumer.start()
    log.info('Consumer started: %s', ', '.join(cfg.main.kafka_hosts))

    worker = Worker(consumer, cfg.main.kafka_group, loop=loop)
    with graceful_exit([worker], loop=loop):
        await worker.start()
        log.info('Worker started')
        await worker.wait_closed()
        log.info('Exiting...')
        await consumer.stop()
