FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pwd
RUN ls -la
RUN find . -maxdepth 2

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]