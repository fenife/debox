import sys
import logging 
import pandas as pd
import streamlit as st
from page.page import Page
from post import examples as exm

logger = logging.getLogger(__name__)

def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url, name)

class PostListPage(Page):
    def title(self):
        return "post list"

    def write(self):
        _post_list = []
        col = st.columns([2, 1, 1, 5, 3])
        col[0].write("name")
        col[1].write("user")
        col[2].write("cate")
        col[3].write("content")
        col[4].write("post detail")
        for p in exm.post_list:
            col = st.columns([2, 1, 1, 5, 3])
            col[0].write(p.title)
            col[1].write(p.user.name)
            col[2].write(p.cate.name)
            col[3].write(p.content)
            col[4].page_link("pages/post_detail.py", label="detail", query_params={"post_id": p.id})

        st.write(exm.post1.to_dict())
        st.write(exm.post1.user.to_dict())
        st.write(exm.post1.cate.to_dict())

    def on_click(self, post):
        return st.page_link("pages/post_detail.py", label="detail", query_params={"post_id": post.id})

    def write2(self):
        _post_list = []
        for p in exm.post_list:
            d = p.to_dict() 
            _post_list.append(d)

        df = pd.DataFrame(_post_list)
        df['detail'] = df.apply(lambda x: self.on_click(x), axis=1)

        st.dataframe(df)

        st.write(exm.post1.to_dict())
        st.write(exm.post1.user.to_dict())
        st.write(exm.post1.cate.to_dict())

post_list_page = PostListPage('post_list_page')

post_list_page.write()
