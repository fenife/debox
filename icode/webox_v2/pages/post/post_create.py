import sys
import logging
import streamlit as st
from page.page import Page
from post import examples as exm

logger = logging.getLogger(__name__)


class PostCreatePage(Page):
    def title(self):
        return "post create"

    def write(self):
        # 页面渲染代码
        st.write("post create page")


post_create_page = PostCreatePage('post_create_page')

post_create_page.write()
