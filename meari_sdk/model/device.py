from dataclasses import dataclass, field
from typing import List
from dataclass_wizard import JSONWizard
from .camera_info import CameraInfo


@dataclass
class MeariDevice(JSONWizard):
    nvr: List[CameraInfo] = field(default_factory=list)
    ipc: List[CameraInfo] = field(default_factory=list)
    door_bell: List[CameraInfo] = field(default_factory=list)
    battery_camera: List[CameraInfo] = field(default_factory=list)
    voice_bell: List[CameraInfo] = field(default_factory=list)
    fourth_generation: List[CameraInfo] = field(default_factory=list)
    flight_camera: List[CameraInfo] = field(default_factory=list)
    chime: List[CameraInfo] = field(default_factory=list)
    nvr_neutral: List[CameraInfo] = field(default_factory=list)
    base: List[CameraInfo] = field(default_factory=list)
    pic_doorbell_info: List[CameraInfo] = field(default_factory=list)
    jingle_info: List[CameraInfo] = field(default_factory=list)
    cellular_info: List[CameraInfo] = field(default_factory=list)
    new_iot_device_list: List[CameraInfo] = field(default_factory=list)
    locator_list: List[CameraInfo] = field(default_factory=list)

    def get_all_list(self) -> List[CameraInfo]:
        """Return all cameras combined into a single list."""
        return (
            self.nvr
            + self.ipc
            + self.door_bell
            + self.battery_camera
            + self.voice_bell
            + self.fourth_generation
            + self.flight_camera
            + self.chime
            + self.nvr_neutral
            + self.base
            + self.pic_doorbell_info
            + self.jingle_info
            + self.cellular_info
            + self.new_iot_device_list
            + self.locator_list
        )

    def get_all_list_sn(self) -> List[str]:
        """Return all camera serial numbers (sn_num)."""
        return [info.sn_num for info in self.get_all_list()]

    def get_no_chime_sub_device_list(self) -> List[CameraInfo]:
        """
        Return all cameras without chime,
        excluding those that have relay_license_id or are marked as friend.
        """
        return [
            cam
            for cam in (
                self.ipc
                + self.door_bell
                + self.battery_camera
                + self.voice_bell
                + self.fourth_generation
                + self.cellular_info
                + self.flight_camera
                + self.chime
                + self.nvr_neutral
            )
            if not cam.relay_license_id and not cam.as_friend
        ]

    class Meta(JSONWizard.Meta):
        key_transform = 'SNAKE'  # oppure 'CAMEL' se serve
        recursive_classes = True
