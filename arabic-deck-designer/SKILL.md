---
name: arabic-deck-designer
description: Design or redesign Arabic right-to-left presentation slides (pptx or slide artifacts). Use when choosing a visual layout per slide, applying an existing deck's identity, handling RTL text with numbers and English terms, or setting typography and hierarchy.
---

# مصمم العروض العربية

مهارة لاختيار الشكل البصري المناسب لكل رسالة، وتطبيقه على عرض عربي من اليمين لليسار بهوية متسقة.

## القواعد الحاكمة

1. **الرسالة أولاً ثم الشكل.** لا يُصمم شيء قبل أن تكون رسالة الشريحة مكتوبة (مهارة deck-content-writer).
2. **الهوية من الملف نفسه.** إن لم يزوّد المستخدم دليل هوية، استخرجها من العرض الأصلي (`scripts/extract_theme.py`). لا تفترض ألواناً أو شعارات رسمية.
3. **أي اتجاه بصري جديد يُعلَّم "مقترح"** ولا يُقدَّم كهوية معتمدة.
4. **الازدحام يُحل بالتحرير أو التقسيم، لا بتصغير الخط.**
5. **إن لم تتوفر أداة تصميم**، قدّم تصوراً بصرياً قابلاً للتنفيذ ولا تصفه بأنه تصميم منجز.

## سير العمل

1. **استخرج الهوية**: `python3 scripts/extract_theme.py deck.pptx` ← ألوان الثيم، الخطوط، مقاس الشريحة، الخطوط المستخدمة فعلاً.
2. **حوّل الشرائح إلى صور** وافحص الأسلوب القائم (انظر deck-quality-review).
3. **اختر الشكل لكل شريحة** وفق `references/visual-formats.md`.
4. **طبّق قواعد الاتجاه** وفق `references/rtl-layout.md`.
5. **اضبط التسلسل البصري** وفق `references/typography-hierarchy.md`.
6. **للأرقام والرسوم البيانية** استخدم مهارة dataviz مع قواعد الأرقام في `visual-formats.md`.
7. **افحص الناتج** بمهارة deck-quality-review.

## عند التعديل على ملف pptx قائم

- استخدم مهارة pptx للقراءة والتعديل.
- حافظ على القوالب الرئيسية (Masters/Layouts) والثيم الأصلي.
- النص المدمج في صور لا يُعدّل بالكتابة فوقه. استبدله بمربع نص حقيقي قابل للتعديل بنفس الموضع والخط، أو سجّله في الملاحظات إن تعذّر.
- عيّن اتجاه الفقرة RTL ومحاذاتها لليمين لكل مربع نص عربي (`a:pPr rtl="1" algn="r"`).

## الملفات المرجعية

| الملف | متى تقرأه |
|---|---|
| `references/visual-formats.md` | عند اختيار شكل أي شريحة |
| `references/rtl-layout.md` | عند وضع أي نص عربي، خاصة مع أرقام أو إنجليزي |
| `references/typography-hierarchy.md` | عند ضبط الخطوط والأحجام والمسافات |
| `references/brand-extraction.md` | عند بدء العمل على عرض قائم |
