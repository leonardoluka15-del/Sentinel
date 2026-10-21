FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home --uid 10001 sentinel && mkdir /app/data && chown sentinel:sentinel /app/data
COPY --chown=sentinel:sentinel app.py /app/app.py
COPY --chown=sentinel:sentinel sentinel /app/sentinel
USER sentinel
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:'+os.getenv('PORT','8501')+'/health',timeout=3)"
CMD ["python", "app.py", "--host", "0.0.0.0"]
