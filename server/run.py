from server_public import create_server

import os

if __name__ == '__main__':

    app = create_server()
    app.run(debug=False, threaded=True)
