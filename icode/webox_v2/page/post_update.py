import sys
import logging 
import streamlit as st
from page.page import Page

logger = logging.getLogger(__name__)

class PostUpdatePage(Page):

    def title(self):
        return "post update"
    
    def write(self):
        # 页面渲染代码
        st.write("post update page")

post_update_page = PostUpdatePage('post_update_page')
