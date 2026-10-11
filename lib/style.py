"""RTL layout, right-hand sidebar and light decorative animation.

CSS is used here deliberately and only for things config.toml cannot express:
text direction, sidebar side, and a few keyframe animations the user asked for.
All colour and font choices live in .streamlit/config.toml.
"""

import streamlit as st

# model colours, reused by the charts and the badges
C_ARDL = "#1565C0"
C_PANEL = "#2E7D32"
C_CSARDL = "#EF6C00"
C_SURARDL = "#6A1B9A"

MODEL_COLORS = {
    "ARDL": C_ARDL,
    "Panel ARDL": C_PANEL,
    "CS-ARDL": C_CSARDL,
    "SUR-ARDL": C_SURARDL,
}

_CSS = """
<style>
/* ---------- اتجاه الصفحة من اليمين إلى اليسار ---------- */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"] {
    direction: rtl;
}
[data-testid="stAppViewContainer"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown {
    text-align: right;
}

/* السايدبار إلى اليمين: في تخطيط rtl يكفي أن يكون أول عنصر في DOM،
   وهو كذلك أصلًا. أي تدخّل بـ order يُعيده إلى اليسار. */

/* منع كسر أسماء النماذج عند الشرطة: SUR-ARDL لا تُقسم سطرين */
.sa-nowrap { white-space: nowrap; }

/* ---------- ما يجب أن يبقى من اليسار إلى اليمين ---------- */
/* المعادلات والرموز والشيفرة والمخططات لا تُقلب */
.katex, .katex-display,
code, pre, [data-testid="stCode"],
[data-testid="stMetricValue"],
.mermaid, [data-testid="stMermaidChart"],
.vega-embed, [data-testid="stVegaLiteChart"],
[data-testid="stDataFrame"], [data-testid="stTable"] {
    direction: ltr;
    text-align: left;
}
.katex-display { text-align: center; }

/* الجداول المكتوبة بـ Markdown تبقى عربية المحاذاة */
.stMarkdown table { direction: rtl; }
.stMarkdown table th, .stMarkdown table td { text-align: right; }

/* القوائم النقطية والرقمية */
.stMarkdown ul, .stMarkdown ol { padding-right: 1.4rem; padding-left: 0; }

/* ---------- حركة خفيفة عند ظهور المحتوى ---------- */
@keyframes sa-rise {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.sa-anim > div { animation: sa-rise 0.45s ease-out both; }
.sa-anim > div:nth-child(2) { animation-delay: 0.06s; }
.sa-anim > div:nth-child(3) { animation-delay: 0.12s; }
.sa-anim > div:nth-child(4) { animation-delay: 0.18s; }

/* نبضة هادئة لإبراز عنصر واحد */
@keyframes sa-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(106, 27, 154, 0.30); }
    50%      { box-shadow: 0 0 0 10px rgba(106, 27, 154, 0.00); }
}
.sa-pulse { animation: sa-pulse 2.4s ease-in-out infinite; border-radius: 12px; }

/* شريط تدرّج علوي يعرّف كل نموذج بلونه */
.sa-stripe {
    height: 6px; border-radius: 99px; margin: 0.2rem 0 1.1rem 0;
    background: linear-gradient(90deg, #1565C0, #2E7D32, #EF6C00, #6A1B9A);
    background-size: 300% 100%;
    animation: sa-slide 9s ease-in-out infinite;
}
@keyframes sa-slide {
    0%, 100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}
</style>
"""


def apply() -> None:
    """يُستدعى مرة واحدة في بداية التطبيق."""
    st.html(_CSS)


def stripe() -> None:
    """شريط ملوّن يفصل أقسام الصفحة."""
    st.html('<div class="sa-stripe"></div>')


def model_badge(name: str) -> str:
    """وسم ملوّن باسم النموذج، صالح للاستخدام داخل Markdown."""
    color = MODEL_COLORS.get(name, "#546E7A")
    return f":color[**{name}**]{{foreground=\"{color}\"}}"
