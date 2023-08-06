# pyTMG

A Python API client library for Cisco's [Transceiver Module Group (TMG) Compatibility Matrix](https://tmgmatrix.cisco.com/).

## Quick Links

* [Installation](https://github.com/ChristopherJHart/pytmg#Installation)
* [Getting Started](https://github.com/ChristopherJHart/pytmg#getting-started)

## Installation

To install this library, execute the following command:

```
pip install pytmg
```

## Getting Started

The below guide demonstrates the basic usage of this library through the Python 3 interpreter. At the end of the guide, a sample Python script is shown that demonstrates the equivalent commands within the context of a Python script.

To begin, import and instantiate the "TMG" class from pyTMG.

```
>>> from pytmg import TMG
>>> tmg = TMG.TMG()
>>> type(tmg)
<class 'pytmg.TMG.TMG'>
```

Most use cases of this library involve searching for transceiver information applicable to a specific Cisco product. The `search_device()` function allows one to easily accomplish this task. In the below example, we will search for all transceivers compatible with a Cisco Nexus 93180YC-EX device, which has a model number of "N9K-C93180YC-EX".

```
>>> result = tmg.search_device("N9K-C93180YC-EX")
>>> type(result)
<class 'pytmg.TMGResult.TMGResult'>
```

This function returns a TMGResult object that represents the results of the query. Models of network devices that match your query are contained in a list of TMGNetworkDevice objects in the TMGResult.network_devices attribute.

```
>>> dir(result)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__','__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__','__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__','__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'network_devices', 'result', 'total_count']
>>> type(result.network_devices)
<class 'list'>
>>> print(result.network_devices)
[<pytmg.TMGNetworkDevice.TMGNetworkDevice object at 0x0000028311C6FDD8>]
```

Each TMGNetworkDevice object represents general information about the queried product, as well as the transceivers supported by that particular product. Supported transceivers are accessible via the "transceivers" attribute, which is a list of TMGTransceiver objects. The below output shows that 217 transceivers are supported on the Nexus 93180YC-EX device.

```
>>> device = result.network_devices[0]
>>> type(device)
<class 'pytmg.TMGNetworkDevice.TMGNetworkDevice'>
>>> dir(device)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__',
 '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'network_family_data_sheet', 'product_family', 'product_id', 'result', 'transceivers']
>>> print(device.network_family_data_sheet)
https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742282.html
>>> print(device.product_family)
N9300
>>> print(device.product_id)
N9K-C93180YC-EX
>>> type(device.transceivers)
<class 'list'>
>>> print(len(device.transceivers))
217
```

Each TMGTransceiver object represents a transceiver that is supported on the queried product. Additionally, each object contains information about how the transceiver is supported, such as the necessary network operating system, minimum software release version, and physical properties that will allow the transceiver to work as expected (such as temperature, reach, etc.).

```
>>> transceiver = device.transceivers[0]
>>> type(transceiver)
<class 'pytmg.TMGTransceiver.TMGTransceiver'>
>>> dir(transceiver)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__',
 '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_clean_aci_soft_release', '_clean_nxos_soft_release', '_clean_soft_release', 'breakout_mode', 'cable_type', 'clean_soft_release_min_ver', 'connector_type', 'data_rate', 'description', 'digital_diagnostic', 'dom_support', 'end_of_sale', 'form_factor', 'media', 'network_device_notes', 'network_model_id', 'note_count', 'os_type', 'product_family', 'product_family_id', 'product_id', 'product_model_id', 'reach', 'release_id', 'result', 'soft_release_dom', 'soft_release_min_ver', 'state', 'state_message', 'temperature_range', 'tmg_id', 'transceiver_business_unit', 'transceiver_model_data_sheet', 'transceiver_notes', 'transmission_standard', 'type', 'updated_by', 'updated_on', 'version', 'version_id']
```

The below output shows that the first support transceiver in the list is for scenarios where the Nexus 93180YC-EX device is deployed in ACI mode, and is supported starting with ACI software 11.3(2)

```
>>> print(transceiver.os_type)
ACI
>>> print(transceiver.soft_release_min_ver)
ACI-N9KDK9-11.3(2)
```

A Python script demonstrating the basic usage of this library is as follows. Specifically, this script identifies all 40G transceiver models that are supported in the NX-OS operating system:

```python
from pytmg import TMG

tmg = TMG.TMG()
print("Searching for device...")
result = tmg.search_device("N9K-C93180YC-EX")
print("Device results returned!")
for device in result.network_devices:
    print("Device model number: {}".format(device.product_id))
    print("List of supported transceivers: ")
    for transceiver in device.transceivers:
        if transceiver.os_type == "NX-OS" and transceiver.data_rate == "40 Gbps":
            print(" - {}".format(transceiver.product_id))
```

The output of this script is as follows:

```
Searching for device...
Device results returned!
Device model number: N9K-C93180YC-EX
List of supported transceivers:
 - QSFP-40G-SR4
 - QSFP-40G-SR4
 - QSFP-40G-CSR4
 - QSFP-40G-CSR4
 - QSFP-40G-SR4-S
 - QSFP-40G-SR4-S
 - FET-40G
 - FET-40G
 - QSFP-40G-SR-BD
 - QSFP-40G-SR-BD
 - QSFP-4X10G-LR-S
 - QSFP-40G-LR4-S
 - QSFP-40GE-LR4
 - QSFP-40G-LR4
 - QSFP-40G-ER4
 - WSP-Q40GLR4L
 - QSFP-4SFP10G-CU5M
 - QSFP-4SFP10G-CU3M
 - QSFP-4SFP10G-CU1M
 - QSFP-4X10G-AC7M
 - QSFP-4X10G-AC10M
 - QSFP-H40G-CU5M
 - QSFP-H40G-CU3M
 - QSFP-H40G-CU1M
 - QSFP-H40G-ACU7M
 - QSFP-H40G-ACU10M
 - QSFP-4X10G-AOC1M
 - QSFP-4X10G-AOC3M
 - QSFP-4X10G-AOC5M
 - QSFP-4X10G-AOC7M
 - QSFP-4X10G-AOC10M
 - QSFP-H40G-AOC1M
 - QSFP-H40G-AOC2M
 - QSFP-H40G-AOC3M
 - QSFP-H40G-AOC5M
 - QSFP-H40G-AOC7M
 - QSFP-H40G-AOC10M
 - QSFP-H40G-AOC15M
 - QSFP-H40G-AOC20M
 - QSFP-40G-BD-RX
 - QSFP-40G-BD-RX
 - QSFP-H40G-AOC25M
 - QSFP-H40G-AOC30M
```