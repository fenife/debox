import sys
import logging
import streamlit as st
from post.mo import User, Category, Post

logger = logging.getLogger(__name__)

class PostTableItemView(object):
    def __init__(self, post, spec):
        self._col_spec = spec
        self.post = post   # type: Post
    
    def write(self):
        self.write_post_data()

    def write_post_data(self):
        p = self.post
        col = st.columns(self._col_spec)
        col[0].write(p.title)
        col[1].write(p.user.name)
        col[2].write(p.cate.name)
        col[3].write(p.content)
        col[4].page_link("pages/post/post_detail.py", label="detail", query_params={"post_id": p.id})
        col[5].page_link("pages/user/user_detail.py", label="user", query_params={"user_id": p.user_id})


class PostTableView(object):
    def __init__(self, posts):
        self._col_spec = [1, 1, 1, 3, 1, 1, 1]
        self._posts = posts

    def write(self):
        self.write_title()
        self.write_data()

    def write_title(self):
        cols = st.columns(self._col_spec)
        cols[0].write("name")
        cols[1].write("user")
        cols[2].write("cate")
        cols[3].write("content")
        cols[4].write("post detail") 
        cols[5].write("user") 

    def write_data(self):
        for post in self._posts:
            pv = PostTableItemView(post, self._col_spec)
            pv.write()
