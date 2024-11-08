status_210 = bytes(
    [
        0x00,  # Centurion
        0x00,  # Cabled
        0xFF,  # Counter
        0x81,  # Calibrated, Left Heel button pressed
        0x00,
        0x00,  # Treadle count
        0x01,  # Laser FootSwitch connected
        0x00,  # Reserved
    ]
)

status_211_battery = bytes(
    [
        0x00,
        0x00,
        0x00,  # Reserver
        0x03,  # Battery Status 1
        0x8F,  # Charging, level 16 %
        0x02,  # Battery Low
        0x10,  # Temperature
        0x0F,  # SoH
    ]
)
