import sys
import logging
import streamlit as st

# from page.page import Page
# from page.post_create import post_create_page
# from page.post_list import post_list_page
# from page.post_detail import post_detail_page
# from page.post_update import post_update_page

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d:%(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

st.set_page_config(layout="wide")

pages = {
    # "main": [
    #     st.Page("pages/main.py", title="main page"),
    # ],
    "user": [
        st.Page("pages/user/user_detail.py", title="user"),
    ],
    "post": [
        st.Page("pages/post/post_list.py", title="post list"),
        st.Page("pages/post/post_detail.py", title="post detail"),
        st.Page("pages/post/post_create.py", title="post create"),
        st.Page("pages/post/post_update.py", title="post update"),
    ],
    "category": [
    ],
}

pg = st.navigation(pages)
pg.run()

# class MultiApp:
#     """
#     整个平台的主页面，所有子页面需要按照它的标准进行初始化. 每个子页面对象都要集成page.page中的Page父类
#     """

#     def __init__(self):
#         self.nav_pages = []
#         self.extra_pages = []

#     def add_nav_page(self, page):
#         # type: (Page) -> None
#         """ 这里定义的页面会显示在侧边导航栏
#         page: 页面对象, 该对象需要继承page.page中的Page父类
#         """
#         self.nav_pages.append(page)

#     def add_extra_page(self, page):
#         # type: (Page) -> None
#         """ 这里定义的页面不会显示在侧边导航栏
#         page: 页面对象， 该页面不会显示在侧边导航栏
#         """
#         self.extra_pages.append(page)

#     def run(self):
#         """
#         负责主页面显示的函数，主要通过以下步骤：
#         1. 定义侧边导航栏架构
#         2. 获取当前url中是否已经设定了page参数, 如果有page参数则遍历已注册的所有页面对象并导航到对应的页面,
#            如果没有则直接显示默认首页
#         """

#         # ratio的回调函数, 负责设置url并导航到对应子页面
#         def change_route():
#             # 获取当前被选中的页面
#             _page = st.session_state['page_key']  # type: Page
#             _page.refresh_route()   # 重置url中的参数

#         # 获取当前URL中是否已经带了page参数， page参数决定了应该显示哪个子页面.
#         route = st.query_params.get('page')
#         default_page_idx = 0
#         if route:
#             for _page in self.nav_pages:
#                 if route == _page.get_route():
#                     default_page_idx = self.nav_pages.index(_page)
#                 # else:
#                 #     _page.write()

#         # step 1: 定义侧边导航栏架构
#         st.sidebar.title("页面导航")
#         with st.sidebar.expander("页面集合", expanded=True):
#             _page = st.radio(
#                 'select_page',
#                 self.nav_pages,
#                 format_func=lambda pa: pa.title(),
#                 on_change=change_route,
#                 key="page_key",
#                 index=default_page_idx,
#             )
#         url = 'http://feng-dev:8012/'
#         st.markdown(f'<a href="{url}" target="_self">{"返回首页"}</a>', unsafe_allow_html=True)
#         if route:
#             for _page in self.nav_pages:
#                 if route == _page.get_route():
#                     _page.write()
#             for _page in self.extra_pages:
#                 if route == _page.get_route():
#                     _page.write()
#         else:
#             _page.refresh_route()
#             _page.write()


# st.set_page_config(layout='wide')
# app = MultiApp()
# # 开始注册效果测试侧边栏
# app.add_nav_page(post_list_page)
# app.add_nav_page(post_create_page)
# app.add_nav_page(post_update_page)

# app.add_extra_page(post_detail_page)

# # app.add_extra_app(mllm_test_compare)
# # app.add_extra_app(doc_parse_compare)
# # app.add_extra_app(doc_parse_data_detail)
# app.run()
