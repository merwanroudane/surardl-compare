import streamlit as st

from lib import style
from lib.content import MODELS

st.title(":material/alt_route: مرشد اختيار النموذج")
st.caption("أجب عن بياناتك، واحصل على توصية مُعلَّلة — لا على رقم")
style.stripe()

st.markdown(
    """
هذا المرشد **لا يُقرّر عنك**. هو يُطبّق الشجرة المنطقية الموضّحة في صفحة
النظرة العامة، ويشرح لك لماذا وصل إلى ما وصل إليه، وما الذي يُغيّر الإجابة.
"""
)

with st.form("chooser"):
    st.subheader(":material/database: ١. بنية البيانات")
    c1, c2 = st.columns(2)
    with c1:
        n = st.number_input(
            "عدد الوحدات المقطعية N",
            min_value=1, max_value=500, value=6, step=1,
            help="عدد الدول أو الشركات أو الأقاليم. اكتب 1 لسلسلة زمنية واحدة.",
        )
    with c2:
        t = st.number_input(
            "طول السلسلة الزمنية T",
            min_value=5, max_value=2000, value=35, step=1,
            help="عدد الفترات لكل وحدة.",
        )

    balanced = st.checkbox("اللوحة متوازنة وبلا فجوات زمنية", value=True)

    st.divider()
    st.subheader(":material/link: ٢. الاعتماد المقطعي")
    cd = st.radio(
        "ماذا تقول اختبارات الاعتماد المقطعي (CD أو Breusch–Pagan)؟",
        [
            "لم أختبره بعد",
            "لم تُرفض فرضية الاستقلال",
            "رُفضت — لكن يبدو ارتباط أخطاء فقط",
            "رُفضت بقوّة — وأشتبه في عامل مشترك",
        ],
        index=0,
    )

    st.divider()
    st.subheader(":material/tune: ٣. ما تريده من النتيجة")
    want = st.radio(
        "أي صيغة نتيجة تخدم سؤالك البحثي؟",
        [
            "معامل مُسمّى لكل وحدة على حدة",
            "رقم واحد يلخّص اللوحة كلها",
            "لا يهمّ — أريد الأدقّ إحصائيًا",
        ],
        index=0,
    )
    cross_tests = st.checkbox(
        "أحتاج اختبارًا رسميًا لتساوي المعاملات بين وحدات بعينها",
        value=False,
        help="مثل: هل سرعة التعديل في إندونيسيا تساوي نظيرتها في ماليزيا؟",
    )

    st.divider()
    st.subheader(":material/warning: ٤. فحوص أوّلية")
    has_i2 = st.checkbox("يوجد متغيّر واحد على الأقل من رتبة I(2)", value=False)

    submitted = st.form_submit_button(
        "احسب التوصية", type="primary", width="stretch"
    )

if not submitted:
    st.info("املأ الحقول أعلاه ثم اضغط «احسب التوصية».", icon=":material/arrow_upward:")
    st.stop()

style.stripe()

# ----------------------------------------------------------------------
# منطق القرار
# ----------------------------------------------------------------------
if has_i2:
    st.error(
        "### :material/block: توقّف — لا يصلح أي من النماذج الأربعة\n\n"
        "وجود متغيّر **I(2)** يُبطل نظرية اختبار الحدود: إحصاءة F لا تعود محصورة "
        "بين الحدّين المجدولين، فيصبح الاستدلال بلا أساس.\n\n"
        "**ما تفعله:** إمّا أن تُفرّق المتغيّر مرّة إضافية وتُعيد تعريف السؤال، "
        "أو تستبعده، أو تنتقل إلى إطار يقبل I(2) مثل Johansen الموسّع. "
        "وتأكّد أولًا أن التصنيف صحيح — فاختبارات جذر الوحدة ضعيفة القوّة.",
        icon=":material/dangerous:",
    )
    st.stop()

ratio = t / n if n else 0
reasons: list[str] = []
warnings_: list[str] = []
pick = None

