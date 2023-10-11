import asyncio
import socket
from contextlib import suppress
from asyncio import CancelledError, TimeoutError
from aiowebostv import WebOsClient
from aiowebostv.exceptions import WebOsTvCommandError
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK, ConnectionClosedError

WEBOSTV_EXCEPTIONS = (
    OSError,
    ConnectionClosed,
    ConnectionClosedError,
    ConnectionClosedOK,
    ConnectionRefusedError,
    WebOsTvCommandError,
    TimeoutError,
    CancelledError,
)

sock = socket.socket()
sock.bind(('127.0.0.1', 12349))
sock.listen(10)
conn, addr = sock.accept()
butt = [
    "LEFT",
    "RIGHT",
    "UP",
    "DOWN",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "CHANNELUP",
    "CHANNELDOWN",
    "VOLUMEUP",
    "VOLUMEDOWN",
    "PLAY",
    "PAUSE",
    "STOP",
    "REWIND",
    "FASTFORWARD",
    "ASTERISK",
    "BACK",
    "EXIT",
    "ENTER",
    "AMAZON",
    "NETFLIX",
    "3D_MODE",
    "AD",  # Audio Description toggle
    "ASPECT_RATIO",  # Quick Settings Menu - Aspect Ratio
    "CC",  # Closed Captions
    "DASH",  # Live TV
    "GUIDE",
    "HOME",  # Home Dashboard
    "INFO",  # Info button
    "INPUT_HUB",  # Home Dashboard
    "LIST",  # Live TV
    "LIVE_ZOOM",  # Live Zoom
    "MAGNIFIER_ZOOM",  # Focus Zoom
    "MENU",  # Quick Settings Menu
    "MUTE",
    "MYAPPS",  # Home Dashboard
    "POWER",  # Power button
    "PROGRAM",  # TV Guide
    "QMENU",  # Quick Settings Menu
    "RECENT",  # Home Dashboard - Recent Apps
    "RECORD",
    "SAP",  # Multi Audio Setting
    "SCREEN_REMOTE",  # Screen Remote
    "TELETEXT",
    "TEXTOPTION",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]
inp = [
    "hdmi1",
    "hdmi2",
    "hdmi3",
    "livetv",
]
HOST = "192.168.10.8"
f = open('key.txt', 'r+') #file
KEY: str = f.read() #read key from file
#print(KEY)
f.close()


async def main():
    global conn #conection
    # global sock
    global addr #address
    global f #file
    global KEY #current key
    client = WebOsClient(HOST, KEY)
    while True:
        await asyncio.sleep(0.2)
        is_connected = client.is_connected()
        if is_connected:
            data = conn.recv(1024)
            bt = data.decode() #button = decode message from tcp socket
            if bt in butt: #if we find command in butt array
                await client.button(bt)
            elif bt in inp: # if we recive hdmi2 or livetv 
                #print("com.webos.app." + bt)
                await client.launch_app("com.webos.app." + bt)
            else:
                print("none")
            conn, addr = sock.accept()
            continue

        with suppress(*WEBOSTV_EXCEPTIONS):
            await client.connect()
            f = open('key.txt', 'r+')
            KEY = f.write(f"{client.client_key}")
            f.close()
            #print(f"Client key: {client.client_key}")


if __name__ == "__main__":
    asyncio.run(main())
