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
        col[4].page_link("pages/post/post_detail.py",
                         label="detail", query_params={"post_id": p.id})
        col[5].page_link("pages/user/user_detail.py",
                         label="user", query_params={"user_id": p.user_id})
        _key = "del_post_%s" % self.post.id
        if col[6].button(label="delete", key=_key):
            self.delete_post()

    @st.dialog("dialog: delete_post")
    def delete_post(self):
        with st.form("form: delete_post"):
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.info("delete post: %s" % self.post.id)


class PostTableColunms(object):
    def __init__(self):
        self._col_spec = [0.5, 1, 1, 1, 3, 1, 1, 1]
        cols = st.columns(self._col_spec)
        self.cols = cols
        self.id = cols[0]
        self.name = cols[1]
        self.user = cols[2]
        self.cate = cols[3]
        self.content = cols[4]
        self.detail_link = cols[5]
        self.user_link = cols[6]
        self.del_btn = cols[7]


class PostTableView(object):
    def __init__(self, posts):
        self._col_spec = [0.5, 1, 1, 1, 3, 1, 1, 1]
        self._posts = posts

    def write(self):
        st.text("post list, len: %s" % len(self._posts))
        with st.container(border=True):
            self.write_title()
            self.write_data()

    def write_title(self):
        c = PostTableColunms()
        c.id.write("id")
        c.name.write("name")
        c.user.write("user")
        c.cate.write("cate")
        c.content.write("content")
        c.detail_link.write("post detail")
        c.user_link.write("user")
        c.del_btn.write("delete")

    def write_data(self):
        for post in self._posts:
            # pv = PostTableItemView(post, self._col_spec)
            # pv.write()
            self.write_post_data(post)

    def write_post_data(self, post):
        p = post    # type: Post
        c = PostTableColunms()
        c.id.write(p.id)
        c.name.write(p.title)
        c.user.write(p.user.name)
        c.cate.write(p.cate.name)
        c.content.write(p.content)
        c.detail_link.page_link("pages/post/post_detail.py",
                         label="detail", query_params={"post_id": p.id})
        c.user_link.page_link("pages/user/user_detail.py",
                         label="user", query_params={"user_id": p.user_id})
        _key = "del_post_%s" % post.id
        if c.del_btn.button(label="delete", key=_key):
            self.delete_post(p)

    @st.dialog("dialog: delete_post")
    def delete_post(self, post):
        with st.form("form: delete_post"):
            submitted = st.form_submit_button("Confrim")
            if submitted:
                self._posts.remove(post)
                st.info("delete post: %s" % post.id)
                st.rerun()
