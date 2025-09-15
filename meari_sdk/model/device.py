from dataclasses import dataclass, field
from typing import List
from dataclass_wizard import JSONWizard
from .camera_info import CameraInfo


@dataclass
class MeariDevice(JSONWizard, key_transform='SNAKE'):
    nvrs: List[CameraInfo] = field(default_factory=list)
    ipcs: List[CameraInfo] = field(default_factory=list)
    door_bells: List[CameraInfo] = field(default_factory=list)
    battery_cameras: List[CameraInfo] = field(default_factory=list)
    voice_bells: List[CameraInfo] = field(default_factory=list)
    fourth_generations: List[CameraInfo] = field(default_factory=list)
    flight_cameras: List[CameraInfo] = field(default_factory=list)
    chimes: List[CameraInfo] = field(default_factory=list)
    nvr_neutrals: List[CameraInfo] = field(default_factory=list)
    bases: List[CameraInfo] = field(default_factory=list)
    pic_doorbell_infos: List[CameraInfo] = field(default_factory=list)
    jingle_infos: List[CameraInfo] = field(default_factory=list)
    cellular_infos: List[CameraInfo] = field(default_factory=list)
    new_iot_device_list: List[CameraInfo] = field(default_factory=list)
    locator_list: List[CameraInfo] = field(default_factory=list)

    def get_all_list(self) -> List[CameraInfo]:
        """Return all cameras combined into a single list."""
        return (
            self.nvrs
            + self.ipcs
            + self.door_bells
            + self.battery_cameras
            + self.voice_bells
            + self.fourth_generations
            + self.flight_cameras
            + self.chimes
            + self.nvr_neutrals
            + self.bases
            + self.pic_doorbell_infos
            + self.jingle_infos
            + self.cellular_infos
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
                self.ipcs
                + self.door_bells
                + self.battery_cameras
                + self.voice_bells
                + self.fourth_generations
                + self.cellular_infos
                + self.flight_cameras
                + self.chimes
                + self.nvr_neutrals
            )
            if not cam.relay_license_id and not cam.as_friend
        ]
