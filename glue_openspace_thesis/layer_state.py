from __future__ import absolute_import, division, print_function

from glue.external.echo import (CallbackProperty, keep_in_sync)
from glue.viewers.common.state import LayerState

__all__ = ['OpenSpaceLayerState']


class OpenSpaceLayerState(LayerState):

    layer = CallbackProperty()
    color = CallbackProperty()
    size = CallbackProperty()
    alpha = CallbackProperty()

    def __init__(self, layer=None, **kwargs):

        self._sync_markersize = None

        super(OpenSpaceLayerState, self).__init__(layer=layer)

        self._sync_color = keep_in_sync(self, 'color', self.layer.style, 'color')
        self._sync_alpha = keep_in_sync(self, 'alpha', self.layer.style, 'alpha')
        self._sync_size = keep_in_sync(self, 'size', self.layer.style, 'markersize')

        self.color = self.layer.style.color
        self.size = self.layer.style.markersize
        self.alpha = self.layer.style.alpha

        self.update_from_dict(kwargs)

    def _layer_changed(self):

        super(OpenSpaceLayerState, self)._layer_changed()

        if self._sync_markersize is not None:
            self._sync_markersize.stop_syncing()

        if self.layer is not None:
            self.size = self.layer.style.markersize
            self._sync_markersize = keep_in_sync(self, 'size', self.layer.style, 'markersize')
