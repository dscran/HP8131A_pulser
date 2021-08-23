# HP8131A_pulser

A simple class to control settings on an HP 8131A dual channel pulse generator.


## Requirements
* pyvisa
* pyvis_py

## Usage

```python
import hp8131a


# check pyvisa documentation for resource specification
visa_resource = 'ASRL/dev/ttyUSB0'  # USB-GPIB adapter
# visa_resource = 'GPIB::6::INSTR'  # GPIB channel 6

pulser = hp8131a.HP8131A(visa_resource)

# set pulse parameters
pulser.period = 12e-9
pulser.width1 = 5e-9
pulser.delay2 = 112e-9

# read parameters
pulser.delay2
> 112e-9

# manual trigger
pulser.manual_trigger()
```
