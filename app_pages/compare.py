import pandas as pd
import streamlit as st

from lib import style
from lib.content import COMPARISON, MODELS

st.title(":material/table_chart: المقارنة الشاملة")
st.caption("عشرون بُعدًا عبر النماذج الأربعة في جدول واحد")
style.stripe()

df = pd.DataFrame(
    COMPARISON,
    columns=["المحور", "البند", "ARDL", "Panel ARDL", "CS-ARDL", "SUR-ARDL"],
)

axes = list(dict.fromkeys(df["المحور"]))
chosen = st.pills(
    "رشّح حسب المحور",
    axes,
    selection_mode="multi",
    default=axes,
    key="axes",
)

view = df[df["المحور"].isin(chosen)] if chosen else df

for axis in [a for a in axes if a in (chosen or axes)]:
    st.subheader(axis)
    block = view[view["المحور"] == axis].drop(columns=["المحور"])
    st.dataframe(
        block,
        hide_index=True,
        width="stretch",
        column_config={
            "البند": st.column_config.TextColumn("البند", width="medium"),
            "ARDL": st.column_config.TextColumn("ARDL", width="medium"),
            "Panel ARDL": st.column_config.TextColumn("Panel ARDL", width="medium"),
            "CS-ARDL": st.column_config.TextColumn("CS-ARDL", width="medium"),
            "SUR-ARDL": st.column_config.TextColumn("SUR-ARDL", width="medium"),
        },
    )

style.stripe()

# ------------------------------------------------------------------
st.header(":material/scatter_plot: خريطة (N, T) — أين يقع كل نموذج")

st.markdown(
    """
أوضح طريقة لرؤية الفروق: ارسم النماذج على مستوى عدد الوحدات مقابل طول السلسلة.
النماذج **لا تتنافس على المساحة نفسها** — كلٌّ يسكن ركنًا مختلفًا.
"""
)

st.markdown(
    """
| | **T قصيرة (< 30)** | **T متوسطة (30–50)** | **T طويلة (> 50)** |
|---|---|---|---|
| **N = 1** | ضعيف — قوّة متدنّية | :blue-badge[ARDL] | :blue-badge[ARDL] |
| **N = 3–10** | غير كافٍ لـ Σ | :violet-badge[SUR-ARDL] | :violet-badge[SUR-ARDL] |
| **N = 10–20** | :green-badge[Panel ARDL] مع تحفّظ | :green-badge[Panel ARDL] | :green-badge[Panel ARDL] أو CS-ARDL |
| **N > 20** | GMM لا ARDL | CS-DL | :orange-badge[CS-ARDL] |

ولاحظ الخانة التي لا يملؤها شيء: **N كبيرة مع T قصيرة** ليست مجال عائلة ARDL
أصلًا، بل مجال مقدّرات GMM الديناميكية (Arellano–Bond وأمثالها).
"""
)

style.stripe()

# ------------------------------------------------------------------
st.header(":material/psychology_alt: ثلاثة فروق يُخطئ فيها كثيرون")

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    with st.container(border=True):
        st.markdown("#### SUR-ARDL ≠ CS-ARDL")
        st.markdown(
            """
الاسمان متقاربان والمجالان متعاكسان:

- **SUR-ARDL** — N **صغيرة**، يستثمر الارتباط
- **CS-ARDL** — N **كبيرة**، يُزيل العوامل

وضع أحدهما مكان الآخر خطأ بنيوي لا يُصلحه أي اختبار لاحق.
"""
        )

with c2:
    with st.container(border=True):
        st.markdown("#### الكفاءة ≠ الاتّساق")
        st.markdown(
            """
- اعتماد **ضعيف** ⟹ خسارة **كفاءة** فقط، والتقديرات ما زالت صحيحة
- اعتماد **قوي** ⟹ خسارة **اتّساق**، والتقديرات خاطئة مهما كبرت العيّنة

الأول مشكلة تُحسَّن، والثاني مشكلة تُبطِل.
"""
        )

with c3:
    with st.container(border=True):
        st.markdown("#### متوسّط ≠ مُسمّى")
        st.markdown(
            """
PMG وMG وCS-ARDL تُعطيك **رقمًا واحدًا** للّوحة.

SUR-ARDL يُعطيك **N معاملًا** مع اسم كل وحدة.

إن كان سؤالك «أي الدول تتكامل؟» فالمتوسّط لا يُجيبه مهما بلغت دقّته.
"""
        )

style.stripe()

# ------------------------------------------------------------------
st.header(":material/summarize: الخلاصة في أربعة أسطر")

for name, m in MODELS.items():
    with st.container(border=True):
        st.markdown(
            f"{m['icon']} &nbsp; **:color[{name}]{{foreground=\"{m['color']}\"}}** "
            f"&nbsp;·&nbsp; :small[{m['n']} · {m['t']}]"
        )
        st.markdown(m["one_line"])
