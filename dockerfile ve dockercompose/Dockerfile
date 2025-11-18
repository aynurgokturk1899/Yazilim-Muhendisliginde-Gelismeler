# Resmi bir Python çalışma zamanı imajını temel al
FROM python:3.9-slim

# Çalışma dizinini /app olarak ayarla
WORKDIR /app

# Gereksinimler dosyasını konteynere kopyala
COPY requirements.txt .

# Gerekli Python bağımlılıklarını kur
RUN pip install --no-cache-dir -r requirements.txt

# Projenin geri kalan dosyalarını konteynere kopyala
# (app1.py, patient_routes1.py, doctor_routes1.py, vb. dahil)
COPY . .

# Flask uygulamasının çalışacağı portu bildir
EXPOSE 5000

# Ortam değişkenini ayarlayarak Gunicorn/uWSGI gibi bir WSGI sunucusu kullanmak daha iyi olsa da,
# basitlik için şimdilik doğrudan 'app1.py' dosyasını çalıştıracağız.
# Üretim ortamında 'app.run(debug=True)' KULLANILMAMALIDIR.

# Uygulamayı çalıştır
CMD ["python", "app1.py"]