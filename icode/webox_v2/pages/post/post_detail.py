import sys
import logging
import streamlit as st
from page.page import Page
from post import examples as exm

logger = logging.getLogger(__name__)


class PostDetailPage(Page):
    def title(self):
        return "post detail"

    def write(self):
        # 页面渲染代码
        st.write(st.query_params.to_dict())
        post_ids = st.query_params.get_all("post_id")
        post_id = None
        if post_ids:
            post_id = int(post_ids[0])
        _post = None
        for p in exm.post_list:
            if p.id == post_id:
                _post = p
                break

        if not _post:
            st.info("post is empty")
            return

        st.write(_post.title)


post_detail_page = PostDetailPage('post_detail_page')

post_detail_page.write()
