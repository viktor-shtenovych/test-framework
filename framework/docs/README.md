# Framework design
- `communications` - Footswitch communication interfaces (wired/CAN, wireless, inductive). This implementation shall not depend
          on test setup SIL/HIL i.e. wired connection shall work with either simulator or HW CAN
- `core` - Main test framework logic. Implements simulation of peripherals/chips like battery, GPIOs, I2C
  - `components` - component elements
  - `control` - control elements
  - `devices` - device simulation modules
- `hardware_interfaces` - Low-level logic
  - `drivers` - Python driver interfaces
  - `proto` - protobuf definitions of RPC interface between emulator - framework
  - `protoc` - _compiled_ protobuf files for python
- `support` - support modules
  - `reporting` - Test reporting. Currently, console log only. In future shall be extended to generate desired reports
    (e.g. integration with CI/CD and/or test management system)
  - `vtime_helper` - Virtual Time manager implementation
  - `py_emulator` -  Start/Stop of SW under test (emulator, py_emulator,...)
  
![TestFrameworkDesign](imgs/framework_design.svg "Design")

# Footswitch blocks changes

To be able to run and test Footswitch SW the MCAL layer is adapted to forward necessary MCAL calls to test framework over RPC. Test framework is responsible for simulation of specific HW peripherals.

![Blocks](imgs/blocks.svg "Blocks")

# Sequence diagram

Sequence diagram for a test case setting GPIO pin value and checking CAN status message.

1. Simulate button press from test script. This triggers putting interrupt in Interrupts queue. The interrupt stores interrupt ID and value of each GPIO pin in related port.
2. When footswitch SW goes to idle state then remote procedure call is trigerred towards test framework to retrieve pending interrupt from Interrupts queue.
   For GPIO interrupt the pins values for related port are saved for later use.
3. Footswitch SW requests pin value. MCAL implementation returns stored value
4. Footswitch SW sends CAN frame. This is transferred using remote procedure call to Message queue and status message is retrieved. 
   To avoid unnecessary (slow) remote procedure call `FLEXCAN_EVENT_TX_COMPLETE` interrupt is generated internally in MCAL.
5. Test script waits for CAN message transfer and verifies its content.

![Sequence diagram](imgs/sequence_diagram.svg "SequenceDiagram")
