# 🩺 Sağlık Takip Sistemi (Çok Servisli Docker Uygulaması)

Bu proje, Hastalar, Doktorlar ve Diyetisyenler için çizelge yönetimi sağlayan ve Flask tabanlı mikroservislerden oluşan bir sağlık takip sistemidir.

## 🌟 Proje Mimarisi

Sistem, beş ayrı Docker servisi olarak çalışır ve portlar üzerinden birbirleriyle iletişim kurar:

| Servis Adı | Port | Açıklama |
| :--- | :--- | :--- |
| **saglik_takip_app** | 5000 | Tüm veritabanı (in-memory) ve API rotalarını barındırır. |
| **client_app** | 5001 | Kullanıcı Giriş/Kayıt Merkezi. |
| **doctor_client** | 5002 | Doktor Paneli (Hasta onaylama ve İlaç Çizelgesi yönetimi). |
| **dietitian_client** | 5003 | Diyetisyen Paneli (Hasta onaylama ve Yemek Çizelgesi yönetimi). |
| **patient_client** | 5004 | Hasta Paneli (Çizelgeleri görüntüleme). |

---

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için **Docker** ve **Docker Compose** kurulu olmalıdır.

### 1. Docker İmajını Oluşturma

Projeye ait temel Python ortamı ve imajını `Dockerfile` üzerinden oluşturur. (Bu, projenin taşınabilir olmasını sağlar.)

```bash
docker build -t saglik-takip-image .
2. Servisleri Başlatma ve Yayınlama
Tüm servisleri arka planda (detached mode) başlatır ve belirlenen portlar üzerinden yayın yapar:

Bash

docker-compose up -d
Komut Açıklaması:

docker-compose up: docker-compose.yml dosyasını okur ve tüm servisleri oluşturup başlatır.

-d (Detach Mode): Servisleri arka planda çalıştırır, terminalinizi serbest bırakır.

3. Servisleri Durdurma
Arka planda çalışan tüm konteynerleri durdurmak ve kaldırmak için:

Bash

docker-compose down
🌐 Erişimi Adresleri
Uygulamaya erişim için tarayıcınızda aşağıdaki adresleri kullanın:

Ana Giriş/Kayıt Merkezi: http://localhost:5001

Doktor Paneli: http://localhost:5002

Diyetisyen Paneli: http://localhost:5003

Hasta Paneli: http://localhost:5004
