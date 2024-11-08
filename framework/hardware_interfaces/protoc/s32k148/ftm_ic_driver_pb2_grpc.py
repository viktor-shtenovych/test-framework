# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import common_pb2 as common__pb2
import ftm_ic_driver_pb2 as ftm__ic__driver__pb2

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
        + f' but the generated code in ftm_ic_driver_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class FtmIcDriverStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FtmIc_DRV_Init = channel.unary_unary(
                '/rpc_s32k148.FtmIcDriver/FtmIc_DRV_Init',
                request_serializer=ftm__ic__driver__pb2.FtmIcInitParams.SerializeToString,
                response_deserializer=common__pb2.Status.FromString,
                _registered_method=True)
        self.FtmIc_DRV_Start = channel.unary_unary(
                '/rpc_s32k148.FtmIcDriver/FtmIc_DRV_Start',
                request_serializer=ftm__ic__driver__pb2.FtmIcHandle.SerializeToString,
                response_deserializer=common__pb2.Status.FromString,
                _registered_method=True)
        self.FtmIc_DRV_Stop = channel.unary_unary(
                '/rpc_s32k148.FtmIcDriver/FtmIc_DRV_Stop',
                request_serializer=ftm__ic__driver__pb2.FtmIcHandle.SerializeToString,
                response_deserializer=common__pb2.Status.FromString,
                _registered_method=True)


class FtmIcDriverServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FtmIc_DRV_Init(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FtmIc_DRV_Start(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FtmIc_DRV_Stop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FtmIcDriverServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FtmIc_DRV_Init': grpc.unary_unary_rpc_method_handler(
                    servicer.FtmIc_DRV_Init,
                    request_deserializer=ftm__ic__driver__pb2.FtmIcInitParams.FromString,
                    response_serializer=common__pb2.Status.SerializeToString,
            ),
            'FtmIc_DRV_Start': grpc.unary_unary_rpc_method_handler(
                    servicer.FtmIc_DRV_Start,
                    request_deserializer=ftm__ic__driver__pb2.FtmIcHandle.FromString,
                    response_serializer=common__pb2.Status.SerializeToString,
            ),
            'FtmIc_DRV_Stop': grpc.unary_unary_rpc_method_handler(
                    servicer.FtmIc_DRV_Stop,
                    request_deserializer=ftm__ic__driver__pb2.FtmIcHandle.FromString,
                    response_serializer=common__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc_s32k148.FtmIcDriver', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('rpc_s32k148.FtmIcDriver', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class FtmIcDriver(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FtmIc_DRV_Init(request,
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
            '/rpc_s32k148.FtmIcDriver/FtmIc_DRV_Init',
            ftm__ic__driver__pb2.FtmIcInitParams.SerializeToString,
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
    def FtmIc_DRV_Start(request,
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
            '/rpc_s32k148.FtmIcDriver/FtmIc_DRV_Start',
            ftm__ic__driver__pb2.FtmIcHandle.SerializeToString,
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
    def FtmIc_DRV_Stop(request,
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
            '/rpc_s32k148.FtmIcDriver/FtmIc_DRV_Stop',
            ftm__ic__driver__pb2.FtmIcHandle.SerializeToString,
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