import sys
import logging 
import pandas as pd
import streamlit as st
from page.page import Page
from post import examples as exm
from view.post import PostTableView

logger = logging.getLogger(__name__)

def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url, name)

class PostListPage(Page):
    def title(self):
        return "post list"

    def write(self):
        pv = PostTableView(exm.post_list)
        pv.write()

        st.write("info:")
        _post = exm.post_list[0]
        st.write(_post.to_dict())
        st.write(_post.user.to_dict())
        st.write(_post.cate.to_dict())


post_list_page = PostListPage('post_list_page')

post_list_page.write()
