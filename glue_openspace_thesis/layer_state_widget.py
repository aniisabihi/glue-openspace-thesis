from __future__ import absolute_import, division, print_function

import os

from qtpy.QtWidgets import QWidget

from glue.external.echo.qt import autoconnect_callbacks_to_qt
from glue.utils.qt import load_ui, fix_tab_widget_fontsize

__all__ = ['OpenSpaceLayerStateWidget']


class OpenSpaceLayerStateWidget(QWidget):

    def __init__(self, layer_artist):

        super(OpenSpaceLayerStateWidget, self).__init__()

        self.ui = load_ui('layer_state_widget.ui', self, directory=os.path.dirname(__file__))

        fix_tab_widget_fontsize(self.ui.tab_widget)

        self.state = layer_artist.state

        self.layer_artist = layer_artist
        self.layer = layer_artist.layer

        connect_kwargs = {'value_alpha': dict(value_range=(0., 1.))}
        self._connect = autoconnect_callbacks_to_qt(self.state, self.ui, connect_kwargs)

        # Set initial values
        self._update_size_mode()
        self._update_color_mode()

        self._viewer_state = layer_artist._viewer_state

        self.ui.button_center.setVisible(False)

    def _update_size_mode(self, *args):

        self.ui.size_row_2.hide()
        self.ui.combosel_size_att.hide()
        self.ui.valuetext_size.show()

    def _update_color_mode(self, *args):

        self.ui.color_row_2.hide()
        self.ui.color_row_3.hide()
        self.ui.combosel_cmap_att.hide()
        self.ui.spacer_color_label.show()
        self.ui.color_color.show()
