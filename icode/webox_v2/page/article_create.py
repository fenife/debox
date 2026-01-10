import sys
import logging 
import streamlit as st
from page.page import Page

logger = logging.getLogger(__name__)

class ArticleCreatePage(Page):
    def title(self):
        return "article create"

    def write(self):
        # 页面渲染代码
        st.write("article create page")

article_create_page = ArticleCreatePage('article_create_page')
