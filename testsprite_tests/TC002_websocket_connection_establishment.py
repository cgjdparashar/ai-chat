import socketio

WS_ENDPOINT = 'http://localhost:5000'

sio = socketio.Client()

def test_websocket_connection_establishment():
    try:
        sio.connect(WS_ENDPOINT, transports=['websocket'])
        assert sio.connected is True, 'WebSocket connection not open.'
        sio.disconnect()
    except Exception as e:
        assert False, f'WebSocket connection failed: {e}'

if __name__ == '__main__':
    test_websocket_connection_establishment()