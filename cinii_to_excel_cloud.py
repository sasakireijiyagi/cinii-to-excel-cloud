import requests
import pandas as pd
from urllib.parse import urlencode, quote
from datetime import datetime
import time
import streamlit as st
import io

st.title("CiNii 論文検索 to Excel (Cloud)")

with st.form(key="search_form"):
    keyword = st.text_input("検索語を入力してください", value="", placeholder="例：風景構成法")
    run = st.form_submit_button("検索してExcel出力")

# --- 既存のパース・保存ロジック ---
def parse_articles_json(json_data):
    records = []
    entries = json_data.get('items', [])
    for entry in entries:
        authors = entry.get('dc:creator', [])
        if isinstance(authors, list):
            authors = '，'.join([str(a).replace(' ', '') for a in authors])
        else:
            authors = str(authors).replace(' ', '')
        pubdate = entry.get('prism:publicationDate', '')
        pubyear = pubdate[:4] if pubdate else ''
        pubyear_disp = f"({pubyear})" if pubyear else ''
        title = entry.get('title', '')
        journal = entry.get('prism:publicationName', '')
        volume = entry.get('prism:volume', '')
        issue = entry.get('prism:number', '')
        spage = entry.get('prism:startingPage', '')
        epage = entry.get('prism:endingPage', '')
        page_range = f"{spage}-{epage}" if spage and epage else spage or epage
        publisher = entry.get('dc:publisher', '')
        url = entry.get('@id', '')
        if not url:
            link = entry.get('link', {})
            url = link.get('@id', '') if isinstance(link, dict) else ''
        concat = authors + pubyear_disp + title + journal + volume + issue + page_range + publisher
        try:
            pubyear_int = int(pubyear)
        except:
            pubyear_int = -9999
        records.append({
            '著者': authors,
            '出版年': pubyear_disp,
            'タイトル': title,
            '掲載誌名': journal,
            '巻': volume,
            '号': issue,
            'ページ範囲': page_range,
            '出版社名': publisher,
            'URL': url,
            '結合カラム': concat,
            '_sort_year': pubyear_int
        })
    return records

def fetch_total_results(keyword):
    base_url = "https://cir.nii.ac.jp/opensearch/articles"
    params = {
        "q": keyword,
        "count": 1,
        "start": 1,
        "format": "json",
    }
    url = f"{base_url}?{urlencode(params)}"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        return int(data.get('opensearch:totalResults', 0))
    except Exception as e:
        st.error(f"[totalResults取得失敗] {e}")
        return 0

def fetch_articles_json(keyword, start, count=100):
    base_url = "https://cir.nii.ac.jp/opensearch/articles"
    params = {
        "q": keyword,
        "count": count,
        "start": start,
        "format": "json",
    }
    url = f"{base_url}?{urlencode(params)}"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"[start={start}] HTTP error: {e}")
        return None

def save_to_excel(records, keyword):
    df = pd.DataFrame(records)
    if '_sort_year' in df.columns:
        df = df.sort_values('_sort_year', ascending=False)
    if '_sort_year' in df.columns:
        df = df.drop(columns=['_sort_year'])
    columns = ['著者', '出版年', 'タイトル', '掲載誌名', '巻', '号', 'ページ範囲', '出版社名', 'URL', '結合カラム']
    df = df[columns]
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output

if run and keyword.strip():
    st.info(f"検索語: {keyword}")
    total = fetch_total_results(keyword)
    if total == 0:
        st.warning("データなしまたは取得失敗")
    else:
        st.write(f"totalResults: {total}")
        all_records = []
        for start in range(1, total+1, 100):
            st.write(f"現在{start}件目取得中...")
            json_data = fetch_articles_json(keyword, start, count=100)
            if not json_data:
                continue
            records = parse_articles_json(json_data)
            all_records.extend(records)
            time.sleep(0.5)
        if all_records:
            excel_bytes = save_to_excel(all_records, keyword)
            st.success("Excelファイルの準備ができました")
            st.download_button(
                label="Excelファイルをダウンロード",
                data=excel_bytes,
                file_name="cinii_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="download_btn"
            )
        else:
            st.warning("レコードが取得できませんでした") 