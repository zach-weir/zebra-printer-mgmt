"""
    .PARAMETERS:
    - ZEBRA_MESSAGES:       Collection of various read data for Zebra printers
    - DATA_CATEGORIES:      Group collection of data into categories
"""

ZEBRA_MESSAGES = {
    "Status": "! U1 getvar \"device.status\"\r\n",
    "Hostname": "! U1 getvar \"device.friendly_name\"\r\n",
    "IP Address": "! U1 getvar \"ip.addr\"\r\n",
    "SSID": "! U1 getvar \"wlan.essid\"\r\n",
    "Model": "! U1 getvar \"device.product_name\"\r\n",
    "Serial Number": "! U1 getvar \"device.unique_id\"\r\n",
    "MAC Address": "! U1 getvar \"wlan.mac_raw\"\r\n",
    "LinkOS Version": "! U1 getvar \"appl.link_os_version\"\r\n",
    "Firmware Version": "! U1 getvar \"appl.name\"\r\n",
    "DHCP Required": "! U1 getvar \"wlan.ip.dhcp.required\"\r\n",
    "DHCP Option 81": "! U1 getvar \"ip.dhcp.option81\"\r\n",
    "WLAN Band Preference": "! U1 getvar \"wlan.band_preference\"\r\n",
    "WLAN Allowed Band": "! U1 getvar \"wlan.allowed_band\"\r\n",
    "Device Uptime": "! U1 getvar \"device.uptime\"\r\n",
    "Charging Status": "! U1 getvar \"power.chgr_status\"\r\n",
    "Default Port": "! U1 getvar \"wlan.ip.port\"\r\n",
    "Alternate Port": "! U1 getvar \"wlan.ip.port_alternate\"\r\n",
    "ZPL Mode": "! U1 getvar \"zpl.zpl_mode\"\r\n"
}

DATA_CATEGORIES = {
    "Status": ["Hostname", "Status", "Charging Status", "Device Uptime"],
    "Network": ["IP Address", "SSID", "Ports", "DHCP Required", "DHCP Option 81", "WLAN Band Preference", "WLAN Allowed Band"],
    "Hardware": ["Model", "Serial Number", "MAC Address", "ZPL Mode", "LinkOS Version", "Firmware Version"]
}