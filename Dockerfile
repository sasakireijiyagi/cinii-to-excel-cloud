# CiNii 一目瞭然（Streamlit）— さくらVPS配備用
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# secrets は ~/apps/cinii-db/.streamlit をマウントして渡す（イメージには焼き込まない）
CMD ["streamlit", "run", "cinii_to_excel_cloud.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
