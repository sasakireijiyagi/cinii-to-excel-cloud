# CiNii 一目瞭然　［日本語文献瞬間検索］

CiNiiの日本語文献データを、もっと手軽に。結果はその場で一覧表示、Excelファイルにも書き出せます。

🔗 **[アプリを使う](https://cinii-to-excel-cloud-ffvog4pekzpvzk823jreac.streamlit.app/)**

---

## 機能

- キーワードで日本語文献を全件検索（件数上限なし）
- 検索結果をブラウザ上で一覧表示（100件ずつ追加表示）
- Excelファイル（.xlsx）へのエクスポート
- 出版年の新しい順にソート
- CiNiiページへのリンクボタン付き

## 使い方

1. キーワードを入力して「検索してExcel出力」をクリック
2. 検索結果が画面に表示される
3. 必要に応じてExcelファイルをダウンロード

## 技術スタック

- [Streamlit](https://streamlit.io/)
- [CiNii Research API](https://cir.nii.ac.jp/) (国立情報学研究所)
- pandas / openpyxl

> 本アプリは国立情報学研究所（NII）が提供するCiNii APIを利用しています。

## 作者

**佐々木玲仁研究室**（九州大学臨床心理学講座）  
🐐 [ヤギ製作所](https://sasakireijiyagi.com/home)
