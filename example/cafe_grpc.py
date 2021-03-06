# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: cafe.proto
# plugin: grpclib.plugin.main
import abc

import grpclib.const
import grpclib.client

import google.protobuf.empty_pb2
import cafe_pb2


class CoffeeMachineBase(abc.ABC):

    @abc.abstractmethod
    async def MakeLatte(self, stream):
        pass

    def __mapping__(self):
        return {
            '/coffemachine.CoffeeMachine/MakeLatte': grpclib.const.Handler(
                self.MakeLatte,
                grpclib.const.Cardinality.UNARY_UNARY,
                cafe_pb2.LatteOrder,
                google.protobuf.empty_pb2.Empty,
            ),
        }


class CoffeeMachineStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.MakeLatte = grpclib.client.UnaryUnaryMethod(
            channel,
            '/coffemachine.CoffeeMachine/MakeLatte',
            cafe_pb2.LatteOrder,
            google.protobuf.empty_pb2.Empty,
        )
