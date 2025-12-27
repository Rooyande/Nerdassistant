FROM python:3.12-slim

# جلوگیری از بافر شدن لاگ‌ها + رفتار بهتر پایتون داخل کانتینر
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نصب پکیج‌های پایه
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# نصب وابستگی‌ها
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# کد پروژه
COPY . /app

# اجرای بات
CMD ["python", "-m", "bot.main"]
