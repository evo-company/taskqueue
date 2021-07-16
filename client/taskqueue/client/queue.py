from google.protobuf.any_pb2 import Any

from taskqueue.protobuf.service_pb2 import Task
from taskqueue.protobuf.service_grpc import TaskQueueStub


class QueueAdd:

    def __init__(self, authority, task_queue_stub, path):
        self._authority = authority
        self._task_queue_stub = task_queue_stub
        self._path = path

    async def add(self, message, *, queue=None, timeout=None):
        argument = Any()
        argument.Pack(message)
        task = Task(authority=self._authority, method=self._path,
                    argument=argument)
        if queue is not None:
            task.queue = queue
        await self._task_queue_stub.Add(task, timeout=timeout)


class QueueStub:
    __methods__ = {}

    def __init__(self, authority, channel):
        self._authority = authority
        self._task_queue_stub = TaskQueueStub(channel)

        for name, path in self.__methods__.items():
            self.__dict__[name] = QueueAdd(self._authority,
                                           self._task_queue_stub, path)

    @classmethod
    def for_(cls, service_module, service_name):
        service = service_module.DESCRIPTOR.services_by_name[service_name]
        return type('{}Queue'.format(service.name), (cls,), {
            '__methods__': {
                name: '/{}/{}'.format(service.full_name, method.name)
                for name, method in service.methods_by_name.items()
            }
        })
