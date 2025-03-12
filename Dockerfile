FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY .streamlit /app/.streamlit/
COPY main.py ui.py /app/
COPY widgets/* /app/widgets/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/tv/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501"]