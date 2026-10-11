import streamlit as st

from lib import style
from lib.content import MODELS

M = MODELS["Panel ARDL"]

st.title(f"{M['icon']} Panel ARDL — PMG / MG / DFE")
st.caption(f"{M['full']} · {M['authors']}")
style.stripe()

st.info(M["why"], icon=":material/lightbulb:")

# ------------------------------------------------------------------
st.header(":material/functions: المعادلة")
st.latex(M["equation"])

st.markdown(
    """
$\\phi_i$ سرعة التعديل للوحدة $i$، و$\\theta$ متّجه المعاملات طويلة الأجل.
**السؤال كله يدور حول $\\theta$**: هل هو مشترك أم خاص بكل وحدة؟
"""
)

# ------------------------------------------------------------------
st.header(":material/call_split: المقدّرات الثلاثة")

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    with st.container(border=True):
        st.markdown("#### :material/lock: DFE")
        st.markdown(
            """
**Dynamic Fixed Effects**

كل المعاملات مجمّعة عدا الثوابت.

- أقصى كفاءة إن صحّ التجانس
- **متحيّز بشدّة** إن بطل
- يعاني تحيّز Nickell عند T صغيرة

:red-badge[الأكثر تقييدًا]
"""
        )

with c2:
    with st.container(border=True):
        st.markdown("#### :material/balance: PMG")
        st.markdown(
            """
**Pooled Mean Group**

الأجل الطويل مقيّد، القصير حر.

- وسط بين الطرفين
- كفء **إن** صحّ قيد التجانس
- **غير متّسق** إن بطل

:green-badge[الأكثر استعمالًا]
"""
        )

with c3:
    with st.container(border=True):
        st.markdown("#### :material/open_in_full: MG")
        st.markdown(
            """
**Mean Group**

انحدار منفصل لكل وحدة ثم متوسّط.

- **متّسق دائمًا**
- أقل كفاءة
- يحتاج T كبيرة لكل وحدة

:blue-badge[الأكثر مرونة]
"""
        )

st.markdown(
    """
```mermaid
flowchart TD
    A["قدّر MG و PMG"] --> B["اختبار Hausman<br/>H0: قيد التجانس صحيح"]
    B -->|"لم تُرفض"| C["PMG<br/>متّسق وأكفأ"]
    B -->|"رُفضت"| D["MG<br/>PMG غير متّسق"]
    C --> E["قارن PMG بـ DFE<br/>بنفس المنطق"]
    E -->|"لم تُرفض"| F["PMG مفضّل على DFE"]
    E -->|"رُفضت"| G["عدم تجانس<br/>ارجع إلى MG"]
    style C fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    style F fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    style D fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    style G fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
```
"""
)

st.warning(
    "منطق Hausman هنا يُقرأ بعناية: الرفض يعني أن المقدّر **المقيّد** غير متّسق، "
    "فنرجع إلى الحر. وعدم الرفض **ليس إثباتًا** للتجانس — قد يكون ضعف قوّة فقط، "
    "خصوصًا عند N صغيرة.",
    icon=":material/psychology:",
)

# ------------------------------------------------------------------
st.header(":material/checklist: الشروط والافتراضات")

t1, t2 = st.tabs(["شروط البيانات", "الافتراض الذي يُكسر غالبًا"])

with t1:
    st.markdown(
        """
| الشرط | التفصيل |
|---|---|
| N | متوسطة إلى كبيرة (10–50) |
| T | كبيرة ($\\ge 20$، ويفضّل $\\ge 30$) لأن كل وحدة تُقدَّر منفردة في MG |
| رتب التكامل | I(1) أساسًا، مع سكون حدّ تصحيح الخطأ |
| التوازن | لوحة متوازنة يفضّل |
| $\\phi_i < 0$ | لكل وحدة — وإلّا لا تكامل مشترك فيها |
| **استقلال مقطعي** | **الافتراض الحرج — انظر التبويب التالي** |
"""
    )

