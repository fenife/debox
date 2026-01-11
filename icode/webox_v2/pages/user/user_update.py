import sys
import logging
import streamlit as st
from page.page import Page

logger = logging.getLogger(__name__)


class UserUpdatePage(Page):
    def title(self):
        return "user update"

    def write(self):
        # 页面渲染代码
        st.write("user update page")


user_update_page = UserUpdatePage('user_update_page')

user_update_page.write()
