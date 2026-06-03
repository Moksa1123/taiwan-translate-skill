#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[已停用] translate.py

舊版 translate.py 採用「子字串自動代換」翻譯，會把詞彙逐詞塞回原句，
導致詞中誤匹配（bug→程式碼錯誤連 debug 都中、整句被換成亂碼）。
此設計把「詞彙參考」與「整句翻譯」搞反了，已停用。

正確理念：
    詞彙表是「確保用詞一致的參考」，不是拿來做整句機器翻譯。
    整句翻譯由模型完成（查詞彙 + 風格指南），再用 validator 把關。

請改用：
    python scripts/lookup.py "<text>"          # 詞彙查詢（取代原 translate 的好部分）
    python scripts/po.py extract  <file.po>     # 抽出未翻譯 msgid（給模型翻譯）
    python scripts/po.py validate <file.po>     # 把關：佔位符/首字/用語/空格…
"""

import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

MESSAGE = """\
⚠️  translate.py 已停用（不再做整句自動代換）。

原因：子字串自動代換會產生亂碼（例如 bug→程式碼錯誤 連 debug 都中）。
詞彙表僅供參考，整句翻譯請由模型完成，再用 validator 把關。

請改用下列工具：

  詞彙查詢：
      python scripts/lookup.py "<text>"

  抽出 PO 未翻譯項目（交給模型翻譯）：
      python scripts/po.py extract  <file.po>

  PO 翻譯把關（佔位符/首字大小寫/中國用語/空格…）：
      python scripts/po.py validate <file.po>
"""


def main():
    print(MESSAGE)
    sys.exit(2)


if __name__ == '__main__':
    main()
