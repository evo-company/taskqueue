# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: taskqueue/protobuf/service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='taskqueue/protobuf/service.proto',
  package='taskqueue.service',
  syntax='proto3',
  serialized_pb=_b('\n taskqueue/protobuf/service.proto\x12\x11taskqueue.service\x1a\x19google/protobuf/any.proto\x1a\x1bgoogle/protobuf/empty.proto\"`\n\x04Task\x12\r\n\x05queue\x18\x01 \x01(\t\x12\x11\n\tauthority\x18\x02 \x01(\t\x12\x0e\n\x06method\x18\x03 \x01(\t\x12&\n\x08\x61rgument\x18\x04 \x01(\x0b\x32\x14.google.protobuf.Any2\x82\x01\n\tTaskQueue\x12;\n\x03\x61\x64\x64\x12\x17.taskqueue.service.Task\x1a\x16.google.protobuf.Empty\"\x03\x88\x02\x01\x12\x38\n\x03\x41\x64\x64\x12\x17.taskqueue.service.Task\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='taskqueue.service.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='queue', full_name='taskqueue.service.Task.queue', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='authority', full_name='taskqueue.service.Task.authority', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='method', full_name='taskqueue.service.Task.method', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='argument', full_name='taskqueue.service.Task.argument', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=111,
  serialized_end=207,
)

_TASK.fields_by_name['argument'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['Task'] = _TASK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), dict(
  DESCRIPTOR = _TASK,
  __module__ = 'taskqueue.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:taskqueue.service.Task)
  ))
_sym_db.RegisterMessage(Task)



_TASKQUEUE = _descriptor.ServiceDescriptor(
  name='TaskQueue',
  full_name='taskqueue.service.TaskQueue',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=210,
  serialized_end=340,
  methods=[
  _descriptor.MethodDescriptor(
    name='add',
    full_name='taskqueue.service.TaskQueue.add',
    index=0,
    containing_service=None,
    input_type=_TASK,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=_descriptor._ParseOptions(descriptor_pb2.MethodOptions(), _b('\210\002\001')),
  ),
  _descriptor.MethodDescriptor(
    name='Add',
    full_name='taskqueue.service.TaskQueue.Add',
    index=1,
    containing_service=None,
    input_type=_TASK,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TASKQUEUE)

DESCRIPTOR.services_by_name['TaskQueue'] = _TASKQUEUE

# @@protoc_insertion_point(module_scope)