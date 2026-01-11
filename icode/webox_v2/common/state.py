import sys
import logging
import inspect
import streamlit as st

logger = logging.getLogger(__name__)


class StateItem(object):
    def __init__(self, key, default=None):
        self.key = key
        self.default = default
        st.session_state[key] = default
    
    def set(self, value):
        st.session_state[self.key] = value

    def get(self):
        _val = st.session_state[self.key]
        return _val

    @property
    def val(self):
        return self.get()

    def reset(self):
        self.set(self.default)


class StateStoreBase(object):
    def __init__(self):
        pass

    def items(self):
        _attrs = {}
        for attr_name, attr_val in self.__dict__.items():
            if isinstance(attr_val, StateItem):
                _attrs[attr_val.key] = attr_val.val
        return _attrs

    def keys(self):
        _attrs = self.items()
        return _attrs.keys()


class GlobalSessionState(StateStoreBase):
    def __init__(self):
        self.env = StateItem("env", default="local")


gst = GlobalSessionState()
