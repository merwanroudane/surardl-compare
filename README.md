# منصّة المقارنة بين نماذج ARDL الأربعة

**ARDL · Panel ARDL (PMG/MG/DFE) · CS-ARDL · SUR-ARDL**

منصّة تعليمية تفاعلية بالعربية تشرح النماذج الأربعة وتُرشد إلى اختيار الأنسب
منها حسب بنية بياناتك ونتائج اختباراتك التشخيصية.

> An interactive Arabic-language guide to choosing between four cointegration
> frameworks: single-equation ARDL bounds testing, panel ARDL (PMG/MG/DFE),
> cross-sectionally augmented ARDL, and seemingly unrelated regression ARDL.

إعداد: **د. مروان رودان** · [github.com/merwanroudane](https://github.com/merwanroudane)

---

## الفكرة

النماذج الأربعة ليست بدائل تنافسية بل عائلة واحدة تتفرّع من معادلة تصحيح خطأ
واحدة. والفرق بينها يُختزل في ثلاثة أسئلة عن بياناتك:

1. كم عدد الوحدات المقطعية **N** مقابل طول السلسلة **T**؟
2. هل هناك **اعتماد مقطعي**، وما مصدره؟
3. هل تقبل فرض **تجانس** المعاملات عبر الوحدات؟

وكل ما تبقّى — شروط البيانات، الاختبارات، المشاكل — يتفرّع من الإجابات الثلاث.

| النموذج | N | T | الفكرة المميّزة |
|---|---|---|---|
| **ARDL** | 1 | ≥ 30 | اختبار الحدود يقبل خليط I(0) و I(1) |
| **Panel ARDL** | 10–50 | ≥ 20 | تجانس الأجل الطويل مقابل حرّية القصير |
| **CS-ARDL** | ≥ 20 | ≥ 50 | **يُزيل** العوامل المشتركة بالمتوسّطات المقطعية |
| **SUR-ARDL** | 3–10 | ≫ N | **يستثمر** الارتباط المعاصر في Σ مصدرًا للكفاءة |

لاحظ التقابل بين الأخيرين: الاسمان متقاربان والمجالان متعاكسان تمامًا.

## المحتوى

- **نظرة عامة** — شجرة القرار في مخطّط واحد، والفروق الثلاثة الجوهرية
- **المفاهيم الأساسية** — رتبة التكامل، التكامل المشترك، تصحيح الخطأ،
  الاعتماد المقطعي (الضعيف مقابل القوي)، التجانس
- **صفحة لكل نموذج** — المعادلة، الافتراضات، شروط البيانات، خطوات التطبيق،
  المشاكل الشائعة، ومتى تستعمله ومتى لا
- **مرشد اختيار النموذج** — أسئلة عن بياناتك ثم توصية **مُعلَّلة** مع تحفّظاتها
- **المقارنة الشاملة** — عشرون بُعدًا عبر النماذج الأربعة
- **الاختبارات التشخيصية** — كتالوج ما قبل التقدير وما بعده، مع جدول
  «ماذا تفعل عند الفشل»
- **الأخطاء الشائعة** — مصنّفة حسب الخطورة: ما يُبطل النتيجة، وما يُحرّف
  الاستدلال، وما يُضعف العمل

## التشغيل

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

الواجهة من اليمين إلى اليسار مع شريط جانبي يمينيّ، بألوان فاتحة متنوّعة،
ومخطّطات Mermaid ومعادلات LaTeX.

## ملاحظة على النطاق

المنصّة **تشرح وتوجّه ولا تُقدّر**. للتقدير الفعلي:

| النموذج | الأمر في Stata |
|---|---|
| ARDL | `ardl` (Kripfganz & Schneider) |
| Panel ARDL | `xtpmg` |
| CS-ARDL | `xtdcce2 ..., ardl` |
| SUR-ARDL | `sureg` على معادلات ECM |
| جذر الوحدة في نظام SUR | [`suradf`](https://github.com/merwanroudane) |

## المراجع

- Pesaran, M. H., Shin, Y. & Smith, R. J. (2001). Bounds testing approaches to
  the analysis of level relationships. *Journal of Applied Econometrics* 16(3),
  289–326. [doi:10.1002/jae.616](https://doi.org/10.1002/jae.616)
- Pesaran, M. H., Shin, Y. & Smith, R. P. (1999). Pooled mean group estimation
  of dynamic heterogeneous panels. *JASA* 94(446), 621–634.
- Chudik, A. & Pesaran, M. H. (2015). Common correlated effects estimation of
  heterogeneous dynamic panel data models with weakly exogenous regressors.
  *Journal of Econometrics* 188(2), 393–420.
- Arif, M. A. & Furuoka, F. (2026). Seemingly unrelated cointegrating
  regressions with autoregressive distributed lag dynamics.
  [doi:10.21203/rs.3.rs-9237078/v1](https://doi.org/10.21203/rs.3.rs-9237078/v1)
- Narayan, P. K. (2005). The saving and investment nexus for China: evidence
  from cointegration tests. *Applied Economics* 37(17), 1979–1990.
- Kripfganz, S. & Schneider, D. C. (2020). Response surface regressions for
  critical value bounds and approximate p-values in equilibrium correction
  models. *Oxford Bulletin of Economics and Statistics* 82(6), 1456–1481.
  [doi:10.1111/obes.12377](https://doi.org/10.1111/obes.12377)
- Breuer, J. B., McNown, R. & Wallace, M. (2002). Series-specific unit root
  tests with panel data. *OBES* 64(5), 527–546.
  [doi:10.1111/1468-0084.00276](https://doi.org/10.1111/1468-0084.00276)
- Pesaran, M. H. (2004/2015). General diagnostic tests for cross-sectional
  dependence in panels.
- Pesaran, M. H. & Yamagata, T. (2008). Testing slope homogeneity in large
  panels. *Journal of Econometrics* 142(1), 50–93.

## الرخصة

MIT
