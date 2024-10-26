from collections import namedtuple
import datetime
import json
import streamlit as st
from engine.db import DBClient, DBResult
from engine.http import HttpClient
from config import Config
from state.state import state
from domain.base import BaseDomainService
from vo import vo


CACHE_TTL = 10
# hash_funcs, key: class type
cache_hash_funcs = {"domain.yonder.YonderDomainService": lambda x: str(x)}


class UserDomain(BaseDomainService):

    @st.cache_data(ttl=CACHE_TTL, hash_funcs=cache_hash_funcs)
    def get_users(self):
        sql = "select * from users"
        result = self.db.query(sql, label=vo.nt.User)
        return result

    def get_select_users(self):
        result = self.get_users()
        return result.items()

    def create_user(self, name, passwd):
        url = "/api/v1/user/signup"
        body = {"name": name, "password": passwd}
        resp = self.http.post(url, body=body)
        return resp


class CateDomain(BaseDomainService):

    @st.cache_data(ttl=CACHE_TTL, hash_funcs=cache_hash_funcs)
    def get_cates(self):
        sql = "select * from categories"
        result = self.db.query(sql, label=vo.nt.Category)
        return result

    def get_select_cates(self):
        result = self.get_cates()
        return result.items()

    def create_category(self, name):
        url = "/api/v1/category"
        body = {"name": name}
        resp = self.http.post(url, body=body)
        return resp


class PostDomain(BaseDomainService):

    @st.cache_data(ttl=CACHE_TTL, hash_funcs=cache_hash_funcs)
    def get_posts(self):
        sql = "select * from posts"
        result = self.db.query(sql, label=vo.nt.Post)
        return result

    def create_post(self, title, title_en, content, user_id, cate_id):
        url = "/api/v1/post"
        body = {"title": title,
                "title_en": title_en,
                "content": content,
                "cate_id": cate_id,
                "user_id": user_id}
        resp = self.http.post(url, body=body)
        return resp


class YonderDomainService(UserDomain, CateDomain, PostDomain):
    pass
