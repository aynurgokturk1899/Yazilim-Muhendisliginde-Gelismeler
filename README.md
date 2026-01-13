# 🏥 Sağlık Takip Sistemi ve Mikroservis Mimarisi

Bu proje, doktorlar, diyetisyenler ve hastalar arasındaki etkileşimi yöneten, **Dockerize edilmiş** ve **mikroservis mimarisine** sahip kapsamlı bir Flask uygulamasıdır. İçerisinde rol tabanlı yönetim panelleri (RBAC), REST API, Prometheus/Grafana ile sistem izleme (monitoring) ve MCP (Model Context Protocol) tabanlı yapay zeka entegrasyonları barındırır.

## 🚀 Proje Özellikleri

* **Mikroservis Yapısı:** Her rol (Doktor, Diyetisyen, Hasta) ve servis (API, DB, AI) izole konteynerlerde çalışır.
* **Rol Bazlı Yetkilendirme:**
    * 👨‍⚕️ **Doktorlar:** Hastaları onaylar, ilaç çizelgeleri oluşturur.
    * 🥗 **Diyetisyenler:** Hastaları onaylar, beslenme programları yazar.
    * 💊 **Hastalar:** Doktor ve Diyetisyen seçer, kendi reçete ve programlarını görüntüler.
* **Yapay Zeka (MCP) Entegrasyonu:** LLM'lerin dış dünya ile etkileşime geçmesini sağlayan özel araçlar (BMI Hesaplama, Motivasyon Sözü API).
* **Gelişmiş İzleme (Monitoring):** Custom Python Exporter ile sıcaklık verisi simülasyonu, Prometheus ile veri toplama ve Grafana paneli.
* **Güvenlik:** JWT (JSON Web Token) tabanlı kimlik doğrulama simülasyonları.

---

## 🛠️ Kurulum ve Çalıştırma

Proje **Docker Compose** ile tam entegre çalışmaktadır. Tüm sistemi ayağa kaldırmak için aşağıdaki adımları izleyin:

### Gereksinimler
* Docker ve Docker Compose

### Başlatma Komutu
Proje ana dizininde terminali açın ve şu komutu çalıştırın:

``bash
docker-compose up --build  




# 🏥 Sağlık Takip Sistemi ve Mikroservis Mimarisi

Bu proje, doktorlar, diyetisyenler ve hastalar arasındaki etkileşimi yöneten, **Dockerize edilmiş** ve **mikroservis mimarisine** sahip kapsamlı bir Flask uygulamasıdır. İçerisinde rol tabanlı yönetim panelleri (RBAC), REST API, Prometheus/Grafana ile sistem izleme (monitoring) ve MCP (Model Context Protocol) tabanlı yapay zeka entegrasyonları barındırır.

## 🚀 Proje Özellikleri

* **Mikroservis Yapısı:** Her rol (Doktor, Diyetisyen, Hasta) ve servis (API, DB, AI) izole konteynerlerde çalışır.
* **Rol Bazlı Yetkilendirme:**
    * 👨‍⚕️ **Doktorlar:** Hastaları onaylar, ilaç çizelgeleri oluşturur.
    * 🥗 **Diyetisyenler:** Hastaları onaylar, beslenme programları yazar.
    * 💊 **Hastalar:** Doktor ve Diyetisyen seçer, kendi reçete ve programlarını görüntüler.
* **Yapay Zeka (MCP) Entegrasyonu:** LLM'lerin dış dünya ile etkileşime geçmesini sağlayan özel araçlar (BMI Hesaplama, Motivasyon Sözü API).
* **Gelişmiş İzleme (Monitoring):** Custom Python Exporter ile sıcaklık verisi simülasyonu, Prometheus ile veri toplama ve Grafana paneli.
* **Güvenlik:** JWT (JSON Web Token) tabanlı kimlik doğrulama simülasyonları.





## 🛠️ Kurulum ve Çalıştırma

Proje **Docker Compose** ile tam entegre çalışmaktadır. Tüm sistemi ayağa kaldırmak için aşağıdaki adımları izleyin:

### Gereksinimler
* Docker ve Docker Compose

### Başlatma Komutu
Proje ana dizininde terminali açın ve şu komutu çalıştırın:

``bash
docker-compose up --build

