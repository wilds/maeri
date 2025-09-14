SET_CLOUD_UPLOAD_ENABLE = 53          # enable (0 = off, 1 = on)
SET_LED_ENABLE = 103                  # status (0 = spento, 1 = acceso)
SET_ANTI_JAMMING_ENABLE = 223        # status (0 = disattivato, 1 = attivato)
SET_WATERMARK_SWITCH = 191            # status (0 = disattivato, 1 = attivato)
REMOVE_IPC_FROM_NVR = 830             # fisso 1 (rimuove IPC dal NVR)
SET_NVR_CHANNEL_LED_ENABLE = 103     # status (0 = off, 1 = on), con channelId (es. 1–16)
SET_UPDATE_ENABLE = 203               # status (0 = no update automatico, 1 = update automatico)
SET_ROTATE_ENABLE = 102               # status (0 = disattiva rotazione, 1 = attiva)
SET_MOTION_DETECTION_ENABLE = 106    # enable (0 = off, 1 = on)
SET_MOTION_DETECTION_SENSITIVITY = 107 # sensitivity (1–5 o 1–10)
SET_SOUND_DETECTION_ENABLE = 109     # status (0 = off, 1 = on)
SET_SOUND_DETECTION_SENSITIVITY = 110 # sensitivity (1–5 o 1–10)

SET_SD_RECORD_VIDEO_ENABLE = 140      # enable (0 = disattivo, 1 = attivo)
SET_PLAYBACK_RECORD_VIDEO_TYPE = 104  # type (0 = continuo, 1 = movimento)
SET_PLAYBACK_RECORD_VIDEO_DURATION = 105  # duration (es. 60, 180, 300...), convertito via JsonUtil.sdRecordDurationToIot()
SET_SD_RECORD_TYPE = 104              # type (0 = continuo, 1 = evento)
SET_SD_RECORD_DURATION = 105          # duration (es. 60, 180, 300...)
SET_DAY_NIGHT_MODE = 113              # status (0 = giorno, 1 = notte, 2 = auto)
SET_TIMING = 283                      # JSON {"from": "08:00", "to": "18:00"}
SET_FULL_COLOR_MODE = 209             # status (0 = normale, 1 = colore pieno)
SET_H265_ENABLE = 124                 # status (0 = H.264, 1 = H.265)

SET_VIDEO_PWD_SWITCH = 216            # switch (0 = disattivo, 1 = attivo)
SET_VIDEO_PWD = 217                   # password codificata Base64 (usata se switch = 1)

SWITCH_WIFI = 260                     # JSON {"name": "...", "passwd": "..."}

SET_BASE_SOUND_VOLUME = 262           # volume (0–100)

SET_ONVIF_ENABLE = 121                # status (0 = off, 1 = on)
SET_ONVIF_PWD = 122                   # password codificata Base64

SET_HUMAN_TRACK_ENABLE = 112          # status (0=off, 1=on)
SET_HUMAN_DET_ENABLE = 108            # status (0=off, 1=on)
SET_HUMAN_DET_DAY_ENABLE = 174        # status (0=off, 1=on)
SET_HUMAN_DET_NIGHT_ENABLE = 173      # status (0=off, 1=on)
SET_HUMAN_FRAME_ENABLE = 117          # status (0=off, 1=on)
SET_CRY_DET_ENABLE = 111              # status (0=off, 1=on)
SET_ABNORMAL_NOISE_INSPECTION_ENABLE = 195  # status (0=off, 1=on)

SET_WORK_MODE = 201                   # workmode int (es: 0=normal, 1=away, ecc.)
SET_AOV_WORK_MODE = 275               # custom AOV workmode int
SET_LOCATOR_WORK_MODE = 282           # locator-specific mode int

SET_ANTIFLICKER_MODE = 202            # antiflicker (0=off, 1=50Hz, 2=60Hz)
SET_MICROPHONE_ENABLE = 207           # status microfono (0=off, 1=on) – nome parametro ambiguo
SET_SPEAKER_ENABLE = 208              # status speaker (0=off, 1=on)
SET_RAE_ENABLE = 211                  # status RAE (0=off, 1=on)

SET_SLEEP_MODE = 118                  # mode int (0=sleep, 1=awake)
SET_SLEEP_TIME_LIST = 119             # timeList string JSON o formato custom
SET_ALARM_PLAN_LIST = 125             # timeList string JSON o formato custom
SET_TIMING_RECORD_TIMES = 145         # timeList string JSON o formato custom

SET_WATCH_POSITION = 278              # JSON string con campi v_id, enable, preset_no, time
SET_BELL_PHONE = 212                  # numero di telefono (string)

SET_CHIME_PLAN_LIST = 137             # timeList string JSON o formato custom
SET_LIGHTING_PLAN_LIST = 186          # timeList string JSON o formato custom

FORMAT_SDCARD = 806                   # param: timestamp (string)
UPGRADE_FIRMWARE = 803                # param: OTAUpgradeInfo (string firmware info)
REFRESH_PROPERTY = 809                # param: propertyList (stringified JSON array di property IDs)

GET_SD_CARD_INFO = "809"              # codici 114, 115, 116, 290 + param t (timestamp)
START_PTZ = "807"                     # params: ps (pan), ts (tilt), zs (zoom), t (timestamp)
STOP_PTZ = "808"                      # param t (timestamp)
START_PATROL = "822"                  # param t (timestamp)
SET_TIMED_PATROL = "196"              # timeList stringa di orari

SET_ALL_ALARMS_ENABLE = "825"         # enable (0/1)

SET_PET_FEED_ENABLE = "845"            # enable (0/1)
SET_PET_FEED_PORTIONS = "850"          # parts (numero porzioni)

SET_PIR_DETECTION_ENABLE = "150"       # enable (0/1)
SET_PIR_DETECTION_SENSITIVITY = "151"  # sensitivity (es. 1-3)

SET_ALARM_AREA_ENABLE = "177"          # enable (0/1), width, height, bitmap
SET_ALARM_FREQUENCY = "178"            # alarmFrequency int (es. secondi o frequenza)

SET_HUMAN_DETECTION_SENSITIVITY = "224"  # sensitivity int (es. 1-3)

SET_SPEAK_VOLUME = "152"               # volume int (0-100)

SET_MECHANICAL_CHIME_ENABLE = "161"   # enable (0/1)
SET_WIRELESS_CHIME_ENABLE = "157"     # enable (0/1)
SET_WIRELESS_CHIME_VOLUME = "158"     # volume int (0-100)
SET_WIRELESS_CHIME_SELECT_SONG = "160"  # song nome o ID del brano

#TODO: add others commands