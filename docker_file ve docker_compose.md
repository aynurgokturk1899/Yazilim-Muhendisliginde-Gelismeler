Sağlık Takip Sistemi REST API ve İstemciler

Bu proje, Flask kullanılarak geliştirilmiş bir Sağlık Takip API'si ve bu API'nin yeteneklerini gösteren birden fazla istemci uygulamasını (Doktor Paneli, Diyetisyen Paneli, Hasta Paneli) içerir. Tüm servisler Docker ve Docker Compose ile yönetilmektedir.

🚀 Projeyi Çalıştırma

Projenin çalıştırılması ve gerekli Docker imajlarının oluşturulması için aşağıdaki adımları takip edin:

1. Docker İmajının Oluşturulması

Projenin temel Python imajı, Dockerfile kullanılarak oluşturulur. İmajı oluşturmak için projenin ana dizininde aşağıdaki komutu çalıştırın:

docker build -t saglik-takip-img .


2. Docker Compose ile Başlatma

API ve temel istemci servisini tek bir komutla ayağa kaldırmak ve yayınlamak için:

docker compose up -d


(Bu komut, projenizi arka planda (-d) çalıştırır ve Dockerfile üzerinden imajları otomatik olarak oluşturur.)

3. Erişim Adresleri

Servisler başarıyla başlatıldıktan sonra, aşağıdaki adreslerden erişim sağlayabilirsiniz:

Servis Adı

Port

Erişim Adresi

Ana API Servisi

5000

http://localhost:5000/

Temel İstemci (Kullanıcı Ekleme)

5001

http://localhost:5001/

Doktor Paneli (doctor_client.py)

5002

http://localhost:5002/

Diyetisyen Paneli (dietitian_client.py)

5003

http://localhost:5003/

Hasta Paneli (patient_client.py)

5004

http://localhost:5004/

Not: Bu docker-compose.yml dosyası sadece saglik_takip_app ve client_app servislerini içerir. Eğer Doktor (5002), Diyetisyen (5003) veya Hasta (5004) panellerini de çalıştırmak isterseniz, bu servisleri docker-compose.yml dosyasına eklemeniz gerekmektedir.
