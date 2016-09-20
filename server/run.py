
from server_public import create_server
# from gevent.event import Event
#
# import eventlet
import os, thread, signal, sys
from time import sleep

# app = None
# socketio = None

# stopper = Event()

running = True
def kill_flask(signal, frame):
    print "[DEBUG Kill]"

    # socketio.disconnect()
    # stopper.set()
    sys.exit(0)
    # global running
    #
    # while running:
    #     try:
    #         print "[DEBUG] Tick"
    #         sleep(1)
    #     except KeyboardInterrupt:
    #         print "[DEBUG] Closing"
    #         running = False

if __name__ == '__main__':

    # Killer thread
    # thread.start_new_thread( kill_flask, (0, ) )
    signal.signal(signal.SIGINT, kill_flask)

    app, socketio = create_server()

    app.run(host="0.0.0.0", debug=False, threaded=True)
    # socketio.run(app)
    # eventlet.wsgi.server(eventlet.listen(('', 8000)), socketio)
