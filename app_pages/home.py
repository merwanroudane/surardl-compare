import streamlit as st

from lib import style
from lib.content import MODELS

st.title(":material/analytics: نماذج ARDL الأربعة")
st.subheader("متى تستعمل كلًّا منها، ولماذا")
style.stripe()

st.markdown(
    """
النماذج الأربعة في هذه المنصّة **ليست بدائل تنافسية**، بل عائلة واحدة تتفرّع من
معادلة واحدة. الفرق بينها يُختزل في ثلاثة أسئلة فقط عن بياناتك:

1. كم عدد الوحدات المقطعية **N** مقابل طول السلسلة **T**؟
2. هل هناك **اعتماد مقطعي** بين الوحدات، وما قوّته؟
3. هل تقبل فرض **تجانس** المعاملات عبر الوحدات، أم تريدها حرّة؟

كل ما تبقّى — شروط البيانات، الاختبارات، المشاكل — يتفرّع من إجاباتك الثلاث.
"""
)

st.html('<div class="sa-anim">')
cols = st.columns(4, gap="medium")
for col, (name, m) in zip(cols, MODELS.items()):
    with col:
        with st.container(border=True):
            st.markdown(f"{m['icon']} &nbsp; **:color[{name}]{{foreground=\"{m['color']}\"}}**")
            st.caption(m["authors"])
            st.markdown(f"**{m['dim']}**")
            st.markdown(f":small[{m['n']}]")
            st.markdown(f":small[{m['t']}]")
            st.divider()
            st.markdown(m["one_line"])
st.html("</div>")

style.stripe()

st.header(":material/account_tree: شجرة القرار في صورة واحدة")

st.markdown(
    """
```mermaid
flowchart TD
    A["بياناتك"] --> B{"عدد الوحدات N"}

    B -->|"N = 1<br/>سلسلة واحدة"| C["ARDL<br/>Pesaran-Shin-Smith 2001"]

    B -->|"N صغيرة 3-10<br/>و T أكبر بكثير"| D{"اختبار Breusch-Pagan LM<br/>هل Σ غير قطرية؟"}
    D -->|"نعم - ارتباط معاصر"| E["SUR-ARDL<br/>Arif-Furuoka 2026"]
    D -->|"لا"| C2["ARDL لكل وحدة<br/>على حدة"]

    B -->|"N كبيرة 20+<br/>و T كبيرة"| F{"اختبار Pesaran CD<br/>هل يوجد اعتماد مقطعي؟"}
    F -->|"نعم - عامل مشترك"| G["CS-ARDL<br/>Chudik-Pesaran 2015"]
    F -->|"لا"| H{"اختبار Hausman<br/>هل الأجل الطويل متجانس؟"}
    H -->|"نعم"| I["PMG<br/>Panel ARDL"]
    H -->|"لا"| J["MG<br/>Panel ARDL"]

    style C fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    style C2 fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    style I fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    style J fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    style G fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px,color:#E65100
    style E fill:#F3E5F5,stroke:#6A1B9A,stroke-width:3px,color:#4A148C
```
"""
)

st.info(
    "لاحظ أن القرار الأول ليس إحصائيًا بل **بنيويًا**: نسبة N إلى T. "
    "الاختبارات الإحصائية تأتي بعده، لا قبله.",
    icon=":material/lightbulb:",
)

style.stripe()

st.header(":material/compare_arrows: الفروق الثلاثة الجوهرية")

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    with st.container(border=True):
        st.markdown("#### :material/straighten: ١. بُعد البيانات")
        st.markdown(
            """
| النموذج | N | T |
|---|---|---|
| ARDL | 1 | ≥ 30 |
| SUR-ARDL | 3–10 | ≫ N |
| Panel ARDL | 10–50 | ≥ 20 |
| CS-ARDL | ≥ 20 | ≥ 50 |

`SUR-ARDL` و`CS-ARDL` على طرفَي نقيض في N رغم تشابه اسميهما.
"""
        )

with c2:
    with st.container(border=True):
        st.markdown("#### :material/link: ٢. الاعتماد المقطعي")
        st.markdown(
            """
- **ARDL** — لا ينطبق (وحدة واحدة)
- **Panel ARDL** — يتجاهله؛ وجوده يُبطل الاتّساق
- **CS-ARDL** — يُزيله بالمتوسّطات المقطعية
- **SUR-ARDL** — **يستثمره** مصدرًا للكفاءة

الفرق الأخير دقيق ومهم: CS-ARDL يعتبره **مشكلة تُعالَج**،
وSUR-ARDL يعتبره **معلومة تُستغَل**.
"""
        )

with c3:
    with st.container(border=True):
        st.markdown("#### :material/balance: ٣. التجانس")
        st.markdown(
            """
- **PMG** — الأجل الطويل مقيّد بالتساوي
- **MG / CS-ARDL** — حر، ثم متوسّط
- **DFE** — كل شيء مجمّع
- **SUR-ARDL** — حر تمامًا، **بلا متوسّط**

SUR-ARDL وحده يُبقي كل وحدة بمعاملاتها ويُقدّم في الوقت نفسه
اختبارات رسمية لتساوي المعاملات عبر الوحدات.
"""
        )

style.stripe()

st.header(":material/route: كيف تستعمل هذه المنصّة")

st.markdown(
    """
1. إن لم تكن متأكّدًا من المفاهيم (التكامل المشترك، تصحيح الخطأ، رتب التكامل)،
   ابدأ من **المفاهيم الأساسية**.
2. إن كنت تعرف بياناتك وتريد قرارًا، اذهب مباشرةً إلى
   **:material/alt_route: مرشد اختيار النموذج** — بضعة أسئلة ثم توصية مُعلَّلة.
3. صفحة كل نموذج تشرح معادلته وافتراضاته وشروطه واختباراته ومشاكله.
4. **المقارنة الشاملة** تضع العشرين بُعدًا في جدول واحد.
5. **الاختبارات التشخيصية** كتالوج كامل: ما يُختبر، وفرضية العدم، وماذا تفعل عند الرفض.
"""
)

st.warning(
    "هذه المنصّة **تشرح وتوجّه ولا تُقدّر**. للتقدير الفعلي: "
    "`ardl` و`xtpmg` و`xtdcce2` و`surardl` في Stata.",
    icon=":material/info:",
)
