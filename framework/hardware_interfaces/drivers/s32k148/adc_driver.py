import struct
from typing import Dict, Any, Callable

from framework.support.reports import rpc_call, logger
from framework.hardware_interfaces.protoc.s32k148.adc_driver_pb2 import (
    ADGetValueReturn,
    ADHandle,
    ADResetParams,
    ADInitParams,
)
from framework.hardware_interfaces.protoc.s32k148.adc_driver_pb2_grpc import (
    AdcDriverServicer,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.support.vtime import TimeEvent


class AdcChannel:
    """
    A class to represent an ADC channel.

    Attributes:
        vref_mv (int | None): The reference voltage in millivolts.
        max_counts (int | None): The maximum number of counts.
        _voltage (float): The voltage of the channel.
        _raise_interrupt (Callable[[int, int], None]): The function to raise an interrupt.
        _instance_id (int): The instance ID of the channel.
        _channel_id (int): The channel ID of the channel.
        iqr_id (int | None): The IRQ ID of the channel.
        _multiplier (float): The multiplier of the channel.
    """

    def __init__(
        self,
        instance_id: int,
        channel_id: int,
        raise_interrupt_func: Callable[[int, int], None],
        value: float = 0,
    ) -> None:
        self.vref_mv: int | None = None
        self.max_counts: int | None = None
        self._voltage = value
        self._raise_interrupt = raise_interrupt_func
        self._instance_id = instance_id
        self._channel_id = channel_id
        self.iqr_id: int | None = None
        self._multiplier: float = 1.0

    def initialize(self, vref: int, max_counts: int, irq_id: int) -> None:
        """
        Initialize the ADC channel.

        Args:
            vref (int): The reference voltage in millivolts.
            max_counts (int): The maximum number of counts.
            irq_id (int): The IRQ ID.
        """
        self.vref_mv = vref
        self.max_counts = max_counts
        self.iqr_id = irq_id

    @property
    def multiplier(self) -> float:
        """
        Get the multiplier of the channel.

        Returns:
            float: The multiplier of the channel.
        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, value: float) -> None:
        """
        Set the multiplier of the channel.

        Args:
            value (float): The multiplier to set.
        """
        self._multiplier = value

    @property
    def voltage(self) -> float:
        """
        Get the voltage of the channel.

        Returns:
            float: The voltage of the channel.
        """
        return self._voltage

    @voltage.setter
    def voltage(self, value: float) -> None:
        """
        Set the voltage of the channel.

        Args:
            value (float): The voltage to set.
        """
        self._voltage = value
        if self.iqr_id:
            flags = int.from_bytes(
                struct.pack(">BBH", self._channel_id, self._instance_id, self.counts),
                byteorder="big",
            )
            self._raise_interrupt(self.iqr_id, flags)

    @property
    def counts(self) -> int:
        """
        Get the counts of the channel.

        Returns:
            int: The counts of the channel.
        """
        assert self.vref_mv is not None
        assert self.voltage is not None
        assert self.max_counts is not None
        return int(
            ((self.voltage * self.multiplier * 1000) / self.vref_mv) * self.max_counts
        )


class AdcDriver(AdcDriverServicer):
    """
    A class to represent an ADC driver.

    Attributes:
        _channels (Dict[int, Dict[int, AdcChannel]]): The ADC channels.
        _ready (TimeEvent): The ready event.
        _raise_interrupt (Callable[[int, int], None]): The function to raise an interrupt.
    """

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self._channels: Dict[int, Dict[int, AdcChannel]] = {}
        self._ready = TimeEvent()
        self._raise_interrupt = raise_interrupt_func

    def wait_for_initialization(self) -> None:
        """
        Wait for the ADC driver initialization.
        """
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait(0.01)
        logger.info(f"{self.__class__.__name__} initialized")

    def get_channel(self, instance_id: int, channel_id: int) -> AdcChannel:
        """
        Get the ADC channel.

        Args:
            instance_id (int): The instance ID.
            channel_id (int): The channel ID.

        Returns:
            AdcChannel: The ADC channel.
        """
        if instance_id in self._channels:
            if channel_id not in self._channels[instance_id]:
                self._channels[instance_id][channel_id] = AdcChannel(
                    instance_id, channel_id, self._raise_interrupt
                )
        else:
            self._channels[instance_id] = {
                channel_id: AdcChannel(instance_id, channel_id, self._raise_interrupt)
            }

        return self._channels[instance_id][channel_id]

    @rpc_call
    def AdcDriver_InitChannel(self, request: ADInitParams, context: Any) -> Status:
        """
        Initialize the ADC channel.

        Args:
            request (ADInitParams): The ADC initialization parameters.
            context (Any): The context.

        Returns:
            Status: The status.
        """
        self._ready.set()
        channel = self.get_channel(request.instance_id, request.channel_id)
        channel.initialize(request.vref_mv, request.counts_max, request.irq_id)
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def AdcDriver_ResetInstance(self, request: ADResetParams, context: Any) -> Status:
        """
        Reset the ADC instance.

        Args:
            request (ADResetParams): The ADC reset parameters.
            context (Any): The context.

        Returns:
            Status: The status.
        """
        for channel in self._channels[request.instance_id].values():
            channel.voltage = 0
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def AdcDriver_GetChannelValue(
        self, request: ADHandle, context: Any
    ) -> ADGetValueReturn:
        """
        Get the ADC channel value.

        Args:
            request (ADHandle): The ADC handle.
            context (Any): The context.

        Returns:
            ADGetValueReturn: The ADC get value return.
        """
        channel = self.get_channel(request.instance_id, request.channel_id)
        assert channel.vref_mv is not None
        assert channel.max_counts is not None

        return ADGetValueReturn(
            status=Status(status=StatusEnum.STATUS_SUCCESS),
            counts=channel.counts,
        )
