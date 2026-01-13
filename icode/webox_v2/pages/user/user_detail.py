import sys
import logging
import pandas as pd
import streamlit as st
from common.page import Page
from view.user import UserDetailView
from post import examples as exm

logger = logging.getLogger(__name__)

class UserDetailPage(Page):
    def title(self):
        return "user detail"

    def get_user(self):
        user_ids = st.query_params.get_all("user_id")
        user_id = int(user_ids[0]) if user_ids else None
        default_user_idx = 0
        users = [None] + exm.user_list
        if user_id:
            for _user in exm.user_list:
                if user_id == _user.id:
                    logger.info("user_id: %s, user.id: %s, name: %s", user_id, _user.id, _user.name)
                    default_user_idx = exm.user_list.index(_user) + 1
        
        user = st.selectbox(label="select user", options=users, index=default_user_idx) 
        return user
    
    def write_posts(self, posts):
        _post_list = [p.to_dict() for p in posts]
        df = pd.DataFrame(_post_list)
        st.dataframe(df)

    def write(self):
        # 页面渲染代码
        st.write("query_params: ", str(st.query_params.to_dict()))
        user = self.get_user()
        if not user:
            return
        
        uv = UserDetailView(user)
        uv.write()


user_detail_page = UserDetailPage('user_detail_page')

user_detail_page.write()
