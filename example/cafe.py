import sys
import asyncio

from grpclib.utils import graceful_exit
from grpclib.client import Channel
from grpclib.server import Server
from google.protobuf.empty_pb2 import Empty

from taskqueue.client.queue import QueueStub

import cafe_pb2
import cafe_grpc


HOST = 'grpc.cafe.svc'
PORT = 50051
KNOWN_AS = '{}:{}'.format(HOST, PORT)

TQ_HOST = 'grpc.taskqueue.svc'
TQ_PORT = 50051


CoffeeMachineQueue = QueueStub.for_(cafe_pb2, 'CoffeeMachine')


class CoffeeMachine(cafe_grpc.CoffeeMachineBase):

    async def MakeLatte(self, stream):
        task: cafe_pb2.LatteOrder = await stream.recv_message()
        print('Brewing...')
        await asyncio.sleep(1)
        print('Done!', task)
        await stream.send_message(Empty())


async def start_service():
    loop = asyncio.get_event_loop()
    server = Server([CoffeeMachine()], loop=loop)
    with graceful_exit([server], loop=loop):
        await server.start(HOST, PORT)
        print('Cafe started on {}:{}'.format(HOST, PORT))
        await server.wait_closed()
        print('Exiting...')


async def send_task():
    loop = asyncio.get_event_loop()
    channel = Channel(TQ_HOST, TQ_PORT, loop=loop)
    queue = CoffeeMachineQueue(KNOWN_AS, channel)
    await queue.MakeLatte.add(
        cafe_pb2.LatteOrder(size=cafe_pb2.SMALL, temperature=90, sugar=3),
        queue='default'
    )
    channel.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Provide sub-command: server, test')
    elif sys.argv[1] == 'server':
        asyncio.run(start_service())
    elif sys.argv[1] == 'test':
        asyncio.run(send_task())
    else:
        print('Unknown argument: {}'.format(sys.argv[1]))
