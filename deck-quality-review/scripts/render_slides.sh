#!/usr/bin/env bash
# Render every slide of a .pptx to PNG for visual QA.
# Usage: bash render_slides.sh deck.pptx out_dir [dpi]
set -euo pipefail

deck="${1:?usage: render_slides.sh deck.pptx out_dir [dpi]}"
out="${2:?usage: render_slides.sh deck.pptx out_dir [dpi]}"
dpi="${3:-80}"
mkdir -p "$out"

# Warn about fonts used in the deck that are not installed here.
missing=$(python3 - "$deck" <<'PY'
import re, sys, zipfile, subprocess
z = zipfile.ZipFile(sys.argv[1])
used = set()
for n in z.namelist():
    xml = z.read(n).decode("utf8", "ignore") if n.endswith(".xml") else ""
    if re.match(r"ppt/slides/slide\d+\.xml$", n):
        used |= set(re.findall(r'<a:(?:latin|cs|ea) typeface="([^"+][^"]*)"', xml))
    elif re.match(r"ppt/theme/theme\d+\.xml$", n):
        for kind in ("majorFont", "minorFont"):
            m = re.search(rf"<a:{kind}>(.*?)</a:{kind}>", xml, re.S)
            if m:
                used |= set(re.findall(r'<a:(?:latin|cs) typeface="([^"+][^"]*)"', m.group(1)))
have = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout.lower()
print("\n".join(sorted(f for f in used if f and f.lower() not in have)))
PY
)
if [ -n "$missing" ]; then
  echo "تنبيه: خطوط غير متوفرة، المعاينة بخط بديل والقياسات تقريبية:"
  echo "$missing" | sed 's/^/  - /'
fi

tmp=$(mktemp -d)
soffice --headless --convert-to pdf --outdir "$tmp" "$deck" >/dev/null 2>&1
pdf=$(ls "$tmp"/*.pdf | head -1)
pdftoppm -r "$dpi" -png "$pdf" "$out/slide"
rm -rf "$tmp"
echo "تم: $(ls "$out"/slide-*.png | wc -l) شريحة في $out"
