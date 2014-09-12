import os
import sys
app_root = os.path.dirname(__file__)
os.chdir(app_root)
sys.path.append(app_root)
sys.path.append(
    os.path.normpath(
        os.path.join(
            app_root,
            '../../../python'
        )
    )
)

import hashlib
import base64
import time

def application(env, start_response):
    secKey = env['HTTP_SEC_WEBSOCKET_KEY']

    hash_result = hashlib.new(
        "sha1",
        (secKey + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()
    ).digest()

    base64_result = base64.encodestring(hash_result)
    resKey = base64_result.decode().split('\n')[0]

    write = start_response(
        '101 Switching Protocols',
        [
            # ('Content-Type', 'bin/socket'),
            ('Upgrade', 'websocket'),
            ('Connection', 'Upgrade'),
            ('Sec-WebSocket-Accept', resKey),
            # ('Content-Length', '10000'),
        ]
    )

    # yield b'11'
    # print(1)
    # time.sleep(10)

    # yield b'22'
    # print(2)

    # time.sleep(10)

    send_data = b'abcdefghikkk'
    write(bytes([0x81, len(send_data)]))
    write(send_data)
    print(3)

    time.sleep(10)
