import streamlit as st
from libx.utils import EnumBase


def get(k):
    return st.session_state[k]

def set(k, v):
    st.session_state[k] = v

class StateBase(EnumBase):
    _default_vals = {}

    @classmethod
    def _set_default_val(cls, k):
        if not isinstance(k, str):
            return
        v = cls._default_vals.get(k, None)
        st.session_state[k] = v

    @classmethod
    def init_all(cls):
        for k in cls.enums():
            if k not in st.session_state:
                cls._set_default_val(k)
    
    @classmethod
    def clear_all(cls):
        for k in cls.enums():
            cls._set_default_val(k)


class Bos(StateBase):
    Users = "users"
    User = "user"
    Cates = "cates"
    Cate = "cate"
    Posts = "posts"
    Post = "post"


class Shell(StateBase):
    local_shells = "local_shells"
    vmc1_shells = "vmc1_shells"

    _default_vals = {
        local_shells: [],
        vmc1_shells: [],
    }


class Env(StateBase):
    Env = "env"
    # Local = "local"
    # Dev = "dev"

    @classmethod
    def get_env(cls):
        env = get(cls.Env)
        if not env:
            env = "local"
        return env

    @classmethod
    def set_env(cls, env):
        set(cls.Env, env)


def init_states():
    Bos.init_all()
    Shell.init_all()
    Env.init_all()

def clear_states():
    Bos.clear_all()
    Env.clear_all()


