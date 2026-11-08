#!/usr/bin/env python3
"""Extract visual identity (theme colors, fonts, usage) from a .pptx file.

Usage: python3 extract_theme.py deck.pptx
"""
import sys
import re
import zipfile
from collections import Counter

NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"


def theme_info(z):
    names = sorted(n for n in z.namelist() if re.match(r"ppt/theme/theme\d+\.xml$", n))
    if not names:
        return
    xml = z.read(names[0]).decode("utf8", "ignore")
    print(f"== ألوان الثيم ({names[0]}) ==")
    for key in ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3",
                "accent4", "accent5", "accent6", "hlink"]:
        m = re.search(rf"<a:{key}>(.*?)</a:{key}>", xml, re.S)
        if m:
            c = re.search(r'(?:val|lastClr)="([0-9A-Fa-f]{6})"', m.group(1))
            print(f"  {key:9s} #{c.group(1).upper() if c else '?'}")
    print("== خطوط الثيم ==")
    for kind in ["majorFont", "minorFont"]:
        m = re.search(rf"<a:{kind}>(.*?)</a:{kind}>", xml, re.S)
        if m:
            latin = re.search(r'<a:latin typeface="([^"]*)"', m.group(1))
            cs = re.search(r'<a:cs typeface="([^"]*)"', m.group(1))
            arab = re.search(r'<a:font script="Arab" typeface="([^"]*)"', m.group(1))
            print(f"  {kind}: latin={latin.group(1) if latin else '-'} "
                  f"cs={cs.group(1) if cs else '-'} arab={arab.group(1) if arab else '-'}")


def usage(z):
    slides = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                    key=lambda n: int(re.search(r"(\d+)", n.split("/")[-1]).group(1)))
    fonts, colors, sizes = Counter(), Counter(), Counter()
    pics = {}
    for n in slides:
        xml = z.read(n).decode("utf8", "ignore")
        fonts.update(re.findall(r'<a:(?:latin|cs|ea) typeface="([^"+][^"]*)"', xml))
        colors.update(c.upper() for c in re.findall(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', xml))
        sizes.update(int(s) / 100 for s in re.findall(r'<a:rPr[^>]*\bsz="(\d+)"', xml))
        pics[n] = (xml.count("<p:pic>") + xml.count("<p:pic "),
                   len(re.findall(r"<a:t>([^<]*\S[^<]*)</a:t>", xml)))
    print("== الخطوط المستخدمة فعلاً ==")
    for f, c in fonts.most_common(10):
        print(f"  {f}: {c}")
    print("== الألوان المستخدمة فعلاً (srgb) ==")
    for f, c in colors.most_common(12):
        print(f"  #{f}: {c}")
    print("== أحجام الخط (نقطة) ==")
    print("  " + ", ".join(f"{s:g}pt×{c}" for s, c in sorted(sizes.items())))
    print("== صور / مقاطع نص في كل شريحة ==")
    image_only = []
    for n, (p, t) in pics.items():
        num = re.search(r"(\d+)", n.split("/")[-1]).group(1)
        flag = "  ← نصها غالباً داخل صورة" if p and t <= 1 else ""
        if flag:
            image_only.append(num)
        print(f"  ش{num}: صور={p} نصوص={t}{flag}")
    if image_only:
        print(f"تنبيه: الشرائح {', '.join(image_only)} تحتاج قراءة بصرية بعد التحويل لصور.")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with zipfile.ZipFile(sys.argv[1]) as z:
        pres = z.read("ppt/presentation.xml").decode("utf8", "ignore")
        m = re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', pres)
        if m:
            w, h = int(m.group(1)) / 914400, int(m.group(2)) / 914400
            print(f"== المقاس == {w:.2f} × {h:.2f} بوصة")
        theme_info(z)
        usage(z)


if __name__ == "__main__":
    main()
