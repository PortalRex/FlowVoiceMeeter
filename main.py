import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
from flowlauncher import FlowLauncher
import voicemeeterlib

class VoicemeeterDevices(FlowLauncher):
    def __init__(self):
        self.vm = None
        super().__init__()

    def connect_voicemeeter(self):
        try:
            if self.vm is None:
                self.vm = voicemeeterlib.api("potato")
                self.vm.login()
            return True
        except:
            return False

    def list_wdm_devices(self):
        try:
            if not self.connect_voicemeeter():
                return []

            wdm_devices = []
            for i in range(self.vm.device.outs):
                device_info = self.vm.device.output(i)
                if device_info["type"].lower() == "wdm":
                    wdm_devices.append(device_info["name"])

            if not wdm_devices:
                return [{
                    "Title": "No WDM output devices detected",
                    "SubTitle": "Ensure WDM output devices are active in Voicemeeter.",
                    "IcoPath": "assets/error.png"
                }]

            return [
                {
                    "Title": device,
                    "SubTitle": f"Set A1 Bus to {device}",
                    "IcoPath": "assets/device.png",
                    "JsonRPCAction": {
                        "method": "select_wdm_device",
                        "parameters": [device],
                        "dontHideAfterAction": False
                    }
                }
                for device in wdm_devices
            ]

        except:
            return [{"Title": "Error", "SubTitle": "Failed to list WDM devices.", "IcoPath": "assets/error.png"}]

    def select_wdm_device(self, device_name):
        try:
            if not self.connect_voicemeeter():
                return False

            self.vm.bus[0].device.wdm = device_name
            return [{
                "Title": "Success!",
                "SubTitle": f"Device '{device_name}' set for A1 Bus (WDM).",
            }]

        except:
            return [{"Title": "Error", "SubTitle": "Failed to set WDM device.", "IcoPath": "assets/error.png"}]

    def query(self, query):
        return self.list_wdm_devices()

if __name__ == "__main__":
    VoicemeeterDevices()