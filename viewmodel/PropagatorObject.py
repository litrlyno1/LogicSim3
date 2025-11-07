from viewmodel.PropagatorRelay import PropagatorRelay
from model.Propagator import Propagator

class PropagatorObject:
    
    def __init__(self, id : str, propagator : Propagator, **kwargs):
        self._propagatorRelay = PropagatorRelay(id, propagator)
        super().__init__(**kwargs)
    
    @property
    def valueChanged(self):
        return self._propagatorRelay.valueChanged