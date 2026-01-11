import sys
import logging 
import streamlit as st
from page.page import Page

logger = logging.getLogger(__name__)

class PostDetailPage(Page):
    def title(self):
        return "post detail"

    def write(self):
        # 页面渲染代码
        st.write("post detail page")

post_detail_page = PostDetailPage('post_detail_page')
