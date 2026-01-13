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

