FROM python:3.10.8
COPY . .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3", "main.py"]