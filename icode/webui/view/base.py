import inspect
from loguru import logger
from pandas.core.arrays.categorical import contains
import streamlit as st
from engine.db import DBClient, DBResult
from engine.http import HttpClient, HttpResult
from config import Config


class BaseViewer(object):

    def view_dataframe_query(self, data: DBResult):
        caller = inspect.stack()[2].function
        label = f"{caller}:{data.label}"
        help_str = " f > 1 or f == 3 and f.notnull() and f.isnull() \n" \
                   " or f in (4, 5) and f.str.contains('a') "

        c = st.container(border=True)
        c_q, c_f, c_k, _ = c.columns(spec=[3, 1, 1, 1])
        query = c_q.text_input("query", key=f"df:input:query:{label}",
                               help=help_str, placeholder=f"q: {help_str}")
        field = c_f.selectbox(label="field",
                              key=f"df:selectbox:field:{label}",
                              options=data.df.columns)
        kw = c_k.text_input(label="contains",
                            key=f"df:input:keywrod:{label}",
                            placeholder="keyword")
        if field and kw:
            like_query = f"{field}.notnull() and {field}.str.contains('{kw}')"
            if query:
                if query.strip().endswith("and") or query.strip().endswith("or"):
                    query += " "
                else:
                    query += " and "
            query += like_query

        query_df = None
        if not query:
            return query_df
        try:
            # logger.info("df query: %s" % query)
            c.text(f"df.query({query})")
            query_df = data.df.query(query)
        except Exception as e:
            c.warning(f"{str(e)}")
        return query_df

    def view_dataframe(self, data: DBResult):
        if not data:
            return

        desc = data.desc or data.label or data.caller
        df = data.df
        query_df = self.view_dataframe_query(data)
        if query_df is not None:
            df = query_df

        st.text(f"[ {desc} ] [ {data.dt} ] [ rows: {len(df)} ]",
                help=data.sql)
        st.dataframe(df)

    def view_http_result(self, r: HttpResult):
        if r is None:
            return
        with st.container(border=True):
            st.write("request:")
            st.code(r.curl(), wrap_lines=True)
            st.write("response:")
            st.json(r.json())

    # def select_cur_cate(self):
    #     with st.container(border=True):
    #         cate = st.selectbox(label="category", index=None,
    #                             options=yonder.get_select_cates(),
    #                             format_func=_format_select_label)
    #         if not cate:
    #             return
    #         d = dict(zip(cate._fields, map(str, list(cate))))
    #         # st.text(f"cate: {cate.id} - {cate.name}", help=str(d))
    #         st.json(d, expanded=False)
    #         st.session_state.cate = cate
