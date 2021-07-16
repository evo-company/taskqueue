import asyncio
import logging

from aiokafka import AIOKafkaProducer
from grpclib.utils import graceful_exit
from grpclib.server import Server
from google.protobuf.empty_pb2 import Empty
from grpclib.reflection.service import ServerReflection

from taskqueue.protobuf.service_pb2 import Task
from taskqueue.protobuf.service_grpc import TaskQueueBase

from .config import Config


log = logging.getLogger(__name__)

DEFAULT_QUEUE = 'default'


class TaskQueue(TaskQueueBase):

    def __init__(self, producer, group):
        self._producer = producer
        self._group = group

    async def add(self, stream):
        # backward compatibility
        await self.Add(stream)

    async def Add(self, stream):
        task: Task = await stream.recv_message()
        assert task.authority, task
        topic = '{group_id}.{service_id}.{queue}'.format(
            group_id=self._group,
            service_id=task.authority.replace(':50051', '').replace(':', '.'),
            queue=task.queue or DEFAULT_QUEUE,
        )
        log.info('Sending task into topic: %s', topic)
        await self._producer.send_and_wait(topic, task.SerializeToString())
        log.info('Task successfully sent into topic: %s', topic)
        await stream.send_message(Empty())


async def main(cfg: Config, *, host=None, port=None):
    host = host or '0.0.0.0'
    port = port or 50051
    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=cfg.main.kafka_hosts,
    )
    await producer.start()
    log.info('Producer started: %s', ', '.join(cfg.main.kafka_hosts))

    task_queue = TaskQueue(producer, cfg.main.kafka_group)
    services = ServerReflection.extend([task_queue])
    server = Server(services, loop=loop)
    with graceful_exit([server], loop=loop):
        await server.start(host, port)
        log.info('gRPC server listening on %s:%s', host, port)
        await server.wait_closed()
        log.info('Exiting...')
        await producer.stop()
