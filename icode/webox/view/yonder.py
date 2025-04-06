
from collections import namedtuple
import datetime
import json
import streamlit as st
from domain.yonder import PostDomain
from engine.db import DBClient, DBResult
from engine.http import HttpClient
from state import sess_state as ss
from view.base import BaseViewer
from domain import yds


def _format_select_label(r: namedtuple):
    s = f"{r.id}-{r.name}"
    return s


class UserViewer(BaseViewer):

    def view_users(self):
        self.view_user_buttons()
        self.view_dataframe(ss.get(ss.Bos.Users))

    def get_users(self):
        users = yds.get_users()
        ss.set(ss.Bos.Users, users)

    def view_user_buttons(self):
        with st.container(border=True):
            cols = st.columns(7)
            # st.markdown("##### user")
            if cols[0].button("users (db)"):
                self.get_users()

            if cols[1].button("add user"):
                self.create_user()

    @st.dialog("dialog:create_user", width="large")
    def create_user(self):
        with st.form("form:create_user"):
            username = st.text_input(label="username")
            passwd = st.text_input(label="password")
            submitted = st.form_submit_button("Submit")
            if not submitted:
                return
            result = yds.create_user(username, passwd)
            self.view_http_result(result)


class CateViewer(BaseViewer):

    def view_cates(self):
        self.view_cate_buttons()
        self.view_dataframe(ss.get(ss.Bos.Users))

    def get_cates(self):
        cates = yds.get_cates()
        ss.set(ss.Bos.Cates, cates)

    def view_cate_buttons(self):
        with st.container(border=True):
            cols = st.columns(7)
            if cols[0].button("categories (db)"):
                self.get_cates()

            if cols[1].button("add category"):
                self.create_category()

    @st.dialog("dialog:create_category", width="large")
    def create_category(self):
        with st.form("form:create_category"):
            cate_name = st.text_input(label="category name")
            submitted = st.form_submit_button("Submit")
            if not submitted:
                return
            result = yds.create_category(cate_name)
            self.view_http_result(result)


class PostViewer(BaseViewer):

    def view_posts(self):
        self.view_post_buttons()
        self.view_dataframe(ss.get(ss.Bos.Posts))

    def get_posts(self):
        posts = yds.get_posts()
        ss.set(ss.Bos.Posts, posts)

    def view_post_buttons(self):
        with st.container(border=True):
            cols = st.columns(7)
            if cols[0].button("posts (db)"):
                self.get_posts()

            if cols[1].button("add post"):
                self.create_post()

    @st.dialog("dialog:create_post", width="large")
    def create_post(self):
        with st.form("form:create_post"):
            title = st.text_input(label="title")
            title_en = st.text_input(label="title_en")
            user = st.selectbox(label="user", index=None,
                                options=yds.get_select_users(),
                                format_func=_format_select_label)
            cate = st.selectbox(label="category", index=None,
                                options=yds.get_select_cates(),
                                format_func=_format_select_label)
            content = st.text_area(label="content")
            submitted = st.form_submit_button("Submit")
            if not submitted:
                return
            result = yds.create_post(title=title, title_en=title_en,
                                     content=content,
                                     user_id=user.id if user else "",
                                     cate_id=cate.id if cate else "")
            self.view_http_result(result)


class YonderViewer(UserViewer, CateViewer, PostViewer):
    pass
