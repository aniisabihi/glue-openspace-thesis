import os
import time
import socket

from qtpy.QtCore import Qt
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QWidget

from glue.utils.qt import messagebox_on_error
from glue.viewers.common.qt.data_viewer import DataViewer

from .viewer_state import OpenSpaceViewerState
from .layer_artist import OpenSpaceLayerArtist, protocol_version
from .viewer_state_widget import OpenSpaceViewerStateWidget
from .layer_state_widget import OpenSpaceLayerStateWidget

__all__ = ['OpenSpaceDataViewer']

LOGO = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logo.png'))

# Time to wait after sending websocket message
WAIT_TIME = 0.01


class OpenSpaceDataViewer(DataViewer):

    LABEL = 'OpenSpace Viewer'
    _state_cls = OpenSpaceViewerState
    _options_cls = OpenSpaceViewerStateWidget
    _layer_style_widget_cls = OpenSpaceLayerStateWidget
    _data_artist_cls = OpenSpaceLayerArtist
    _subset_artist_cls = OpenSpaceLayerArtist

    socket = None

    def __init__(self, *args, **kwargs):
        super(OpenSpaceDataViewer, self).__init__(*args, **kwargs)
        self._logo = QLabel()
        self._image = QPixmap.fromImage(QImage(LOGO))
        self._logo.setPixmap(self._image)
        self._logo.setAlignment(Qt.AlignCenter)

        self._ip = QLineEdit()
        self._ip.setText('http://localhost:4700/')
        self._button = QPushButton('Connect')
        self._button.clicked.connect(self.connect_to_openspace)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._logo)
        self._horizontal = QHBoxLayout()
        self._horizontal.addWidget(self._ip)
        self._horizontal.addWidget(self._button)
        self._layout.addLayout(self._horizontal)
        self._main = QWidget()
        self._main.setLayout(self._layout)

        self.setCentralWidget(self._main)

    @messagebox_on_error('An error occurred when trying to connect to OpenSpace:', sep=' ')
    def connect_to_openspace(self, *args):
        self.reset_socket()
        print('Connected to OpenSpace')
        self._button.setEnabled(False)
        self._button.setText('Connected')
        time.sleep(WAIT_TIME)

        for layer in self.layers:
            layer.update()

        # Create and send "Connection" message to OS
        message_type = "CONN"
        subject = "Glue-Viz"
        length_of_subject = str(format(len(subject), "09"))
        message = protocol_version + message_type + length_of_subject + subject
        self.socket.send(bytes(message, 'utf-8'))

    def reset_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.socket.settimeout(0.0)
        self.socket = socket.create_connection(('localhost', 4700))

    def get_layer_artist(self, cls, layer=None, layer_state=None):
        return cls(self, self.state, layer=layer, layer_state=layer_state)
