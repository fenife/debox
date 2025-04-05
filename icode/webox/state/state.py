import streamlit as st


class state(object):
    users = "users"
    cates = "cates"
    posts = "posts"

    user = "user"
    cate = "cate"
    post = "post"

    local_shells = "local_shells"
    vmc1_shells = "vmc1_shells"

    @staticmethod
    def get(key):
        return st.session_state[key]

    @staticmethod
    def set(key, val):
        st.session_state[key] = val

    @staticmethod
    def _init_one(key, val=None):
        if key not in st.session_state:
            st.session_state[key] = val

    @classmethod
    def clear_db_datas(cls):
        attrs = set([cls.users, cls.cates, cls.posts])
        for attr in attrs:
            cls.set(attr, None)

    @classmethod
    def clear_shells(cls):
        shell_attrs = set([cls.local_shells, cls.vmc1_shells])
        for attr in shell_attrs:
            cls.set(attr, [])

    @classmethod
    def init_all(cls):
        data_attrs = set([cls.users, cls.cates, cls.posts,
                          cls.user, cls.cate, cls.post])
        for attr in data_attrs:
            cls._init_one(attr, None)

        shell_attrs = set([cls.local_shells, cls.vmc1_shells])
        for attr in shell_attrs:
            cls._init_one(attr, [])

    @classmethod
    def clear_cache(self):
        st.cache_data.clear()