if n == 1:
    pick = "ARDL"
    reasons.append("لديك سلسلة زمنية واحدة (N = 1)، وهذا مجال ARDL أحادي المعادلة حصرًا.")
    if t < 30:
        warnings_.append(
            f"T = {t} قصيرة. استعمل قيم Narayan (2005) الحرجة أو سطوح Kripfganz–Schneider، "
            "ولا تستعمل قيم PSS (2001) المقاربية."
        )

elif cd == "لم أختبره بعد":
    pick = None
    st.warning(
        "### :material/help: لا يمكن الحسم قبل اختبار الاعتماد المقطعي\n\n"
        "هذا هو **المفترق الأهم** في الشجرة كلها، ولا يمكن تخمينه من N و T.\n\n"
        f"ببنيتك الحالية (N = {n}، T = {t}) ابدأ بالاختبار المناسب:\n\n"
        + (
            "- **Breusch–Pagan LM** — هو الأنسب عند N صغيرة و T كبيرة.\n"
            if n <= 10
            else "- **Pesaran CD** — هو الأنسب عند N كبيرة.\n"
        )
        + "\nثم عُد إلى هذه الصفحة بالنتيجة.",
        icon=":material/science:",
    )

elif cd == "لم تُرفض فرضية الاستقلال":
    if n <= 10 and ratio >= 3:
        pick = "ARDL"
        reasons.append(
            "الاستقلال المقطعي لم يُرفض، وΣ قطرية عمليًا. ونتيجة Zellner تقول إن "
            "SUR عندها **مطابق عدديًا** لـ OLS معادلةً معادلة — فلا مكسب من النظام."
        )
        reasons.append("قدّر ARDL لكل وحدة على حدة؛ أبسط وأوضح وبنفس النتيجة.")
    else:
        pick = "Panel ARDL"
        reasons.append(
            "الاستقلال المقطعي لم يُرفض، فافتراض PMG/MG الأساسي قائم."
        )
        reasons.append(
            "القرار التالي داخل العائلة: قدّر **MG** و**PMG** ثم طبّق **Hausman**. "
            "عدم الرفض ⟹ PMG (الأكفأ)؛ الرفض ⟹ MG."
        )

elif cd == "رُفضت — لكن يبدو ارتباط أخطاء فقط":
    if n <= 10 and ratio >= 3:
        pick = "SUR-ARDL"
        reasons.append(
            f"N = {n} صغيرة و T = {t} أكبر بكثير (T/N ≈ {ratio:.1f})، "
            "وهذه بنية SUR-ARDL بالضبط."
        )
        reasons.append(
            "الاعتماد ارتباط أخطاء معاصر لا عامل مشترك، فالاتّساق محفوظ "
            "والمفقود هو الكفاءة — وهذا ما يستردّه وزن Σ."
        )
        reasons.append(
            "ويبقى لك ميزة لا تتاح لغيره: كل وحدة بمعاملها، مع اختبارات رسمية "
            "لتساوي المعاملات عبر الوحدات."
        )
    elif n > 10:
        pick = "CS-ARDL"
        reasons.append(
            f"N = {n} كبيرة على SUR-ARDL: تقدير Σ يحتاج {n*(n+1)//2} معلمة "
            f"من {t} مشاهدة فقط، فتصبح شبه شاذّة."
        )
        warnings_.append(
            "إن كان الاعتماد فعلًا ارتباط أخطاء لا عاملًا مشتركًا، فـ CS-ARDL "
            "يحلّ مشكلة غير موجودة ويُهدر درجات حرّية. راجع تشخيصك."
        )
    else:
        pick = "SUR-ARDL"
        warnings_.append(
            f"T/N ≈ {ratio:.1f} منخفضة. SUR-ARDL يحتاج T ≫ N؛ تحقّق من استقرار "
            "Σ المقدَّرة قبل الاعتماد على النتائج."
        )
        reasons.append("البنية تميل إلى SUR-ARDL لكنها على الحافّة.")

