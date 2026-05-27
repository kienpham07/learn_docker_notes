FROM python:3.9-slim
COPY main.py .
COPY books/ books/
CMD ["python", "main.py"]