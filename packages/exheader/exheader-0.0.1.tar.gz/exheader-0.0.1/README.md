# exheader

This is a simple python library allowing to load, modify and save 3ds exheader files.
Not all settings are supported (those will throw an exception on load) or easily modifyable yet.

## Installation

Run the following to install:

```python
pip install exheader
```

## Usage

```python
from exheader import Exheader

exh = Exheader()

# Load exheader from file
f_in = open('exheader.bin', 'rb')
exh.unpack_from(f_in.read())
f_in.close()

# Print the application tite
print(exh.sci.app_title)

# Change the application title
exh.sci.app_title = 'MyApp'

# Print allowed SVCs
print(exh.aci.arm11_kernel_caps.svcs)

# Add SVC 0x70
exh.aci.arm11_kernel_caps.svcs.add(0x70)

# Write modified exheader to file
f_out = open('exheader_out.bin', 'wb')
f_out.write(exh.pack())
f_out.close()
```
