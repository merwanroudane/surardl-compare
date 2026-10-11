"""منصّة المقارنة بين نماذج ARDL الأربعة.

ARDL · Panel ARDL (PMG/MG/DFE) · CS-ARDL · SUR-ARDL

د. مروان رودان — merwanroudane920@gmail.com
github.com/merwanroudane
"""

import streamlit as st

from lib import style

st.set_page_config(
    page_title="نماذج ARDL — دليل المقارنة والاختيار",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)

style.apply()

pages = {
    "البداية": [
        st.Page("app_pages/home.py", title="نظرة عامة", icon=":material/home:", default=True),
        st.Page("app_pages/concepts.py", title="المفاهيم الأساسية", icon=":material/school:"),
    ],
    "النماذج الأربعة": [
        st.Page("app_pages/ardl.py", title="ARDL", icon=":material/timeline:"),
        st.Page("app_pages/panel_ardl.py", title="Panel ARDL", icon=":material/grid_view:"),
        st.Page("app_pages/cs_ardl.py", title="CS-ARDL", icon=":material/hub:"),
        st.Page("app_pages/sur_ardl.py", title="SUR-ARDL", icon=":material/share:"),
    ],
    "القرار والتحقّق": [
        st.Page("app_pages/chooser.py", title="مرشد اختيار النموذج", icon=":material/alt_route:"),
        st.Page("app_pages/compare.py", title="المقارنة الشاملة", icon=":material/table_chart:"),
        st.Page("app_pages/diagnostics.py", title="الاختبارات التشخيصية", icon=":material/fact_check:"),
        st.Page("app_pages/pitfalls.py", title="الأخطاء الشائعة", icon=":material/warning:"),
    ],
}

with st.sidebar:
    st.markdown("### :material/analytics: نماذج ARDL")
    st.caption("دليل المقارنة والاختيار بين أربعة نماذج")
    st.divider()

nav = st.navigation(pages, position="sidebar")

with st.sidebar:
    st.divider()
    st.caption(
        "إعداد: **د. مروان رودان**  \n"
        "[github.com/merwanroudane](https://github.com/merwanroudane)"
    )

nav.run()
