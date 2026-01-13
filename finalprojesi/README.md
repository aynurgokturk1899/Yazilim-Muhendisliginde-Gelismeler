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

Servis Adı	Port	Açıklama
Giriş/Kayıt Paneli	5001	Kullanıcıların sisteme girdiği ana kapı (Gateway) - client_app.py

Backend API	5000	Ana Flask API Sunucusu (Veritabanı işlemleri) - app1.py

Doktor Paneli	5002	Doktor yönetim arayüzü - doctor_client.py

Diyetisyen Paneli	5003	Diyetisyen yönetim arayüzü - dietitian_client.py

Hasta Paneli	5004	Hasta görüntüleme arayüzü - patient_client.py

Grafana	3000	Görselleştirme Paneli (Kullanıcı: admin / Şifre: admin_grafana_guvenli)

Prometheus	9091	Metrik toplama sunucusu

Open WebUI	8081	Yerel LLM (Ollama) ile sohbet arayüzü

JWT Test Sunucusu	5005	(Manuel Çalıştırılır) Bağımsız Token test sunucusu



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


İsteğiniz üzerine, projenizin güvenliğini ve kod kalitesini artıracak 5 kritik güvenlik ve iyileştirme önerisini aşağıda sunuyorum:

1. Şifrelerin Düz Metin (Plain Text) Saklanması (Kritik Güvenlik Açığı)
Mevcut kodunuzda, kullanıcı şifreleri veritabanına doğrudan kaydedilmekte ve giriş yapılırken doğrudan karşılaştırılmaktadır.

Tespit: app1.py dosyasında giriş kontrolü if user and user.password == password: şeklinde yapılmaktadır. Ayrıca models.py dosyasında şifre sütunu düz string olarak tanımlanmıştır.

Öneri: Şifreleri asla veritabanında açık halde tutmayın. Werkzeug.security kütüphanesinden generate_password_hash ve check_password_hash fonksiyonlarını kullanarak şifreleri hash (karma) formatında saklayın. Bu, veritabanınız ele geçirilse bile şifrelerin çalınmasını engeller.

2. IDOR (Insecure Direct Object Reference) ve Oturum Yönetimi Eksikliği
Uygulamanızda giriş yapıldıktan sonra kullanıcı kimliği URL parametresi (Query Parameter) olarak taşınmaktadır.

Tespit: Örneğin doctor_client.py dosyasında request.args.get('id', 2, type=int) ile doktorun kimliği alınmaktadır. Bir kullanıcı, tarayıcı adres çubuğundaki ?id=2 değerini ?id=3 yaparak başka bir doktorun paneline yetkisiz erişim sağlayabilir.

Öneri: server.py dosyasında denediğiniz JWT (JSON Web Token) yapısını ana uygulamanız olan app1.py'ye entegre edin. Kimlik bilgisini URL'de taşımak yerine, giriş sonrası üretilen Token'ı HTTP Header (Authorization: Bearer ...) içinde taşıyarak sunucuda doğrulayın.

3. XSS (Cross-Site Scripting) Riski ve Template Kullanımı
HTML içerikleri Python kodu içinde string olarak oluşturulmakta ve render_template_string ile sunulmaktadır.

Tespit: doctor_client.py ve diğer istemci dosyalarında HTML_TEMPLATE değişkenleri f-string (formatlı string) olarak tanımlanmıştır. Eğer bir kullanıcı, ilaç adı veya hasta ismi yerine <script>alert('Hacked')</script> gibi bir kod girerse, bu kod diğer kullanıcıların tarayıcısında çalıştırılabilir (Code Injection).

Öneri: Flask'ın şablon motoru olan Jinja2'nin .html dosyalarını kullanın (render_template). Jinja2, değişkenleri varsayılan olarak "escape" ederek (zararsız hale getirerek) XSS saldırılarını otomatik olarak önler.

4. Hassas Verilerin Kod İçinde Saklanması (Hardcoded Secrets)
Veritabanı şifreleri ve gizli anahtarlar kodun içine gömülmüş durumdadır.

Tespit: app1.py içinde veritabanı bağlantısı için varsayılan değer olarak postgresql://admin:adminpassword@... tanımlanmıştır. Ayrıca server.py dosyasında SECRET_KEY = "super-gizli-anahtar-123" şeklinde açıkça yazılmıştır.

Öneri: Bu değerleri koddan tamamen kaldırın. Yüklediğiniz .env dosyasını aktif olarak kullanın ve Python tarafında os.environ.get('SECRET_KEY') şeklinde çağırın. .env dosyasını asla Git geçmişine (commit) eklemeyin.

5. Docker Servis İzolasyonu ve Port Güvenliği
Docker Compose yapılandırmanızda bazı servisler dış dünyaya gereksiz yere açılmış durumdadır.

Tespit: docker-compose.yml dosyasında veritabanı servisi (db), 5432:5432 portu ile dış dünyaya açılmıştır. Bu, internete açık bir sunucuda veritabanınıza dışarıdan saldırı yapılmasına olanak tanır. Ayrıca open-webui servisinde WEBUI_AUTH=False ayarı yapılmıştır, bu da paneli herkese açık hale getirir.

Öneri: Veritabanı gibi backend servislerinin ports kısmını kaldırın veya sadece localhost'a açın (127.0.0.1:5432:5432). Uygulamalarınız (app1.py vb.) Docker ağı (network) içinde veritabanına servis ismiyle (db) zaten erişebilir; dışarıdan erişime gerek yoktur.

