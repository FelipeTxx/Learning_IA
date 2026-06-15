import tinytuya

DEV_ID = "eb6cf639a85ba6907by7ss"
IP = "186.227.135.166"
LOCAL_KEY = "65CC95DFEE111891"

for VERSION in [3.1, 3.3, 3.4, 3.5]:
    print("\n==============================")
    print("Testando versão:", VERSION)

    lamp = tinytuya.Device(
        dev_id=DEV_ID,
        address=IP,
        local_key=LOCAL_KEY,
        version=VERSION
    )

    lamp.set_socketPersistent(False)
    lamp.set_socketTimeout(5)

    try:
        result = lamp.status()
        print(result)
    except Exception as e:
        print("Erro:", e)