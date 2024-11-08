# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: s32k148_pins_driver.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19s32k148_pins_driver.proto\x12\x0brpc_s32k148\x1a\x0c\x63ommon.proto\"r\n\x10PinSettingConfig\x12\x0e\n\x06pin_id\x18\x01 \x01(\r\x12\x0f\n\x07port_id\x18\x02 \x01(\r\x12)\n\tdirection\x18\x03 \x01(\x0e\x32\x16.rpc_s32k148.Direction\x12\x12\n\ninit_value\x18\x04 \x01(\r\",\n\tPortIrqId\x12\x0f\n\x07port_id\x18\x01 \x01(\r\x12\x0e\n\x06irq_id\x18\x02 \x01(\x05\"c\n\x15PinSetDirectionParams\x12\x0e\n\x06pin_id\x18\x01 \x01(\r\x12\x0f\n\x07port_id\x18\x02 \x01(\r\x12)\n\tdirection\x18\x03 \x01(\x0e\x32\x16.rpc_s32k148.Direction\"@\n\x0ePinWriteParams\x12\x0e\n\x06pin_id\x18\x01 \x01(\r\x12\x0f\n\x07port_id\x18\x02 \x01(\r\x12\r\n\x05value\x18\x03 \x01(\r\"h\n\x0ePinsInitParams\x12-\n\x06\x63onfig\x18\x01 \x03(\x0b\x32\x1d.rpc_s32k148.PinSettingConfig\x12\'\n\x07irq_ids\x18\x02 \x03(\x0b\x32\x16.rpc_s32k148.PortIrqId*7\n\tDirection\x12\n\n\x06\x46SW_IN\x10\x00\x12\x0b\n\x07\x46SW_OUT\x10\x01\x12\x11\n\rFSW_UNDEFINED\x10\x02\x32\xee\x01\n\nPinsDriver\x12\x43\n\rPINS_DRV_Init\x12\x1b.rpc_s32k148.PinsInitParams\x1a\x13.rpc_general.Status\"\x00\x12R\n\x15PINS_DRV_SetDirection\x12\".rpc_s32k148.PinSetDirectionParams\x1a\x13.rpc_general.Status\"\x00\x12G\n\x11PINS_DRV_WritePin\x12\x1b.rpc_s32k148.PinWriteParams\x1a\x13.rpc_general.Status\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 's32k148_pins_driver_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DIRECTION']._serialized_start=491
  _globals['_DIRECTION']._serialized_end=546
  _globals['_PINSETTINGCONFIG']._serialized_start=56
  _globals['_PINSETTINGCONFIG']._serialized_end=170
  _globals['_PORTIRQID']._serialized_start=172
  _globals['_PORTIRQID']._serialized_end=216
  _globals['_PINSETDIRECTIONPARAMS']._serialized_start=218
  _globals['_PINSETDIRECTIONPARAMS']._serialized_end=317
  _globals['_PINWRITEPARAMS']._serialized_start=319
  _globals['_PINWRITEPARAMS']._serialized_end=383
  _globals['_PINSINITPARAMS']._serialized_start=385
  _globals['_PINSINITPARAMS']._serialized_end=489
  _globals['_PINSDRIVER']._serialized_start=549
  _globals['_PINSDRIVER']._serialized_end=787
# @@protoc_insertion_point(module_scope)