else:  # رُفضت بقوّة — عامل مشترك
    if n >= 15:
        pick = "CS-ARDL"
        reasons.append(
            "عامل مشترك يدخل المنحدرات يجعل PMG/MG **غير متّسقين** — "
            "المشكلة متغيّر محذوف لا مجرّد كفاءة."
        )
        reasons.append(
            f"N = {n} كافية لتكون المتوسّطات المقطعية وكيلًا موثوقًا عن العوامل."
        )
        reasons.append(f"ابدأ بـ pT ≈ T^(1/3) ≈ {max(1, round(t ** (1/3)))} إبطاءات للمتوسّطات.")
        if t < 50:
            warnings_.append(
                f"T = {t} أقل من 50. جرّب **CS-DL** وقارن — فهي تتفوّق على CS-ARDL "
                "عند T المتوسطة."
            )
    else:
        pick = "SUR-ARDL"
        reasons.append(
            f"N = {n} صغيرة جدًا على CS-ARDL: متوسّط {n} وحدات ليس وكيلًا موثوقًا "
            "عن عامل مشترك — بل ضجيج."
        )
        reasons.append(
            "SUR-ARDL لا يحاول إزالة الاعتماد بل يُنمذجه في Σ، وهو الخيار العملي "
            "الوحيد في هذا الركن من فضاء (N, T)."
        )
        warnings_.append(
            "تحفّظ أمين: إن كان العامل المشترك مرتبطًا فعلًا بالمنحدرات، فـ SUR-ARDL "
            "يُحسّن الكفاءة لكنه **لا يُزيل تحيّز المتغيّر المحذوف**. أفصح عن ذلك."
        )

# ----------------------------------------------------------------------
# عرض التوصية
# ----------------------------------------------------------------------
if pick:
    m = MODELS[pick]
    st.markdown(
        f"## :material/recommend: التوصية — "
        f":color[{pick}]{{foreground=\"{m['color']}\"}}"
    )
    st.html('<div class="sa-pulse">')
    with st.container(border=True):
        st.markdown(f"**{m['full']}** · {m['authors']}")
        st.markdown(m["one_line"])
    st.html("</div>")

    st.subheader(":material/psychology: لماذا")
    for r in reasons:
        st.markdown(f"- {r}")

    if warnings_:
        st.subheader(":material/warning: تحفّظات")
        for w in warnings_:
            st.warning(w, icon=":material/priority_high:")

    if not balanced and pick == "SUR-ARDL":
        st.error(
            "لوحتك غير متوازنة، و**SUR يتطلّب عيّنة مشتركة** لكل المعادلات. "
            "وازن اللوحة أو قلّص المدى الزمني إلى الفترة المشتركة قبل التقدير.",
            icon=":material/dangerous:",
        )

    if cross_tests and pick != "SUR-ARDL":
        st.info(
            "طلبتَ اختبارًا رسميًا لتساوي المعاملات بين وحدات بعينها — وهذا "
            "**لا يتوفّر إلا في SUR-ARDL**. إن كان هذا جوهر سؤالك البحثي، "
            "فأعد النظر في بنية العيّنة لتناسبه (N أصغر، T أطول).",
            icon=":material/compare:",
        )

    if want == "معامل مُسمّى لكل وحدة" and pick == "Panel ARDL":
        st.info(
            "PMG تُنتج معاملًا طويل الأجل **واحدًا** مشتركًا. إن كنت تريد معاملًا "
            "لكل وحدة فاستعمل **MG** داخل العائلة نفسها، أو SUR-ARDL إن سمحت البنية.",
            icon=":material/fingerprint:",
        )

    st.divider()
    st.subheader(":material/checklist: خطواتك التالية")
    st.markdown(
        f"""
1. افتح صفحة **{pick}** لمراجعة الافتراضات وخطوات التطبيق.
2. راجع **الاختبارات التشخيصية** وطبّق ما يخصّ هذا النموذج.
3. اقرأ **الأخطاء الشائعة** قبل كتابة النتائج.
"""
    )
