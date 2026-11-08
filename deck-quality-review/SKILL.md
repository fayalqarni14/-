---
name: deck-quality-review
description: Quality-check an Arabic presentation before delivery. Use after writing or designing slides to render every slide to an image, catch RTL, overflow and consistency defects, score the deck against the editorial checklist, and produce a change log.
---

# مراجعة جودة العروض

مهارة الفحص الأخير قبل التسليم. لا يُسلَّم عرض قبل المرور بها.

## القاعدة الحاكمة

**لا يُحكم على شريحة من نصها فقط.** كل شريحة تُحوّل إلى صورة وتُفحص بالنظر. العيوب الحقيقية (خروج النص، انقلاب الأرقام، التداخل) لا تظهر إلا بصرياً.

## سير العمل

1. **حوّل الشرائح لصور:**
   ```bash
   bash scripts/render_slides.sh deck.pptx out_dir
   ```
   ينتج `out_dir/slide-01.png` ... ويطبع تنبيهاً إن كانت الخطوط المستخدمة غير متوفرة.
2. **افحص كل صورة** وفق `references/render-qa.md` وسجّل العيوب برقم الشريحة.
3. **صحّح العيوب** ثم أعد التحويل والفحص. كرر حتى لا يبقى عيب جوهري.
4. **قيّم العرض كاملاً** وفق `references/final-checklist.md`.
5. **اكتب سجل التغييرات** وفق `references/change-log.md`.
6. سلّم: الملف + سطر عن النتيجة + "عناصر تحتاج تأكيد" إن وجدت.

## للمراجعات عالية الأهمية

اطلب مراجعة من وكيل مستقل لم يشارك في الكتابة، يُعطى المصدر والعرض الجديد وقائمة final-checklist.md فقط، حتى لا يقيّم العمل نفسه.

## الملفات المرجعية

| الملف | متى تقرأه |
|---|---|
| `references/render-qa.md` | عند فحص صور الشرائح |
| `references/final-checklist.md` | قبل التسليم |
| `references/change-log.md` | عند كتابة الملاحظات وسجل التغييرات |
