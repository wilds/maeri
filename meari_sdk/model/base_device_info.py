from dataclasses import dataclass
from typing import Optional

from dataclass_wizard import JSONWizard
import json


@dataclass
class Capability(JSONWizard):
    ver: Optional[int] = -1
    vtk: Optional[int] = -1
    fcr: Optional[int] = -1
    dcb: Optional[int] = -1
    md: Optional[int] = -1
    ptz: Optional[int] = -1
    tmpr: Optional[int] = -1
    hmd: Optional[int] = -1
    pir: Optional[int] = -1
    cst: Optional[int] = -1
    geo: Optional[int] = -1
    nst: Optional[int] = -1
    evs: Optional[int] = -1
    vst: Optional[int] = -1
    btl: Optional[int] = -1
    cse: Optional[int] = -1
    dnm: Optional[int] = -1
    dnm2: Optional[int] = -1
    led: Optional[int] = -1
    svc: Optional[int] = -1
    ovf: Optional[int] = -1
    cs2: Optional[int] = -1
    bps: Optional[int] = -1
    bps2: Optional[str] = None
    wfs: Optional[int] = -1
    flt: Optional[int] = -1
    rng: Optional[int] = -1
    pwm: Optional[int] = -1
    sd: Optional[int] = -1
    ota: Optional[int] = -1
    hms: Optional[int] = -1
    shd: Optional[int] = -1
    flp: Optional[int] = -1
    lcd: Optional[int] = -1
    dlk: Optional[int] = -1
    dor: Optional[int] = -1
    lgt: Optional[int] = -1
    che: Optional[int] = -1
    slp: Optional[int] = -1
    vec: Optional[int] = -1
    bcd: Optional[int] = -1
    ptr: Optional[int] = -1
    pdt: Optional[int] = -1
    cct: Optional[int] = -1
    ecs: Optional[int] = -1
    rel: Optional[int] = -1
    esd: Optional[int] = -1
    alp: Optional[int] = -1
    spp: Optional[int] = -1
    ltl: Optional[int] = -1
    p2p: Optional[int] = -1
    ovc: Optional[int] = -1
    ren: Optional[int] = -1
    wkp: Optional[int] = -1
    roi: Optional[int] = -1
    afq: Optional[int] = -1
    crm: Optional[int] = -1
    fcd: Optional[int] = -1
    sla: Optional[int] = -1
    slv: Optional[int] = 0
    ttp: Optional[int] = -1
    mpc: Optional[int] = -1
    plp: Optional[int] = -1
    plv: Optional[int] = -1
    rtm: Optional[int] = -1
    vid: Optional[int] = -1
    fcb: Optional[int] = None
    fld: Optional[int] = -1
    acs: Optional[int] = -1
    dbc: Optional[int] = -1
    uif: Optional[int] = -1
    mts: Optional[int] = -1
    rbt: Optional[int] = -1
    pcr: Optional[int] = -1
    lwm: Optional[int] = -1
    alm: Optional[int] = -1
    lwm2: Optional[int] = -1
    gal: Optional[int] = -1
    flk: Optional[int] = -1
    rgb: Optional[int] = -1
    rgbm: Optional[int] = 0
    hkt: Optional[int] = -1
    voi: Optional[int] = -1
    sti: Optional[int] = -1
    lgh: Optional[int] = -1
    sir: Optional[int] = -1
    sen: Optional[int] = -1
    men: Optional[int] = -1
    rae: Optional[int] = -1
    rec: Optional[int] = -1
    aup: Optional[int] = -1
    mup: Optional[int] = -1
    lgl: Optional[int] = -1
    sot: Optional[int] = -1
    lot: Optional[int] = -1
    tmz: Optional[int] = -1
    dpc: Optional[int] = -1
    ajs: Optional[int] = -1
    ndr: Optional[int] = -1
    pds: Optional[int] = -1
    evt: Optional[int] = -1
    evt2: Optional[int] = -1
    evt3: Optional[int] = -1
    fls: Optional[int] = -1
    cpn: Optional[int] = -1
    tv: Optional[int] = -1
    rwm: Optional[int] = -1
    lgo: Optional[int] = -1
    ai: Optional[int] = -1
    bat: Optional[int] = -1
    idt: Optional[int] = 0
    plg: Optional[int] = -1
    pva: Optional[int] = -1
    ptz2: Optional[int] = -1
    pet: Optional[int] = -1
    pfv: Optional[int] = -1
    pfp: Optional[int] = -1
    pms: Optional[int] = -1
    ptf: Optional[int] = -1
    lem: Optional[int] = -1
    avd: Optional[int] = -1
    pbd: Optional[int] = -1
    pbf: Optional[int] = 0
    adb: Optional[int] = -1
    pvs: Optional[int] = -1
    sqr: Optional[int] = -1
    ntw: Optional[int] = -1
    svt: Optional[int] = -1
    ptc: Optional[int] = -1
    swi: Optional[int] = -1
    swi2: Optional[int] = -1
    ptd: Optional[int] = -1
    rly: Optional[int] = -1
    tha: Optional[int] = -1
    ttc: Optional[int] = -1
    hts: Optional[int] = -1
    dbd: Optional[int] = -1
    msc: Optional[str] = None
    slt: Optional[int] = -1
    sfi: Optional[int] = -1
    pvm: Optional[int] = -1
    sbf: Optional[str] = None
    sdc: Optional[int] = -1
    ars: Optional[int] = -1
    lmf: Optional[int] = -1
    erd: Optional[int] = -1
    sld: Optional[int] = -1
    nms: Optional[int] = -1
    auf: Optional[int] = 0
    mul: Optional[int] = 0
    mpm: Optional[int] = 0
    wml: Optional[int] = 0
    trp: Optional[int] = 0
    wtl: Optional[int] = 0
    pbe: Optional[int] = 0
    pbs: Optional[int] = 0
    cqr: Optional[int] = -1
    dai: Optional[str] = ""
    cai: Optional[str] = ""
    ble: Optional[int] = 0
    bzr: Optional[int] = 0
    pri: Optional[int] = 0
    wff: Optional[int] = 0
    pfl: Optional[int] = 0
    sd2: Optional[int] = 0
    pbr: Optional[str] = None
    ssc: Optional[int] = 0
    fey: Optional[str] = None
    aid: Optional[int] = 0
    sdm: Optional[int] = 0
    fme: Optional[int] = 0
    ppl: Optional[int] = 0
    sba: Optional[int] = 0
    csf: Optional[int] = -1
    elt: Optional[int] = -1
    las: Optional[int] = 0
    zmf: Optional[int] = None
    r90: Optional[int] = -1
    vop: Optional[int] = -1
    pwh: Optional[str] = None
    pno: Optional[int] = -1
    vwh: Optional[str] = None
    vot: Optional[str] = None
    pit: Optional[str] = None
    mper: Optional[int] = -1
    ir: Optional[int] = -1
    tms: Optional[int] = -1
    rst: Optional[int] = -1
    mic: Optional[int] = -1
    lange: Optional[int] = -1
    sap: Optional[int] = -1
    mrda: Optional[int] = -1
    hhs: Optional[int] = -1
    cfs: Optional[int] = -1
    lds: Optional[int] = -1
    alb: Optional[int] = 0
    uvd: Optional[int] = 0
    stc: Optional[str] = ""
    dis: Optional[int] = 0
    plm: Optional[int] = 0
    bsi: Optional[int] = 0
    flit: Optional[int] = 0


