import tinytuya

lamp = tinytuya.Device(
    dev_id='eb3709d3ce82370ee9xiqf',
    address='192.168.0.101',
    local_key='65CC95DFEE111891',
    version=3.3
)

result = lamp.set_value(20, True)
print(result)