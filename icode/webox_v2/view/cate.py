import sys
import logging
import streamlit as st
from post.mo import User, Category, Post
from view.post import PostTableView

logger = logging.getLogger(__name__)

class CateTableItemView(object):
    def __init__(self, cate):
        self.cate = cate   # type: Category
    
    def write(self):
        with st.expander(label="cate info", expanded=True):
            cols = st.columns([1, 1, 1, 3])
            cols[0].text("cate id: %s  " % self.cate.id)
            cols[1].text("cate name: %s" % self.cate.name)
            cols[2].text("user name: %s" % self.cate.user.name)

            with st.expander(label="post info", expanded=True):
                self.write_post_data()

    def write_post_data(self):
        pv = PostTableView(self.cate.posts)
        with st.container(border=True):
            pv.write()


class CateTableView(object):
    def __init__(self, cates):
        self.cates = cates   # type: list[Category]

    def _write_cate_button(self):
        with st.container(border=True):
            cols = st.columns([1, 1, 3])
            if cols[0].button("update"):
                st.switch_page("pages/user/user_update.py", query_params={"user_id": self.cate.user.id})

    def write(self):
        for cate in self.cates:
            cv = CateTableItemView(cate)
            cv.write()
        
        