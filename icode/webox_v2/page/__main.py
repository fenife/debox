import sys
import logging 
import streamlit as st
from page.page import Page

logger = logging.getLogger(__name__)

class MainPage(Page):
    def title(self):
        return "main page"

    def write(self):
        # 页面渲染代码
        st.write("main page")

main_page = MainPage('main_page')

main_page.write()
