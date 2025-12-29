# Dockerfile (GÜNCELLENDİ)

# Resmi bir Python çalışma zamanı imajını temel al
FROM python:3.9-slim

# Gerekli ağ araçlarını (ping, netcat/nc) kur
RUN apt-get update && apt-get install -y iputils-ping netcat-traditional && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini /app olarak ayarla
WORKDIR /app

# Gereksinimler dosyasını konteynere kopyala
COPY requirements.txt .
# Gerekli Python bağımlılıklarını kur
RUN pip install --no-cache-dir -r requirements.txt

# Projenin geri kalan dosyalarını konteynere kopyala
COPY . .

# Flask uygulamasının çalışacağı portu bildir
EXPOSE 5000

# Uygulamayı çalıştırmak için CMD kullanacağız. (docker-compose'da ezilecek)
CMD ["python", "app1.py"]