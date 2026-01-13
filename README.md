# 🏥 Sağlık Takip Sistemi ve Mikroservis Mimarisi

Bu proje, doktorlar, diyetisyenler ve hastalar arasındaki etkileşimi yöneten, Dockerize edilmiş, mikroservis mimarisine sahip kapsamlı bir Flask uygulamasıdır. İçerisinde REST API, rol bazlı yönetim panelleri, Prometheus/Grafana ile izleme (monitoring) ve yapay zeka entegrasyonları barındırır.

## 🚀 Kurulum ve Çalıştırma

Proje Docker Compose ile tam entegre çalışmaktadır. Tüm sistemi ayağa kaldırmak için proje dizininde şu komutu çalıştırmanız yeterlidir:

`bash
docker-compose up --build

## Servis Adı	Port	Açıklama			
Backend API	5000	Ana Flask API Sunucusu (Veritabanı işlemleri)			
Giriş/Kayıt Paneli	5001	Kullanıcıların sisteme girdiği ana kapı (Gateway)			
Doktor Paneli	5002	Doktorların hasta yönetimi ve ilaç atama ekranı			
Diyetisyen Paneli	5003	Diyetisyenlerin yemek programı oluşturma ekranı			
Hasta Paneli	5004	Hastaların kendi verilerini ve programlarını gördüğü ekran			
JWT Test Sunucusu	5005	Manuel çalıştırılırsa JWT Token test ve doğrulama ekranı			
Prometheus	9091	Metrik toplama ve sorgulama arayüzü			
Grafana	3000	Görselleştirme Paneli (Giriş: admin / admin_grafana_guvenli)			
Weather Exporter	8000	Python ile yazılmış custom Prometheus exporter (Sıcaklık verisi)			
Open WebUI	8081	Yerel LLM (Ollama) ile sohbet arayüzü			
Ollama API	11435	Yapay zeka model servisi			
PostgreSQL	5432	Veritabanı servisi			
					
Swagger (OpenAPI): API uç noktalarını test etmek ve belgelemek için tarayıcınızdan şu adrese gidin: http://localhost:5000/apidocs/

MermaidJS Diyagramları: Projenin akış diyagramları (Sequence Diagram) mermaidjskodu.txt dosyasında mevcuttur.

### 🤖 MCP Araçları (AI Capabilities)

🧠 Yapay Zeka ve MCP (Model Context Protocol)
Bu proje, yapay zeka asistanının yeteneklerini artırmak için özel bir MCP Sunucusu (mcp_server.py) içerir. Bu sunucu, LLM'in (Büyük Dil Modeli) doğrudan kendi başına yapamayacağı veya dış veriye ihtiyaç duyduğu işlemler için 2 özel araç (tool) sağlar:

Vücut Kitle İndeksi (BMI) Hesaplayıcı

Fonksiyon: vucut_kitle_indeksi_hesapla(kilo, boy_cm)

Görevi: Kullanıcıdan alınan boy ve kilo verilerini matematiksel olarak işler. Sadece sonucu (örn: 24.5) değil, aynı zamanda Dünya Sağlık Örgütü standartlarına göre sağlık durumunu (Zayıf, Normal, Obez vb.) analiz ederek döner.

Kullanım: Asistan, kullanıcının fiziksel bilgilerini aldığında bu aracı otomatik olarak çağırır.

Günlük Motivasyon Servisi (Dış API Entegrasyonu)

Fonksiyon: gunluk_motivasyon_sozu_getir()

Görevi: zenquotes.io API'sine gerçek zamanlı bir HTTP isteği (GET request) atar.

Kullanım: Kullanıcı moral verici bir söz istediğinde, asistan statik veri yerine bu aracı kullanarak internetten rastgele ve güncel bir motivasyon sözü çeker.



🔐 Kimlik Doğrulama ve Token Servisi (JWT)
Proje, ana uygulamanın yanı sıra, güvenli kimlik doğrulama işlemlerini test etmek ve simüle etmek için Port 5005 üzerinde çalışan harici bir JWT (JSON Web Token) servisi içerir.

Dosya: server.py

Port: 5005

Çalıştırma: Bu servis Docker konfigürasyonuna dahil değildir, manuel başlatılmalıdır:

Bash

python server.py
Nasıl Çalışır?
Bu servis, Bearer Token yapısını kullanır. İstemciler önce giriş yaparak bir token alır, ardından bu token'ı kullanarak korumalı alanlara erişir.

1. Token Alma (Login): Kullanıcı adı ve şifre ile /login adresine POST isteği atılır.

Örnek Kullanıcı: alice / 123456

İstek:

Bash

POST http://localhost:5005/login
Body: { "username": "alice", "password": "123456" }
Yanıt: {"token": "eyJ0eXAiOiJKV1QiLCJhbG..."}

2. Korumalı Alana Erişim: Alınan token, sonraki isteklerde Authorization başlığı (header) içinde gönderilmelidir.

Header Formatı: Authorization: Bearer <TOKEN>

İstek:

Bash

GET http://localhost:5005/protected
Headers: { "Authorization": "Bearer eyJ0eXAi..." }
Test İstemcisi: Bu akışı otomatik test etmek için client.py dosyasını çalıştırabilirsiniz:

Bash

python client.py 
