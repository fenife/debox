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
        col = st.columns([1, 1, 1, 5, 3])
        col[0].write("name")
        col[1].write("user")
        col[2].write("cate")
        col[3].write("content")
        col[4].write("post detail")
        for p in exm.post_list:
            col = st.columns([1, 1, 1, 5, 3])
            col[0].write(p.title)
            col[1].write(p.user.name)
            col[2].write(p.cate.name)
            col[3].write(p.content)
            col[4].page_link("pages/post_detail.py", query_params={"page": "post_detail_page"})

            # d = p.to_dict() 
            # d["url"] = "http://feng-dev:8012?page=post_detail&post_id=%s" % p.id
            # _post_list.append(d)

        # df = pd.DataFrame(_post_list)
        # df['link'] = df.apply(lambda x: make_clickable(x['url'], x['title']), axis=1)

        # df = df.to_html(escape=False)

        # st.dataframe(df)
        # st.html(df)

        st.write(exm.post1.to_dict())
        st.write(exm.post1.user.to_dict())
        st.write(exm.post1.cate.to_dict())

post_list_page = PostListPage('post_list_page')
