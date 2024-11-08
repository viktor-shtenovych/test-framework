# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import common_pb2 as common__pb2
import mpc5777c_eqadc_driver_pb2 as mpc5777c__eqadc__driver__pb2

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
        + f' but the generated code in mpc5777c_eqadc_driver_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class EqAdcDriverStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.EQADC_DRV_CC_Init = channel.unary_unary(
                '/rpc_mpc5777c.EqAdcDriver/EQADC_DRV_CC_Init',
                request_serializer=mpc5777c__eqadc__driver__pb2.EqAdcInitParams.SerializeToString,
                response_deserializer=common__pb2.Status.FromString,
                _registered_method=True)
        self.EQADC_DRV_CC_CalibrateConverter = channel.unary_unary(
                '/rpc_mpc5777c.EqAdcDriver/EQADC_DRV_CC_CalibrateConverter',
                request_serializer=mpc5777c__eqadc__driver__pb2.EqAdcCcCalibrateConverterParams.SerializeToString,
                response_deserializer=common__pb2.Status.FromString,
                _registered_method=True)
        self.EQADC_DRV_CC_SamplesRequest = channel.unary_unary(
                '/rpc_mpc5777c.EqAdcDriver/EQADC_DRV_CC_SamplesRequest',
                request_serializer=mpc5777c__eqadc__driver__pb2.EqAdcCCSamplesRequestParams.SerializeToString,
                response_deserializer=common__pb2.Status.FromString,
                _registered_method=True)


class EqAdcDriverServicer(object):
    """Missing associated documentation comment in .proto file."""

    def EQADC_DRV_CC_Init(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EQADC_DRV_CC_CalibrateConverter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EQADC_DRV_CC_SamplesRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EqAdcDriverServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'EQADC_DRV_CC_Init': grpc.unary_unary_rpc_method_handler(
                    servicer.EQADC_DRV_CC_Init,
                    request_deserializer=mpc5777c__eqadc__driver__pb2.EqAdcInitParams.FromString,
                    response_serializer=common__pb2.Status.SerializeToString,
            ),
            'EQADC_DRV_CC_CalibrateConverter': grpc.unary_unary_rpc_method_handler(
                    servicer.EQADC_DRV_CC_CalibrateConverter,
                    request_deserializer=mpc5777c__eqadc__driver__pb2.EqAdcCcCalibrateConverterParams.FromString,
                    response_serializer=common__pb2.Status.SerializeToString,
            ),
            'EQADC_DRV_CC_SamplesRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.EQADC_DRV_CC_SamplesRequest,
                    request_deserializer=mpc5777c__eqadc__driver__pb2.EqAdcCCSamplesRequestParams.FromString,
                    response_serializer=common__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc_mpc5777c.EqAdcDriver', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('rpc_mpc5777c.EqAdcDriver', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class EqAdcDriver(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def EQADC_DRV_CC_Init(request,
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
            '/rpc_mpc5777c.EqAdcDriver/EQADC_DRV_CC_Init',
            mpc5777c__eqadc__driver__pb2.EqAdcInitParams.SerializeToString,
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
    def EQADC_DRV_CC_CalibrateConverter(request,
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
            '/rpc_mpc5777c.EqAdcDriver/EQADC_DRV_CC_CalibrateConverter',
            mpc5777c__eqadc__driver__pb2.EqAdcCcCalibrateConverterParams.SerializeToString,
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
    def EQADC_DRV_CC_SamplesRequest(request,
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
            '/rpc_mpc5777c.EqAdcDriver/EQADC_DRV_CC_SamplesRequest',
            mpc5777c__eqadc__driver__pb2.EqAdcCCSamplesRequestParams.SerializeToString,
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
