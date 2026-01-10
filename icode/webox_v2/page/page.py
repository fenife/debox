import sys
import time
import logging 
import streamlit as st

logger = logging.getLogger(__name__)

class Page:
    def __init__(self, route):
        self.route_path = route

    def refresh_route(self):
        st.query_params["page"] = self.route_path

    def route(self):
        st.query_params["page"] = self.route_path
        time.sleep(0.2)  # 需要等待路由更新
        st.rerun()

    def get_route(self):
        return self.route_path

    def title(self):
        return "base page"

    def write(self):
        pass
