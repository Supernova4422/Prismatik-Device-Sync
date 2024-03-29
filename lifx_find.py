import sys
import asyncio as aio
import aiolifx as alix
from functools import partial

# Simple bulb control frpm console
class bulbs:
    """A simple class with a register and  unregister methods"""

    def __init__(self):
        self.bulbs = []
        self.boi = None  # bulb of interest

    def register(self, bulb):
        bulb.get_label()
        bulb.get_location()
        bulb.get_version()
        bulb.get_group()
        bulb.get_wififirmware()
        bulb.get_hostfirmware()
        self.bulbs.append(bulb)
        self.bulbs.sort(key=lambda x: x.label or x.mac_addr)

    def unregister(self, bulb):
        idx = 0
        for x in list([y.mac_addr for y in self.bulbs]):
            if x == bulb.mac_addr:
                del self.bulbs[idx]
                break
            idx += 1


def readin():
    """Reading from stdin and displaying menu"""

    selection = sys.stdin.readline().strip("\n")
    MyBulbs.bulbs.sort(key=lambda x: x.label or x.mac_addr)
    lov = [x for x in selection.split(" ") if x != ""]
    if lov:
        if MyBulbs.boi:
            # try:
            if True:
                if int(lov[0]) == 0:
                    MyBulbs.boi = None
                elif int(lov[0]) == 1:
                    if len(lov) > 1:
                        MyBulbs.boi.set_power(lov[1].lower() in ["1", "on", "true"])
                        MyBulbs.boi = None
                    else:
                        print("Error: For power you must indicate on or off\n")
                elif int(lov[0]) == 2:
                    if len(lov) > 2:
                        try:
                            MyBulbs.boi.set_color(
                                [
                                    58275,
                                    0,
                                    int(round((float(lov[1]) * 65365.0) / 100.0)),
                                    int(round(float(lov[2]))),
                                ]
                            )

                            MyBulbs.boi = None
                        except:
                            print(
                                "Error: For white brightness (0-100) and temperature (2500-9000) must be numbers.\n"
                            )
                    else:
                        print(
                            "Error: For white you must indicate brightness (0-100) and temperature (2500-9000)\n"
                        )
                elif int(lov[0]) == 3:
                    if len(lov) > 3:
                        try:
                            MyBulbs.boi.set_color(
                                [
                                    int(round((float(lov[1]) * 65535.0) / 360.0)),
                                    int(round((float(lov[2]) * 65535.0) / 100.0)),
                                    int(round((float(lov[3]) * 65535.0) / 100.0)),
                                    3500,
                                ]
                            )
                            MyBulbs.boi = None
                        except:
                            print(
                                "Error: For colour hue (0-360), saturation (0-100) and brightness (0-100)) must be numbers.\n"
                            )
                    else:
                        print(
                            "Error: For colour you must indicate hue (0-360), saturation (0-100) and brightness (0-100))\n"
                        )

                elif int(lov[0]) == 4:
                    print(MyBulbs.boi.device_characteristics_str("    "))
                    print(MyBulbs.boi.device_product_str("    "))
                    MyBulbs.boi = None
                elif int(lov[0]) == 5:
                    print(MyBulbs.boi.device_firmware_str("   "))
                    MyBulbs.boi = None
                elif int(lov[0]) == 6:
                    mypartial = partial(MyBulbs.boi.device_radio_str)
                    MyBulbs.boi.get_wifiinfo(
                        callb=lambda x, y: print("\n" + mypartial(y))
                    )
                    MyBulbs.boi = None
                elif int(lov[0]) == 7:
                    mypartial = partial(MyBulbs.boi.device_time_str)
                    MyBulbs.boi.get_hostinfo(
                        callb=lambda x, y: print("\n" + mypartial(y))
                    )
                    MyBulbs.boi = None
                elif int(lov[0]) == 8:
                    if len(lov) > 3:
                        try:
                            print(
                                "Sending {}".format(
                                    [
                                        int(round((float(lov[1]) * 65535.0) / 360.0)),
                                        int(round((float(lov[2]) * 65535.0) / 100.0)),
                                        int(round((float(lov[3]) * 65535.0) / 100.0)),
                                        3500,
                                    ]
                                )
                            )
                            MyBulbs.boi.set_waveform(
                                {
                                    "color": [
                                        int(round((float(lov[1]) * 65535.0) / 360.0)),
                                        int(round((float(lov[2]) * 65535.0) / 100.0)),
                                        int(round((float(lov[3]) * 65535.0) / 100.0)),
                                        3500,
                                    ],
                                    "transient": 1,
                                    "period": 100,
                                    "cycles": 30,
                                    "skew_ratio": 0,
                                    "waveform": 0,
                                }
                            )
                            MyBulbs.boi = None
                        except:
                            print(
                                "Error: For pulse hue (0-360), saturation (0-100) and brightness (0-100)) must be numbers.\n"
                            )
                    else:
                        print(
                            "Error: For pulse you must indicate hue (0-360), saturation (0-100) and brightness (0-100))\n"
                        )
                elif int(lov[0]) == 9:
                    # HEV cycle
                    if len(lov) == 1:
                        # Get current state
                        print("Getting current HEV state")
                        MyBulbs.boi.get_hev_cycle(
                            callb=lambda _, r: print(
                                f"\nHEV: duration={r.duration}, "
                                f"remaining={r.remaining}, "
                                f"last_power={r.last_power}"
                            )
                        )
                        MyBulbs.boi.get_last_hev_cycle_result(
                            callb=lambda _, r: print(f"\nHEV result: {r.result_str}")
                        )

                    elif len(lov) == 2:
                        duration = int(lov[1])
                        enable = duration >= 0
                        if enable:
                            print(f"Running HEV cycle for {duration} second(s)")
                        else:
                            print(f"Aborting HEV cycle")
                            duration = 0
                        MyBulbs.boi.set_hev_cycle(
                            enable=enable,
                            duration=duration,
                            callb=lambda _, r: print(
                                f"\nHEV: duration={r.duration}, "
                                f"remaining={r.remaining}, "
                                f"last_power={r.last_power}"
                            ),
                        )
                    else:
                        print("Error: maximum 1 argument for HEV cycle")
                    MyBulbs.boi = None
                elif int(lov[0]) == 10:
                    # HEV cycle configuration
                    if len(lov) == 1:
                        # Get current state
                        print("Getting current HEV configuration")
                        MyBulbs.boi.get_hev_configuration(
                            callb=lambda _, r: print(
                                f"\nHEV: indication={r.indication}, "
                                f"duration={r.duration}"
                            )
                        )

                    elif len(lov) == 3:
                        indication = bool(int(lov[1]))
                        duration = int(lov[2])
                        print(
                            f"Configuring default HEV cycle with "
                            f"{'' if indication else 'no '}indication for "
                            f"{duration} second(s)"
                        )
                        MyBulbs.boi.set_hev_configuration(
                            indication=indication,
                            duration=duration,
                            callb=lambda _, r: print(
                                f"\nHEV: indication={r.indication}, "
                                f"duration={r.duration}"
                            ),
                        )
                    else:
                        print("Error: 0 or 2 arguments for HEV config")
                    MyBulbs.boi = None
            # except:
            # print ("\nError: Selection must be a number.\n")
        else:
            try:
                if int(lov[0]) > 0:
                    if int(lov[0]) <= len(MyBulbs.bulbs):
                        MyBulbs.boi = MyBulbs.bulbs[int(lov[0]) - 1]
                    else:
                        print("\nError: Not a valid selection.\n")

            except:
                print("\nError: Selection must be a number.\n")

    if MyBulbs.boi:
        print("Select Function for {}:".format(MyBulbs.boi.label))
        print("\t[1]\tPower (0 or 1)")
        print("\t[2]\tWhite (Brigthness Temperature)")
        print("\t[3]\tColour (Hue Saturation Brightness)")
        print("\t[4]\tInfo")
        print("\t[5]\tFirmware")
        print("\t[6]\tWifi")
        print("\t[7]\tUptime")
        print("\t[8]\tPulse")
        print("\t[9]\tHEV cycle (duration, or -1 to stop)")
        print("\t[10]\tHEV configuration (indication, duration)")
        print("")
        print("\t[0]\tBack to bulb selection")
    else:
        idx = 1
        print("Select Bulb:")
        for x in MyBulbs.bulbs:
            print("\t[{}]\t{}".format(idx, x.label or x.mac_addr))
            idx += 1
    print("")
    print("Your choice: ", end="", flush=True)


async def scan(loop, discovery):
    scanner = alix.LifxScan(loop)
    ips = await scanner.scan()
    discovery.start(listen_ip=ips[0])
    print('Hit "Enter" to start')
    print("Use Ctrl-C to quit")
    if not ips:
        print("LIFX controller not found!")
        return

    discovery.start(listen_ip=ips[0])

MyBulbs = bulbs()
loop = aio.get_event_loop()
discovery = alix.LifxDiscovery(loop, MyBulbs)

try:
    # loop.add_reader(sys.stdin, readin)
    loop.create_task(scan(loop, discovery))
    loop.run_forever()
except:
    pass
finally:
    discovery.cleanup()
    loop.remove_reader(sys.stdin)
    loop.close()