@dataclass
# class BaseDeviceInfo(Capability, JSONWizard):  # Java class have Capability inside
class BaseDeviceInfo(JSONWizard):
    device_uuid: Optional[str] = None
    tp: Optional[str] = None
    ip: Optional[str] = None
    mac: Optional[str] = None
    version: Optional[str] = None
    license_id: Optional[str] = None
    sn_num: Optional[str] = None
    device_name: Optional[str] = None
    model: Optional[str] = None
    capability: Optional[str] = None
    produce_auth: Optional[str] = None
    auto_binding: Optional[int] = None
    dev_type_id: Optional[int] = None
    device_id: Optional[str] = None
    host_key: Optional[str] = None
    host_key1: Optional[str] = None
    initstring: Optional[str] = None
    device_icon: Optional[str] = ""
    user_account: Optional[str] = None
    add_status: Optional[int] = None
    binding_type: Optional[int] = None
    protocol_version: Optional[int] = None
    aws_thing_name: Optional[str] = None
    iot_type: Optional[int] = None
    cloud_type: Optional[int] = None
    aws_cloud_compat: Optional[int] = None
    state: Optional[bool] = None
    is_rotate: Optional[bool] = None
    is_check: Optional[bool] = None
    device_icon_gray: Optional[str] = None
    is_wire_device: Optional[bool] = None
    wire_config_ip: Optional[str] = None
    comm_mode: Optional[int] = None
    ip_config: Optional[int] = None
    status: Optional[int] = 0
    factory: Optional[int] = -1

    def get_capability(self) -> Optional[Capability]:
        if isinstance(self.capability, str):
            try:
                cap_dict = json.loads(self.capability)
                return Capability.from_dict(cap_dict)
            except json.JSONDecodeError:
                return None
        elif isinstance(self.capability, dict):
            return Capability.from_dict(self.capability)
        else:
            return None

    # @classmethod
    # def from_dict(cls, data: dict) -> "BaseDeviceInfo":
    #     cap_raw = data.get("capability")
    #     print(cap_raw)
    #     if isinstance(cap_raw, str):
    #         try:
    #             cap_dict = json.loads(cap_raw)
    #             data["capability"] = Capability.from_dict(cap_dict)
    #         except json.JSONDecodeError:
    #             data["capability"] = None
    #     elif isinstance(cap_raw, dict):
    #         data["capability"] = Capability.from_dict(cap_raw)
    #     else:
    #         data["capability"] = None
    #     return super().from_dict(data)