Servis Adı	Port	Görevi
saglik_takip_app	5000	Ana Backend API: Veritabanı işlemleri, kullanıcı yönetimi ve iş mantığını (Business Logic) yürütür.
saglik_db	5432	Veritabanı: PostgreSQL tabanlı; kullanıcı, hasta eşleşmeleri ve çizelge verilerini saklar.
client_web_app	5001	Giriş/Kayıt Merkezi: Kullanıcıların sisteme kayıt olduğu ve rol bazlı yönlendirildiği ön yüz.
doctor_web_app	5002	Doktor Paneli: Hasta onaylama ve ilaç çizelgesi oluşturma arayüzü.
dietitian_web_app	5003	Diyetisyen Paneli: Beslenme programı hazırlama arayüzü.
patient_web_app	5004	Hasta Paneli: Profil görüntüleme, ilaç ve yemek programlarını takip etme arayüzü.
saglik_mcp_server	-	AI Ajanı (MCP): BMI hesaplama ve dış kaynaklardan motivasyon sözü çekme işlemlerini yapan yardımcı servis.



🤖 Yapay Zeka ve MCP (Model Context Protocol)
Bu proje, yapay zeka asistanının yeteneklerini artırmak için FastMCP tabanlı özel bir sunucu (mcp_server.py) içerir. Bu sunucu, LLM'in (Büyük Dil Modeli) doğrudan kendi başına yapamayacağı işlemler için 2 özel araç (tool) sağlar:

1. Vücut Kitle İndeksi (BMI) Hesaplayıcı
Fonksiyon: vucut_kitle_indeksi_hesapla(kilo, boy_cm)

Görevi: Kullanıcıdan alınan boy ve kilo verilerini işler, BMI değerini hesaplar ve DSÖ standartlarına göre (Zayıf, Normal, Obez vb.) durum analizi yapar.

Kullanım Senaryosu: Asistan, kullanıcının fiziksel bilgilerini aldığında bu aracı otomatik olarak çağırır.

2. Günlük Motivasyon Servisi (Dış API)
Fonksiyon: gunluk_motivasyon_sozu_getir()

Görevi: zenquotes.io API'sine gerçek zamanlı bir HTTP isteği (GET) atar.

Kullanım Senaryosu: Kullanıcı moral verici bir söz istediğinde, asistan statik veri yerine bu aracı kullanarak internetten güncel bir söz çeker.

🔐 Kimlik Doğrulama ve JWT Testi
Proje, ana uygulamanın haricinde, token tabanlı güvenliği (Bearer Token) test etmek için harici bir sunucu içerir. Bu modül Docker Compose'dan bağımsız olarak manuel test edilebilir.

Manuel Çalıştırma:

Bash

python server.py
# Sunucu http://localhost:5005 adresinde başlar.
Test İstemcisi: Token alma ve korumalı rotaya erişim akışını simüle etmek için:

Bash

python client.py
Test Kullanıcısı: alice

Şifre: 123456

📊 Monitoring (İzleme)
Sistem, uygulama sağlığını ve çevresel verileri izlemek için Prometheus ve Grafana kullanır.

Weather Exporter (Port 8000): Python ile yazılmış özel bir scripttir. Türkiye'nin 81 ilinden rastgele sıcaklık verisi üretir ve Prometheus formatında yayınlar.

Prometheus: Bu verileri scrape_interval periyotlarında toplar.

Grafana: Toplanan verileri görselleştirir.

Dashboard: "Türkiye Hava Durumu Paneli" (En sıcak 5 şehir, anlık sıcaklık listesi vb.)

📚 Dokümantasyon ve Diyagramlar
Swagger (OpenAPI): API uç noktalarını test etmek ve teknik detayları görmek için tarayıcınızdan şu adrese gidin: http://localhost:5000/apidocs/

MermaidJS Diyagramları: Projenin akış diyagramları (Sequence Diagram) proje içerisindeki mermaidjskodu.txt dosyasında mevcuttur.

🏗️ Kullanılan Teknolojiler
Backend: Python 3.11, Flask, SQLAlchemy

Database: PostgreSQL 13

DevOps: Docker, Docker Compose

AI: Ollama, FastMCP, Open WebUI

Monitoring: Prometheus, Grafana

Diğer: Flasgger (Swagger UI), Requests, JWT
