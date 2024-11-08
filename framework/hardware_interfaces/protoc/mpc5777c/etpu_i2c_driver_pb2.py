# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: etpu_i2c_driver.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x65tpu_i2c_driver.proto\x12\x0crpc_mpc5777c\x1a\x0c\x63ommon.proto\"8\n\x11\x45tpuI2cInitParams\x12\x13\n\x0binstance_id\x18\x01 \x01(\r\x12\x0e\n\x06irq_id\x18\x03 \x01(\x05\"T\n\x17\x45tpuI2cReceiveReqParams\x12\x13\n\x0binstance_id\x18\x01 \x01(\r\x12\x16\n\x0e\x64\x65vice_address\x18\x03 \x01(\r\x12\x0c\n\x04size\x18\x04 \x01(\r\"U\n\x15\x45tpuI2cTransmitParams\x12\x13\n\x0binstance_id\x18\x01 \x01(\r\x12\x16\n\x0e\x64\x65vice_address\x18\x03 \x01(\r\x12\x0f\n\x07message\x18\x04 \x01(\x0c\"/\n\x18\x45tpuI2cInterfaceIdParams\x12\x13\n\x0binstance_id\x18\x01 \x01(\r\"T\n\x1c\x45tpuI2cGetReceivedDataReturn\x12#\n\x06status\x18\x01 \x01(\x0b\x32\x13.rpc_general.Status\x12\x0f\n\x07message\x18\x02 \x01(\x0c\x32\x80\x03\n\rEtpuI2cDriver\x12K\n\x11\x45TPU_I2C_DRV_Init\x12\x1f.rpc_mpc5777c.EtpuI2cInitParams\x1a\x13.rpc_general.Status\"\x00\x12S\n\x15\x45TPU_I2C_DRV_Transmit\x12#.rpc_mpc5777c.EtpuI2cTransmitParams\x1a\x13.rpc_general.Status\"\x00\x12W\n\x17\x45TPU_I2C_DRV_ReceiveReq\x12%.rpc_mpc5777c.EtpuI2cReceiveReqParams\x1a\x13.rpc_general.Status\"\x00\x12t\n\x1c\x45TPU_I2C_DRV_GetReceivedData\x12&.rpc_mpc5777c.EtpuI2cInterfaceIdParams\x1a*.rpc_mpc5777c.EtpuI2cGetReceivedDataReturn\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'etpu_i2c_driver_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ETPUI2CINITPARAMS']._serialized_start=53
  _globals['_ETPUI2CINITPARAMS']._serialized_end=109
  _globals['_ETPUI2CRECEIVEREQPARAMS']._serialized_start=111
  _globals['_ETPUI2CRECEIVEREQPARAMS']._serialized_end=195
  _globals['_ETPUI2CTRANSMITPARAMS']._serialized_start=197
  _globals['_ETPUI2CTRANSMITPARAMS']._serialized_end=282
  _globals['_ETPUI2CINTERFACEIDPARAMS']._serialized_start=284
  _globals['_ETPUI2CINTERFACEIDPARAMS']._serialized_end=331
  _globals['_ETPUI2CGETRECEIVEDDATARETURN']._serialized_start=333
  _globals['_ETPUI2CGETRECEIVEDDATARETURN']._serialized_end=417
  _globals['_ETPUI2CDRIVER']._serialized_start=420
  _globals['_ETPUI2CDRIVER']._serialized_end=804
# @@protoc_insertion_point(module_scope)
