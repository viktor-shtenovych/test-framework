# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import adc_driver_pb2 as adc__driver__pb2
import common_pb2 as common__pb2

GRPC_GENERATED_VERSION = '1.64.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in adc_driver_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class AdcDriverStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AdcDriver_InitChannel = channel.unary_unary(
                '/rpc_s32k148.AdcDriver/AdcDriver_InitChannel',
                request_serializer=adc__driver__pb2.ADInitParams.SerializeToString,
                response_deserializer=common__pb2.Status.FromString,
                _registered_method=True)
        self.AdcDriver_ResetInstance = channel.unary_unary(
                '/rpc_s32k148.AdcDriver/AdcDriver_ResetInstance',
                request_serializer=adc__driver__pb2.ADResetParams.SerializeToString,
                response_deserializer=common__pb2.Status.FromString,
                _registered_method=True)
        self.AdcDriver_GetChannelValue = channel.unary_unary(
                '/rpc_s32k148.AdcDriver/AdcDriver_GetChannelValue',
                request_serializer=adc__driver__pb2.ADHandle.SerializeToString,
                response_deserializer=adc__driver__pb2.ADGetValueReturn.FromString,
                _registered_method=True)


class AdcDriverServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AdcDriver_InitChannel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AdcDriver_ResetInstance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AdcDriver_GetChannelValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdcDriverServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AdcDriver_InitChannel': grpc.unary_unary_rpc_method_handler(
                    servicer.AdcDriver_InitChannel,
                    request_deserializer=adc__driver__pb2.ADInitParams.FromString,
                    response_serializer=common__pb2.Status.SerializeToString,
            ),
            'AdcDriver_ResetInstance': grpc.unary_unary_rpc_method_handler(
                    servicer.AdcDriver_ResetInstance,
                    request_deserializer=adc__driver__pb2.ADResetParams.FromString,
                    response_serializer=common__pb2.Status.SerializeToString,
            ),
            'AdcDriver_GetChannelValue': grpc.unary_unary_rpc_method_handler(
                    servicer.AdcDriver_GetChannelValue,
                    request_deserializer=adc__driver__pb2.ADHandle.FromString,
                    response_serializer=adc__driver__pb2.ADGetValueReturn.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc_s32k148.AdcDriver', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('rpc_s32k148.AdcDriver', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AdcDriver(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AdcDriver_InitChannel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/rpc_s32k148.AdcDriver/AdcDriver_InitChannel',
            adc__driver__pb2.ADInitParams.SerializeToString,
            common__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AdcDriver_ResetInstance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/rpc_s32k148.AdcDriver/AdcDriver_ResetInstance',
            adc__driver__pb2.ADResetParams.SerializeToString,
            common__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AdcDriver_GetChannelValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/rpc_s32k148.AdcDriver/AdcDriver_GetChannelValue',
            adc__driver__pb2.ADHandle.SerializeToString,
            adc__driver__pb2.ADGetValueReturn.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
