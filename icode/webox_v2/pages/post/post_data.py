import sys
import logging 
import pandas as pd
import streamlit as st
from common.page import Page
from post import examples as exm

logger = logging.getLogger(__name__)


class DataTableView(object):
    def __init__(self, rows=None, title=None):
        self.rows = rows
        self.title = title

    def write(self):
        pass


class PostListPage(Page):
    def title(self):
        return "post list"

    def write(self):
        pv = DataTableView(exm.post_list)
        pv.write()

        st.write("info:")
        _post = exm.post_list[0]
        st.write(_post.to_dict())
        st.write(_post.user.to_dict())
        st.write(_post.cate.to_dict())


post_list_page = PostListPage('post_list_page')

post_list_page.write()
