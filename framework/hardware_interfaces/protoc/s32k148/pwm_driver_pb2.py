# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pwm_driver.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10pwm_driver.proto\x12\x0brpc_s32k148\x1a\x0c\x63ommon.proto\"b\n\x0cPDInitParams\x12\x13\n\x0binstance_id\x18\x01 \x01(\r\x12\x12\n\nchannel_id\x18\x02 \x01(\r\x12)\n\x08polarity\x18\x03 \x01(\x0e\x32\x17.rpc_s32k148.PDPolarity\"8\n\x11PDSetPeriodParams\x12\x13\n\x0binstance_id\x18\x01 \x01(\r\x12\x0e\n\x06period\x18\x02 \x01(\r\"S\n\x14PDSetDutyCycleParams\x12\x13\n\x0binstance_id\x18\x01 \x01(\r\x12\x12\n\nchannel_id\x18\x02 \x01(\r\x12\x12\n\nduty_cycle\x18\x03 \x01(\r*5\n\nPDPolarity\x12\x12\n\x0ePDPolarity_LOW\x10\x00\x12\x13\n\x0fPDPolarity_HIGH\x10\x01\x32\xf8\x01\n\tPwmDriver\x12I\n\x15PwmDriver_InitChannel\x12\x19.rpc_s32k148.PDInitParams\x1a\x13.rpc_general.Status\"\x00\x12L\n\x13PwmDriver_SetPeriod\x12\x1e.rpc_s32k148.PDSetPeriodParams\x1a\x13.rpc_general.Status\"\x00\x12R\n\x16PwmDriver_SetDutyCycle\x12!.rpc_s32k148.PDSetDutyCycleParams\x1a\x13.rpc_general.Status\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pwm_driver_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PDPOLARITY']._serialized_start=290
  _globals['_PDPOLARITY']._serialized_end=343
  _globals['_PDINITPARAMS']._serialized_start=47
  _globals['_PDINITPARAMS']._serialized_end=145
  _globals['_PDSETPERIODPARAMS']._serialized_start=147
  _globals['_PDSETPERIODPARAMS']._serialized_end=203
  _globals['_PDSETDUTYCYCLEPARAMS']._serialized_start=205
  _globals['_PDSETDUTYCYCLEPARAMS']._serialized_end=288
  _globals['_PWMDRIVER']._serialized_start=346
  _globals['_PWMDRIVER']._serialized_end=594
# @@protoc_insertion_point(module_scope)