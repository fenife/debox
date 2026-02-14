import sys
import logging
import streamlit as st
from post.mo import User, Category, Post
from common.page import Page

logger = logging.getLogger(__name__)


class ExRadioWidget(object):
    def __init__(self, spec, label, key, options):
        self.spec = spec
        self.label = label
        self.key = key
        self.options = options

    @st.fragment
    def write(self):
        c1, c2 = st.columns(self.spec)
        ex_val = c1.text_input(label=self.label, key=self.key + "ex", value=None)
        val = c2.radio(label=self.label + "val", index=None, options=self.options, 
                       key= self.key + "val",
                       horizontal=True, label_visibility="hidden")
        res = ex_val or val
        return res

    @st.fragment
    def write2(self):
        with st.container(horizontal=True):
            _ival = st.text_input(label=self.label, key=self.key + "ex", value=None)
            _rval = st.radio(label=self.label + "val", index=None, options=self.options, 
                       key= self.key + "val",
                       horizontal=True, label_visibility="hidden")
            st.space("stretch")
        val = _rval or _ival
        return val


class UserCreatePage(Page):
    def title(self):
        return "user create"

    def write(self):
        # 页面渲染代码
        st.write("create user:")
        self.input_user_data()

    def input_user_data(self):
        with st.form("form:input_user_data"):
            user_id = st.number_input(
                label="user_id", value=None, placeholder="user id")
            name = st.text_input(label="username")
            with st.container(border=True):
                tab_c1, tab_c2 = st.tabs(["cate1", "cate2"])
                with tab_c1:
                    cate1 = self.input_cate_data(idx=1)
                with tab_c2:
                    cate2 = self.input_cate_data(idx=2)
            with st.container(border=True):
                c1, c2 = st.columns([1, 1])
                with c1:
                    cate3 = self.input_cate_data(idx=3)
            submitted = st.form_submit_button("Submit")
            if not submitted:
                return
            user = User(id=user_id, name=name, nickname=name)

        st.write(user)
        st.write(cate1)
        st.write(cate2)
        st.write(cate3)

    @st.fragment
    def input_cate_data(self, idx=1):
        user_id = st.number_input(label="user_id_%s" %
                                  idx, value=None, placeholder="user id")
        # user_id = c1.radio(label="user_id_%s" % idx, options=[1,2,3, "other"], horizontal=True)
        # user_id_ex = c2.number_input(label="ex_user_id_%s" % idx, value=None, placeholder="user id")

        options = [i for i in range(30)]
        cate_id = ExRadioWidget(spec=[1,8], label="cate id", key="cate_id_%s" % idx, options=options).write()
        # c1, c2 = st.columns([1, 9])
        # cate_id_ex = c1.number_input(
        #     label="cate id", key="ex cate id %s" % idx, value=None)
        # cate_id = c2.radio(label="cate_id_%s" % idx, index=None, options=[1, 2, 3],
        #                    horizontal=True, label_visibility="hidden")
        # cate_id = cate_id_ex or cate_id

        name = st.text_input(label="cate name %s" % idx)
        cate = Category(id=cate_id, user_id=user_id, name=name),
        return cate

    def input_user_id(self, user_id):
        if user_id != "other":
            return
        user_id = st.number_input(
            label="user_id", value=None, placeholder="user id")
        return user_id


user_create_page = UserCreatePage('user_create_page')

user_create_page.write()
