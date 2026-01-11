import sys
import logging
import streamlit as st
from post.mo import User, Category, Post
from view.post import PostTableView
from view.cate import CateTableView

logger = logging.getLogger(__name__)

class UserDetailView(object):
    def __init__(self, user):
        self._user = user   # type: User
    
    def write(self):
        self.write_user_data()
        self.write_user_button()
        self.write_cate_data()
    
    def write_user_data(self):
        with st.container(border=True):
            st.markdown("**user info:**")
            cols = st.columns([1, 1, 3])
            cols[0].text("user id: %s  " % self._user.id)
            cols[1].text("user name: %s" % self._user.name)

    def write_user_button(self):
        with st.container(border=True):
            cols = st.columns([1, 1, 3])
            if cols[0].button("update"):
                st.switch_page("pages/user/user_update.py", query_params={"user_id": self._user.id})

    def write_cate_data(self):
        cv = CateTableView(self._user.cates)
        with st.container(border=True):
            st.markdown("**cate info:**")
            cv.write()
        