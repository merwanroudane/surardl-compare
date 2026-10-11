import streamlit as st

from lib import style
from lib.content import MODELS, TESTS_POST, TESTS_PRE

st.title(":material/fact_check: الاختبارات التشخيصية")
st.caption("ما يُختبر، وفرضية العدم، وماذا تفعل عند الرفض")
style.stripe()

st.markdown(
    """
الاختبارات هنا ليست طقسًا. كل واحد منها يحرس **افتراضًا بعينه**، وسقوطه
يُغيّر ما يحقّ لك أن تستنتجه. ولذا يُذكر مع كل اختبار **ماذا تفعل** لا نتيجته فقط.
"""
)

model_filter = st.segmented_control(
    "رشّح حسب النموذج",
    ["الكل", *MODELS.keys()],
    default="الكل",
    key="tf",
)


def _show(tests: list[dict]) -> None:
    shown = 0
    for test in tests:
        if model_filter not in ("الكل", None) and model_filter not in test["models"]:
            continue
        shown += 1
        badges = " ".join(
            f":color[{m}]{{foreground=\"{MODELS[m]['color']}\"}}" for m in test["models"]
        )
        with st.expander(f"**{test['name']}** — {test['purpose']}"):
            st.markdown(f"**يخصّ:** {badges}")
            st.markdown(f"**فرضية العدم $H_0$:** {test['h0']}")
            st.markdown(test["note"])
            st.caption(f":material/menu_book: {test['ref']}")
    if shown == 0:
        st.info("لا اختبارات في هذا القسم للنموذج المختار.", icon=":material/info:")


st.header(":material/looks_one: قبل التقدير")
st.markdown(
    "هذه الاختبارات تُقرّر **أي نموذج تستعمل أصلًا**. "
    "تشغيلها بعد اختيار النموذج يقلب ترتيب القرار."
)
_show(TESTS_PRE)

style.stripe()

st.header(":material/looks_two: بعد التقدير")
st.markdown(
    "هذه تُقرّر **هل تثق بما قدّرت**. فشل أيٍّ منها لا يعني بالضرورة "
    "تغيير النموذج، لكنه يعني تعديل التوصيف أو تقييد ما تستنتجه."
)
_show(TESTS_POST)

style.stripe()

# ------------------------------------------------------------------
st.header(":material/emergency: ماذا تفعل عند الفشل — جدول سريع")

st.markdown(
    """
| الاختبار الفاشل | ما يعنيه | الإجراء |
|---|---|---|
| **ADF على الفروق لا يرفض** | المتغيّر قد يكون I(2) | استبعده أو فرّقه مجددًا — ARDL يصبح باطلًا |
| **Breusch–Godfrey يرفض** | ارتباط ذاتي متبقٍّ | **زِد رتب الإبطاء** حتى تبيضّ البواقي. في SUR-ARDL هذا شرط صحّة Σ |
| **Breusch–Pagan لا يرفض** | Σ قطرية | لا مكسب من SUR — اكتفِ بـ ARDL لكل وحدة |
| **CD يرفض بعد CS-ARDL** | العوامل لم تُلتقط | زِد $p_T$، أو راجع التوصيف، أو فكّر في عوامل إضافية |
| **Hausman يرفض (PMG/MG)** | قيد التجانس باطل | انتقل إلى **MG** — PMG غير متّسق |
| **F بين الحدّين** | غير حاسم | ارجع لرتب التكامل، أو استعمل قيمًا حرجة أدقّ لـ T |
| **λ موجب أو غير معنوي** | لا تصحيح خطأ | **لا تُفسّر الأجل الطويل** — المقام صفر إحصائيًا |
| **CUSUMSQ يخرج عن الحدود** | انكسار بنيوي | اختبر الانكسار، وفكّر في Fourier ARDL أو متغيّر صوري |
| **RESET يرفض** | شكل دالي خاطئ | تحويل لوغاريتمي، أو NARDL للّاخطّية |
| **Jarque–Bera يرفض** | بواقي غير طبيعية | في SUR-ARDL: استعمل CD بدل BP، أو bootstrap للقيم الحرجة |
| **ARCH يرفض** | تغاير شرطي | أخطاء معيارية حصينة — الاتّساق سليم |
"""
)

st.warning(
    "لاحظ التمييز الجوهري في هذا الجدول: بعض الفشل **يُبطل النموذج** "
    "(I(2)، λ موجب)، وبعضه **يُعدّل التوصيف** (BG، RESET)، وبعضه "
    "**يُصحَّح بالأخطاء المعيارية فقط** (ARCH). الخلط بينها يؤدّي إمّا إلى "
    "هجر نموذج سليم أو إلى نشر نتيجة باطلة.",
    icon=":material/priority_high:",
)

style.stripe()

# ------------------------------------------------------------------
st.header(":material/timeline: ترتيب التشغيل")

st.markdown(
    """
```mermaid
flowchart TD
    A["جذر الوحدة<br/>ADF · PP · KPSS · CIPS"] --> B{"أي I(2)؟"}
    B -->|"نعم"| X["توقّف"]
    B -->|"لا"| C["اعتماد مقطعي<br/>BP LM · Pesaran CD"]
    C --> D["اختيار النموذج"]
    D --> E["اختيار رتب الإبطاء<br/>AIC · SBC"]
    E --> F["التقدير"]
    F --> G["ارتباط ذاتي<br/>Breusch-Godfrey"]
    G -->|"رُفض"| E
    G -->|"سليم"| H["اختبار التكامل المشترك<br/>الحدود F و t"]
    H --> I["تشخيص البواقي<br/>ARCH · JB · RESET"]
    I --> J["الاستقرار<br/>CUSUM · CUSUMSQ"]
    J --> K["اختبارات خاصة بالنموذج<br/>Hausman أو Wald عبر المعادلات"]
    style X fill:#FFEBEE,stroke:#C62828,color:#B71C1C
    style D fill:#EDE7F6,stroke:#6A1B9A,stroke-width:2px,color:#4A148C
    style G fill:#FFF8E1,stroke:#F9A825,color:#F57F17
```

لاحظ **الحلقة الراجعة** من Breusch–Godfrey إلى اختيار رتب الإبطاء:
هذه ليست خطوة تمرّ مرّة واحدة. تُكرّر حتى تبيضّ البواقي، **ثم** تُكمل.
"""
)
