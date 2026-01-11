import sys
import logging
import streamlit as st
from post.mo import User, Category, Post
from page.page import Page

logger = logging.getLogger(__name__)


class UserCreatePage(Page):
    def title(self):
        return "user create"

    def write(self):
        # 页面渲染代码
        st.write("create user:")
        self.input_user_data()

    def input_user_data(self):
        with st.form("form:input_user_data"):
            user_id = st.number_input(label="user_id", value=None, placeholder="user id")
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
        user_id = st.number_input(label="user_id_%s" % idx, value=None, placeholder="user id")
        cate_id = st.number_input(label="cate_id_%s" % idx, value=None, placeholder="cate id")
        name = st.text_input(label="cate name %s" % idx)
        cate = Category(id=cate_id, user_id=user_id, name=name),
        return cate
 

user_create_page = UserCreatePage('user_create_page')

user_create_page.write()
