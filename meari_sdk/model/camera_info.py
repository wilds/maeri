from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclass_wizard import JSONWizard

from .device_params import DeviceParams
from .base_device_info import BaseDeviceInfo
from ..helpers import is_low_power_device, is_iothub


@dataclass
class MultiVideoDevice(JSONWizard):
    # Placeholder for multi-video device attributes
    pass


@dataclass
class VideoCloudConfig(JSONWizard):
    # Placeholder for video cloud configuration attributes
    pass


@dataclass
class CameraInfo(BaseDeviceInfo):
    device_p2p: Optional[str] = None
    firm_id: Optional[str] = None
    trial_cloud: Optional[int] = None
    device_version_id: Optional[str] = None
    time_zone: Optional[str] = None
    as_friend: Optional[bool] = None
    as_home_member: Optional[bool] = None
    latitude: Optional[float] = None
    radius: Optional[float] = None
    longitude: Optional[float] = None
    sleep: Optional[str] = None
    user_id: Optional[int] = None
    is_checked: bool = False
    is_binding_ty: Optional[str] = field(default=None, metadata={"deprecated": True})
    cloud_status: Optional[int] = None
    cloud_support: Optional[int] = None
    device_type: Optional[str] = None
    has_alert_msg: bool = False
    update_version: bool = False
    close_push: Optional[int] = None
    update_perssion: Optional[str] = "N"
    wifi_name: Optional[str] = None
    chime_wifi_name: Optional[str] = None
    chime_wifi_pwd: Optional[str] = None
    relay_license_id: Optional[str] = None
    wifi_mac: Optional[str] = None
    region: Optional[str] = None
    alarm_img_oss_state: Optional[int] = None
    nvr_id: Optional[int] = None
    nvr_uuid: Optional[str] = None
    nvr_key: Optional[str] = None
    nvr_num: Optional[str] = None
    nvr_port: Optional[int] = None
    msg_id: Optional[int] = None
    msg_type: Optional[int] = None
    is_frequent_alarm: Optional[bool] = None
    bell_voice_url: Optional[str] = None
    sub_devices: List[CameraInfo] = field(default_factory=list)
    share_access_sign: Optional[int] = None
    privacy_status: Optional[int] = None
    permission: Optional[int] = None
    family_id: Optional[str] = None
    room_id: Optional[str] = None
    room_name: Optional[str] = None
    sim_id: Optional[str] = None
    device_params: Optional[DeviceParams] = None
    categ: Optional[int] = None
    is_cloud_experience: Optional[bool] = None
    nvr_channel_list: List[CameraInfo] = field(default_factory=list)
    nvr_max_channel_num: Optional[int] = None
    nvr_channel_id: Optional[int] = None
    nvr_channel_name: Optional[str] = None
    nvr_channel_status: Optional[int] = None
    nvr_channel_type: Optional[int] = None
    is_nvr_expand: bool = False
    enable: bool = True
    is_ad_type: Optional[bool] = None
    adapter_type: Optional[int] = None
    multiple_videos: List[MultiVideoDevice] = field(default_factory=list)
    num: Optional[int] = None
    video_cloud_config: Optional[VideoCloudConfig] = None
    history_event_enable: Optional[int] = None
    cloud_end_time: Optional[int] = None
    permission_map: Dict[str, int] = field(default_factory=dict)

    class Meta(JSONWizard.Meta):
        key_transform = 'SNAKE'  # oppure 'CAMEL' se serve
        recursive_classes = True

    # --- Methods for device management ---

    def add_sub_device(self, camera_info: CameraInfo):
        """Add a sub-device to this camera."""
        self.sub_devices.append(camera_info)

    def can_control(self) -> bool:
        """Check if the user is allowed to control this device."""
        if self.as_home_member:
            return self.permission == 1
        return not self.as_friend or self.share_access_sign == 1

    def is_master(self) -> bool:
        """Determine if this camera is a master device."""
        if self.as_home_member:
            return False
        return not self.as_friend

    def is_shared(self) -> bool:
        """Check if this camera is shared."""
        return not self.is_master()

    def set_sleep_mode(self, mode: int) -> str:
        """Set sleep mode by code and return its string representation."""
        mode_map = {0: "off", 1: "on", 2: "time", 3: "geographic"}
        self.sleep = mode_map.get(mode, "")
        return self.sleep

    def is_geographic_mode(self) -> bool:
        """Return True if sleep mode is geographic."""
        return self.sleep == "geographic"

    def is_chime_device(self) -> bool:
        """Return True if the device is a chime type."""
        return getattr(self, "device_type_id", None) == 9

    def is_low_power_device(self) -> bool:
        return is_low_power_device(self)

    def is_iot(self) -> bool:
        return is_iothub(self)

    def is_chime(self) -> bool:
        """
        Returns True if this device is a chime (device type ID == 9).

        Equivalent to Java:
            return this.getDevTypeID() == 9;
        """
        return self.dev_type_id == 9
