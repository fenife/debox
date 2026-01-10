import sys
import logging 
import streamlit as st
from page.page import Page

logger = logging.getLogger(__name__)

class ArticleUpdatePage(Page):

    def title(self):
        return "article update"
    
    def write(self):
        # 页面渲染代码
        st.write("article update page")

article_update_page = ArticleUpdatePage('article_update_page')