with t2:
    st.error(
        """
**الاستقلال المقطعي هو كعب أخيل هذه العائلة.**

PMG وMG وDFE تفترض جميعًا أن $\\mathrm{Cov}(\\varepsilon_{it}, \\varepsilon_{jt}) = 0$.
وهذا الافتراض **يُنتهك في معظم بيانات الاقتصاد الكلي الدولية**: الدول مرتبطة
بالتجارة والمال والصدمات العالمية.

وإن كان الاعتماد ناتجًا عن **عامل مشترك يدخل المتغيّرات المفسّرة**، فالمشكلة
ليست كفاءة بل **عدم اتّساق** — المقدّرات متحيّزة مهما كبرت العيّنة.
""",
        icon=":material/dangerous:",
    )
    st.markdown(
        """
**الإجراء الإلزامي:** طبّق اختبار **Pesaran CD** على بواقي النموذج.

- **لم تُرفض** H0 ⟹ يمكن الاعتماد على PMG/MG.
- **رُفضت** H0 ⟹ انتقل إلى **CS-ARDL** (إن كانت N كبيرة)
  أو **SUR-ARDL** (إن كانت N صغيرة وT أكبر بكثير).

ولا تستعمل اختبارات جذر الوحدة من الجيل الأول (LLC، IPS) عند وجود اعتماد
مقطعي — استعمل **CIPS**.
"""
    )

# ------------------------------------------------------------------
st.header(":material/bug_report: المشاكل الشائعة")

with st.expander(":material/error: عدم اختبار الاعتماد المقطعي أصلًا", expanded=True):
    st.markdown(
        """
أكثر الأخطاء شيوعًا وأخطرها. كثير من الأوراق تُقدّر PMG مباشرةً على لوحة دول
دون اختبار CD، فتبني النتيجة كلها على افتراض مُنتهَك غالبًا.

**الحل:** اختبار CD قبل التقدير وبعده، وأفصح عن النتيجة.
"""
    )

with st.expander(":material/error: قراءة عدم رفض Hausman كإثبات للتجانس"):
    st.markdown(
        """
عدم الرفض قد يعني ضعف قوّة الاختبار لا صحّة القيد — وخصوصًا عند N صغيرة
أو تباين كبير في تقديرات MG.

**الحل:** ادعم Hausman باختبار **Pesaran–Yamagata** لتجانس الميول،
وأفصح عن تشتّت معاملات MG عبر الوحدات.
"""
    )

with st.expander(":material/error: تحيّز Nickell عند T صغيرة"):
    st.markdown(
        """
DFE مع متغيّر تابع مُبطّأ وآثار ثابتة يُنتج تحيّزًا من الرتبة $O(1/T)$.
عند $T = 15$ قد يبلغ التحيّز نسبة معتبرة.

**الحل:** تجنّب DFE عند T صغيرة، أو استعمل مقدّرات GMM المخصّصة
لحالة N كبيرة وT صغيرة.
"""
    )

with st.expander(":material/error: وحدات بسرعة تعديل موجبة"):
    st.markdown(
        """
إن كان $\\phi_i > 0$ لبعض الوحدات فلا تكامل مشترك فيها، ومتوسّط MG
يصبح خليطًا بلا معنى.

**الحل:** افحص $\\phi_i$ لكل وحدة قبل المتوسّط، وأفصح عن الوحدات الشاذّة.
"""
    )

# ------------------------------------------------------------------
st.header(":material/thumbs_up_down: متى تستعمله ومتى لا")

c1, c2 = st.columns(2, gap="large")
with c1:
    st.success(
        """
**استعمله عندما**

- N بين 10 و 50، T ≥ 20
- اختبار CD **لم يرفض** الاستقلال
- لديك سبب نظري لتوقّع تجانس الأجل الطويل
- تريد رقمًا واحدًا يلخّص اللوحة
""",
        icon=":material/check_circle:",
    )
with c2:
    st.error(
        """
**لا تستعمله عندما**

- اختبار CD **رفض** الاستقلال ⟹ CS-ARDL
- N صغيرة (< 10) وT كبيرة ⟹ SUR-ARDL
- T صغيرة جدًا ⟹ تحيّز Nickell
- تريد معاملًا لكل وحدة لا متوسّطًا
""",
        icon=":material/cancel:",
    )

st.divider()
st.caption("التنفيذ في Stata: `xtpmg y x1 x2, lr(...) ec(ec) replace pmg` — وكذلك `mg` و`dfe`.")
