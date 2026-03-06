# 💰 AI Destekli Kişisel Finans Asistanı Pro

Bu proje, yapay zeka (LLM) kullanarak kişisel harcama metinlerinizi analiz eden, kategorilere ayıran, tasarruf önerileri sunan ve kapsamlı finans yönetimi sağlayan tam özellikli bir uygulamadır.

## ✨ Özellikler

### 🤖 AI Destekli Analiz
- Doğal dil ile harcama girişi
- Otomatik kategorizasyon
- Akıllı tasarruf önerileri
- Detaylı harcama özeti

### 💰 Gelir & Gider Yönetimi
- Harcama takibi ve geçmişi
- Gelir kaydı ve takibi
- Kategori bazlı analiz
- Zaman serisi grafikleri

### 🎯 Bütçe Kontrolü
- Kategori bazlı bütçe belirleme
- Aylık/Haftalık/Yıllık bütçe
- Otomatik bütçe uyarıları
- Bütçe aşım bildirimleri

### 📊 Raporlama & Analiz
- Detaylı dashboard
- Kategori dağılımı grafikleri
- Zaman serisi analizleri
- Karşılaştırmalı raporlar
- CSV/Excel export

### 🎯 Hedef Takibi
- Tasarruf hedefleri belirleme
- İlerleme takibi
- Hedef tarihi uyarıları
- Aylık tasarruf önerileri

### 🔄 Düzenli Ödemeler
- Fatura ve abonelik takibi
- Ödeme hatırlatmaları
- Gecikme uyarıları
- Aylık toplam hesaplama

### 📈 Gelişmiş Özellikler
- SQLite veritabanı
- Çoklu sayfa navigasyon
- Tarih filtreleme
- Responsive tasarım
- Gerçek zamanlı istatistikler

## 🏗 Mimari

Proje iki ana bileşenden oluşur:

- **Backend (FastAPI)**: `backend/` klasöründe bulunur. LLM servisine bağlanır, veritabanı yönetir ve tüm iş mantığını yönetir.
- **Frontend (Streamlit)**: `frontend/` klasöründe bulunur. Kullanıcı arayüzü ve görselleştirme sağlar.

## 🚀 Kurulum

### 1. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. API Anahtarlarını Ayarlayın

`.env` dosyasını düzenleyin ve Groq API anahtarınızı ekleyin:

```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

Groq API anahtarı almak için: https://console.groq.com/keys

### 3. Veritabanını Başlatın

Backend ilk çalıştırıldığında otomatik olarak SQLite veritabanı oluşturulacaktır.

## 🏃‍♂️ Çalıştırma

Projenin çalışması için iki ayrı terminal kullanmanız gerekir.

### 1. Backend'i Başlatma

Proje ana dizininde:

```bash
uvicorn backend.app:app --reload
```

API adresi: http://127.0.0.1:8000

### 2. Frontend'i Başlatma

#### Basit Versiyon (Sadece Analiz):
```bash
streamlit run frontend/app.py
```

#### Gelişmiş Versiyon (Tüm Özellikler):
```bash
streamlit run frontend/app_advanced.py
```

Uygulama tarayıcıda otomatik açılacaktır (Genellikle http://localhost:8501).

## 📁 Proje Yapısı

```
.
├── backend/
│   ├── __init__.py
│   ├── app.py           # FastAPI servisi ve API endpoints
│   ├── agent.py         # AI Agent mantığı (Groq entegrasyonu)
│   ├── prompts.py       # AI sistem istemleri
│   └── database.py      # SQLite veritabanı yönetimi
├── frontend/
│   ├── __init__.py
│   ├── app.py           # Basit Streamlit arayüzü
│   └── app_advanced.py  # Gelişmiş Streamlit arayüzü (Tüm özellikler)
├── .env                 # API anahtarları (Gizli)
├── .gitignore          # Git ignore kuralları
├── requirements.txt     # Python bağımlılıkları
├── finance.db          # SQLite veritabanı (otomatik oluşturulur)
└── README.md           # Dokümantasyon
```

## 🛠 Kullanılan Teknolojiler

### Backend
- **FastAPI** - Modern, hızlı web framework
- **SQLite** - Hafif veritabanı
- **Groq API** - AI model servisi (Llama 3.3)
- **Pydantic** - Veri validasyonu

### Frontend
- **Streamlit** - Hızlı web uygulaması geliştirme
- **Plotly** - İnteraktif grafikler
- **Pandas** - Veri analizi
- **ReportLab** - PDF oluşturma

### AI
- **Groq** - Hızlı LLM inference
- **Llama 3.3 70B** - Güçlü dil modeli

## 📊 API Endpoints

### Harcama Analizi
- `POST /analyze` - Harcama metnini analiz et
- `GET /expenses` - Harcama geçmişini getir
- `POST /expenses/save` - Harcamaları kaydet

### Gelir Yönetimi
- `POST /income` - Gelir ekle
- `GET /income` - Gelir geçmişini getir

### Bütçe Yönetimi
- `POST /budget` - Bütçe belirle
- `GET /budget` - Bütçeleri getir
- `GET /budget/check` - Bütçe kontrolü yap

### Hedefler
- `POST /goals` - Hedef ekle
- `GET /goals` - Hedefleri getir

### Düzenli Ödemeler
- `POST /recurring` - Düzenli ödeme ekle
- `GET /recurring` - Düzenli ödemeleri getir

### Raporlama
- `GET /statistics` - İstatistikleri getir
- `GET /dashboard` - Dashboard verilerini getir

## 🎯 Kullanım Örnekleri

### Harcama Analizi
```
"Bugün market alışverişi 350 TL, akşam yemeği 180 TL, taksi 50 TL"
```

AI otomatik olarak:
- Kategorilere ayırır (Yemek & İçecek, Ulaşım, vb.)
- Tutarları çıkarır
- Etiketler (temel, lüks, vb.)
- Özet oluşturur
- Tasarruf önerileri sunar

### Bütçe Belirleme
- Kategori seçin (Yemek & İçecek, Ulaşım, vb.)
- Tutar belirleyin (örn: 5000 TL)
- Periyot seçin (Aylık, Haftalık, Yıllık)
- Otomatik uyarılar alın

### Hedef Oluşturma
- Hedef adı (örn: "Tatil")
- Hedef tutar (örn: 15000 TL)
- Hedef tarih
- İlerleme takibi

## 🔒 Güvenlik

- API anahtarları `.env` dosyasında saklanır
- `.gitignore` ile hassas dosyalar korunur
- Veritabanı yerel olarak saklanır
- CORS yapılandırması mevcut

## 🚧 Gelecek Özellikler

- [ ] PDF rapor oluşturma
- [ ] Fotoğraf/Fiş okuma (OCR)
- [ ] Banka entegrasyonu
- [ ] Çoklu kullanıcı desteği
- [ ] Mobil uygulama
- [ ] Döviz desteği
- [ ] Yatırım takibi
- [ ] E-posta bildirimleri

## 📝 Lisans

Bu proje eğitim amaçlıdır.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not:** Bu uygulama AI kullanır ve sonuçlar %100 doğru olmayabilir. Önemli finansal kararlar için profesyonel danışmanlık alın.
