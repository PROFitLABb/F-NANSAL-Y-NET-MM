import streamlit as st
ithalat istekleri
pandas'ı pd olarak içe aktar
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from io import BytesIO
os'u içe aktar

# Doğrudan analiz için yapay zeka yardımcısını içe aktarın
denemek:
    from frontend.ai_helper import analyze_expense_with_ai
    AI_AVAILABLE = True
hariç:
    AI_AVAILABLE = False

# Sayfa yapılandırması
st.set_page_config(
    page_title="AI Finans Asistanı Pro",
    sayfa_simgesi="💰",
    düzen="geniş",
    initial_sidebar_state="expanded"
)

# API Yapılandırması - Ortam değişkeni kullanın veya varsayılan olarak localhost'u kullanın.
API_URL = os.getenv("API_URL", "http://localhost:8000")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

# Özel CSS
st.markdown("""
    <style>
    .main {padding: 0rem 1rem;}
    .stButton>düğme {
        genişlik: %100;
        arka plan rengi: #4CAF50;
        renk: beyaz;
        yazı tipi kalınlığı: kalın;
        border-radius: 8px;
        dolgu: 0.5rem 1rem;
        kenarlık: yok;
    }
    .stButton>button:hover {background-color: #45a049;}
    .metrik-kart {
        arka plan: doğrusal-eğim(135 derece, #667eea %0, #764ba2 %100);
        Dolgu: 1.5rem;
        border-radius: 10px;
        renk: beyaz;
        metin hizala: ortala;
        kutu-gölgesi: 0 4px 6px rgba(0,0,0,0.1);
    }
    .istatistik kutusu {
        arka plan: #f8f9fa;
        border-radius: 10px;
        dolgu: 1rem;
        kenar boşluğu: 10 piksel 0;
        border-left: 5px solid #4CAF50;
        renk: #000000;
    }
    .uyarı kutusu {
        arka plan: #fff3cd;
        border-left: 5px solid #ffc107;
        dolgu: 1rem;
        border-radius: 5px;
        kenar boşluğu: 10 piksel 0;
    }
    .tehlike-kutusu {
        arka plan: #f8d7da;
        border-left: 5px solid #dc3545;
        dolgu: 1rem;
        border-radius: 5px;
        kenar boşluğu: 10 piksel 0;
    }
    .başarı-kutusu {
        arka plan: #d4edda;
        border-left: 5px solid #28a745;
        dolgu: 1rem;
        border-radius: 5px;
        kenar boşluğu: 10 piksel 0;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum durumunu başlat
Eğer 'page' st.session_state içinde değilse:
    st.session_state.page = 'Ana Sayfa'
'all_expenses' st.session_state içinde değilse:
    st.session_state.all_expenses = []

# Yan Menü Navigasyonu
st.sidebar ile:
    st.title("💰 Finans Asistanı Pro")
    st.markdown("---")
    
    sayfa = st.radyo(
        "Menü",
        ["🏠 Ana Sayfa", "📊 Dashboard", "💸 Harcama Analizi", "💰 Gelir Takibi",
         "🎯 Bütçe Yönetimi", "🎯 Hedefler", "🔄 Düzenli Ödemeler",
         "📈 Raporlar", "⚙️ Ayarlar"],
        anahtar="navigasyon"
    )
    st.session_state.page = page
    
    st.markdown("---")
    st.markdown("### 📅 Hızlı Filtreler")
    
    tarih_filtresi = st.seçim kutusu(
        "Tarih Aralığı",
        ["Bu Ay", "Geçen Ay", "Son 3 Ay", "Son 6 Ay", "Bu Yıl", "Özel Tarih"]
    )
    
    if date_filter == "Özel Tarih":
        start_date = st.date_input("Başlangıç")
        bitiş_tarihi = st.tarih_girişi("Bitiş")
    başka:
        bugün = tarih ve saat.şimdi()
        if date_filter == "Bu Ay":
            başlangıç_tarihi = bugün.değiştir(gün=1)
            bitiş_tarihi = bugün
        elif date_filter == "Geçen Ay":
            bitiş_tarihi = bugün.değiştir(gün=1) - zaman_değiştir(gün=1)
            başlangıç_tarihi = bitiş_tarihi.gün=1'i değiştir
        elif date_filter == "Son 3 Ay":
            başlangıç_tarihi = bugün - zaman_değişimi(gün=90)
            bitiş_tarihi = bugün
        elif date_filter == "Son 6 Ay":
            başlangıç_tarihi = bugün - zaman_değişimi(gün=180)
            bitiş_tarihi = bugün
        elif date_filter == "Bu Yıl":
            başlangıç_tarihi = bugün.değiştir(ay=1, gün=1)
            bitiş_tarihi = bugün
    
    st.session_state.start_date = start_date.strftime("%Y-%m-%d")
    st.session_state.end_date = end_date.strftime("%Y-%m-%d")

# Yardımcı fonksiyonlar
def fetch_dashboard_data():
    denemek:
        yanıt = requests.get(f"{API_URL}/dashboard")
        Eğer response.status_code == 200 ise:
            yanıt.json'ı döndürün.
    hariç:
        geçmek
    Hiçbir şey döndür

def fetch_expenses(start_date=None, end_date=None, category=None):
    denemek:
        parametreler = {}
        başlangıç ​​tarihi ise:
            params['start_date'] = start_date
        bitiş tarihi ise:
            params['end_date'] = end_date
        kategori ise:
            params['category'] = category
        
        yanıt = requests.get(f"{API_URL}/expenses", params=params)
        Eğer response.status_code == 200 ise:
            return response.json()['masraflar']
    hariç:
        geçmek
    geri dönmek []

def save_expenses_to_db(expenses):
    denemek:
        yanıt = requests.post(f"{API_URL}/expenses/save", json=expenses)
        yanıtın durum kodunu 200'e eşit olarak döndürün.
    hariç:
        Yanlış döndür

# Sayfa yönlendirmesi
st.session_state.page'de "Ana Sayfa" varsa:
    st.title("🏠 Ana Sayfa")
    st.markdown("### Hoş Geldiniz! AI Destekli Kişisel Finans Asistanınız")
    
    # Hızlı istatistikler
    gösterge paneli_verileri = gösterge paneli_verilerini_alın()
    
    eğer dashboard_data varsa:
        mevcut = gösterge_verisi['mevcut_ay']
        
        sütun1, sütun2, sütun3, sütun4 = st.sütunlar(4)
        
        col1 ile:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>₺{current['total_expenses']:.2f}</h3>
                    <p>Bu Ay Harcama</p>
                </div>
            """, unsafe_allow_html=True)
        
        col2 ile:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>₺{current['total_income']:.2f}</h3>
                    Bu Ay Gelir
                </div>
            """, unsafe_allow_html=True)
        
        col3 ile:
            bakiye_rengi = "#28a745" eğer mevcut['bakiye'] >= 0 ise, aksi halde "#dc3545"
            st.markdown(f"""
                <div class="metric-card" style="background: {balance_color};">
                    <h3>₺{mevcut['bakiye']:.2f</h3>
                    Bakiye
                </div>
            """, unsafe_allow_html=True)
        
        col4 ile:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>{current['expense_count']}</h3>
                    <p>İşlem Sayısı</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Uyarılar
        eğer dashboard_data['budget_warnings'] ise:
            st.subheader("⚠️ Bütçe Uyarıları")
            dashboard_data['budget_warnings'] içindeki uyarı için:
                Eğer uyarı['durum'] 'aşıldı' ise:
                    st.markdown(f"""
                        <div class="danger-box">
                            <strong>🚨 {uyarı['mesaj']}</strong><br>
                            Bütçe: ₺{uyarı['bütçe']:.2f} | Harcanan: ₺{uyarı['harcandı']:.2f}
                        </div>
                    """, unsafe_allow_html=True)
                başka:
                    st.markdown(f"""
                        <div class="warning-box">
                            <strong>⚠️ {uyarı['mesaj']}</strong><br>
                            Bütçe: ₺{uyarı['bütçe']:.2f} | Harcanan: ₺{uyarı['harcandı']:.2f}
                        </div>
                    """, unsafe_allow_html=True)
        
        # Yaklaşan ödemeler
        eğer dashboard_data['upcoming_payments'] ise:
            st.subheader("📅 Yaklaşan Ödemeler")
            dashboard_data['upcoming_payments'] içindeki ödeme için:
                günler = ödeme['günler_kadar']
                Eğer ödeme['gecikmişse']:
                    st.markdown(f"""
                        <div class="danger-box">
                            <strong>🔴 {ödeme['açıklama']}</strong><br>
                            Tutar: ₺{ödeme['tutar']:.2f} | {abs(days)} gün gecikmiş
                        </div>
                    """, unsafe_allow_html=True)
                başka:
                    st.markdown(f"""
                        <div class="warning-box">
                            <strong>🟡 {ödeme['açıklama']}</strong><br>
                            Tutar: ₺{ödeme['tutar']:.2f} | {days} gün kaldı
                        </div>
                    """, unsafe_allow_html=True)
    
    # Hızlı işlemler
    st.markdown("---")
    st.subheader("⚡ Hızlı İşlemler")
    
    sütun1, sütun2, sütun3 = st.sütunlar(3)
    
    col1 ile:
        if st.button("💸 Harcama Ekle", use_container_width=True):
            st.session_state.page = "💸 Harcama Analizi"
            st.rerun()
    
    col2 ile:
        if st.button("💰 Gelir Ekle", use_container_width=True):
            st.session_state.page = "💰 Gelir Takibi"
            st.rerun()
    
    col3 ile:
        if st.button("📊 Rapor Görüntüle", use_container_width=True):
            st.session_state.page = "📈 Raporlar"
            st.rerun()

elif "Dashboard" in st.session_state.page:
    st.title("📊 Kontrol Paneli")
    
    gösterge paneli_verileri = gösterge paneli_verilerini_alın()
    
    eğer dashboard_data varsa:
        mevcut = gösterge_verisi['mevcut_ay']
        son_ay = gösterge_verisi['son_ay']
        
        # Karşılaştırma ölçütleri
        sütun1, sütun2, sütun3 = st.sütunlar(3)
        
        col1 ile:
            gider_değişimi = ((mevcut['toplam_giderler'] - geçen_ay['toplam_giderler']) /
                            last_month['total_expenses'] * 100) eğer last_month['total_expenses'] > 0 ise aksi halde 0
            st.metrik(
                "Bu Ay Harcama",
                f"₺{current['total_expenses']:.2f}",
                f"{gider_değişikliği:+.1f}%"
            )
        
        col2 ile:
            gelir_değişimi = ((mevcut['toplam_gelir'] - geçen_ay['toplam_gelir']) /
                           last_month['total_income'] * 100) eğer last_month['total_income'] > 0 ise aksi halde 0
            st.metrik(
                "Bu Ay Gelir",
                f"₺{current['total_income']:.2f}",
                f"{gelir_değişimi:+.1f}%"
            )
        
        col3 ile:
            st.metrik(
                "Bakiye",
                f"₺{current['balance']:.2f}",
                f"₺{current['balance'] - last_month['balance']:+.2f}"
            )
        
        # Kategoriye göre dağılım
        Eğer mevcut['category_breakdown'] ise:
            st.subheader("📊 Kategori Dağılımı")
            
            sütun1, sütun2 = st.sütunlar(2)
            
            col1 ile:
                # Pasta grafiği
                df_cat = pd.DataFrame(list(current['category_breakdown'].items()),
                                     sütunlar=['Kategori', 'Tutar'])
                fig_pie = px.pie(df_cat, values='Tutar', names='Kategori',
                                title='Harcama Dağılımı', delik=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            col2 ile:
                # Çubuk grafik
                fig_bar = px.bar(df_cat.sort_values('Tutar', ascending=False),
                               x='Kategori', y='Tutar',
                               title='Kategorilere Göre Harcama')
                st.plotly_chart(fig_bar, use_container_width=True)

elif "Harcama Analizi" st.session_state.page'de:
    st.title("💸 Harcama Analizi")
    
    # Gider girişi
    gider_metni = st.metin_alanı(
        "Harcama metninizi girin:",
        yükseklik=150,
        placeholder="Örnek: Market 250 TL, akşam yemeği 180 TL, taksi 50 TL"
    )
    
    sütun1, sütun2 = st.sütunlar(2)
    col1 ile:
        analyze_btn = st.button("📊 Analiz Et", type="primary", use_container_width=True)
    col2 ile:
        Eğer st.button("🔄 Temizle", use_container_width=True ise):
            st.rerun()
    
    eğer analyze_btn ve expense_text mevcutsa:
        with st.spinner("🤖AI harcamalarınızı analiz ediyor..."):
            denemek:
                # Öncelikle doğrudan yapay zeka analizini deneyin (Streamlit Cloud için)
                AI_AVAILABLE ise:
                    sonuç = gideri yapay zeka ile analiz et (gider metni)
                    
                    Eğer sonuçta 'hata' yoksa:
                        st.oturum_durumu.analiz_sonucu = sonuç
                        st.success("✅ Analiz tamamlandı!")
                    başka:
                        st.error(f"❌ {result['error']}")
                başka:
                    # Arka uç API'sine geri dönüş
                    yanıt = istekler.post(
                        f"{API_URL}/analiz",
                        json={"text": expense_text, "provider": "groq"},
                        zaman aşımı=30
                    )
                    
                    Eğer response.status_code == 200 ise:
                        sonuç = yanıt.json()
                        st.oturum_durumu.analiz_sonucu = sonuç
                        
                        # Veritabanına kaydet
                        Eğer sonuç 'masrafları' alırsa:
                            save_expenses_to_db(result['expenses'])
                        
                        st.success("✅ Analiz tamamlandı ve veri tabanı kaydedildi!")
                    başka:
                        st.error("❌ Analiz hatası.")
                    
            e istisnası hariç:
                st.error(f"❌ Hata: {str(e)}")
    
    # Sonuçları göster (öncekiyle aynı)
    Eğer 'analysis_result' st.session_state içindeyse:
        sonuç = st.oturum_durumu.analiz_sonucu
        
        Eğer sonuç 'masrafları' alırsa:
            giderler_veri çerçevesi = pd.DataFrame(sonuç['giderler'])
            
            # Metrikler
            sütun1, sütun2, sütun3, sütun4 = st.sütunlar(4)
            toplam_tutar = toplam(e['tutar'] for e in sonuç['giderler'])
            
            col1 ile:
                st.metric("Toplam", f"₺{total_amount:.2f}")
            col2 ile:
                st.metric("İşlem", f"{len(result['expenses'])}")
            col3 ile:
                st.metric("Ortalama", f"₺{total_amount/len(result['expenses']):.2f}")
            col4 ile:
                st.metric("Kategori", f"{len(set(e['category'] for e in result['expenses']))}")
            
            # Görselleştirmeler
            sütun1, sütun2 = st.sütunlar(2)
            
            col1 ile:
                kategori_toplamları = giderler_df.gruplandırma('kategori')['miktar'].toplam().indeksi_sıfırla()
                fig_pie = px.pie(category_totals, values='amount', names='category',
                                title='📊 Kategori Dağılımı', delik=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            col2 ile:
                fig_bar = px.bar(category_totals.sort_values('amount', ascending=False),
                               x='kategori', y='miktar',
                               title='💰 Kategorilere Göre Harcama')
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Masa
            st.subheader("📋 Harcama Detayları")
            display_df = expenses_df.copy()
            display_df['amount'] = display_df['amount'].apply(lambda x: f"₺{x:.2f}")
            Eğer display_df.columns'da 'etiketler' varsa:
                display_df['tags'] = display_df['tags'].apply(
                    lambda x: ', '.join(x) if isinstance(x, list) else x
                )
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Özet ve öneriler
            sütun1, sütun2 = st.sütunlar(2)
            
            col1 ile:
                st.subheader("📝 Özet")
                st.info(result.get('summary', ''))
            
            col2 ile:
                st.subheader("💡 Tasarruf Önerileri")
                for i, tip in enumerate(result.get('suggestions', []), 1):
                    st.markdown(f"""
                        <div class="stat-box">
                            <strong>{i}.</strong> {tip}
                        </div>
                    """, unsafe_allow_html=True)

elif "Gelir Takibi" st.session_state.page'de:
    st.title("💰 Gelir Takibi")
    
    tab1, tab2 = st.tabs(["➕Gelir Ekle", "📋Gelir Geçmişi"])
    
    tab1 ile:
        st.subheader("Yeni Gelir Ekle")
        
        sütun1, sütun2 = st.sütunlar(2)
        
        col1 ile:
            gelir_kaynak = st.text_input("Gelir Kaynağı", placeholder="Örn: Maaş, Freelance, Yatırım")
            gelir_miktarı = st.sayı_girişi("Tutar (₺)", min_değer=0.0, adım=100.0)
        
        col2 ile:
            gelir_tarihi = st.date_input("Tarih", değer=datetime.now())
            gelir_desc = st.text_area("Açıklama (Opsiyonel)", yükseklik=100)
        
        if st.button("💰 Gelir Ekle", type="primary", use_containing_width=True):
            Eğer gelir kaynağı ve gelir miktarı 0'dan büyükse:
                denemek:
                    yanıt = istekler.post(
                        f"{API_URL}/gelir",
                        json={
                            "kaynak": gelir_kaynağı,
                            "miktar": gelir_miktarı,
                            "açıklama": gelir_açıklaması,
                            "tarih": gelir_tarihi.strftime("%Y-%m-%d")
                        }
                    )
                    Eğer response.status_code == 200 ise:
                        st.success("✅ Gelir başarıyla eklendi!")
                        st.rerun()
                    başka:
                        st.error("❌ Gelir eklenirken hata oluştu.")
                e istisnası hariç:
                    st.error(f"❌ Hata: {str(e)}")
            başka:
                st.warning("⚠️ Lütfen tüm alanları doldurun.")
    
    tab2 ile:
        st.subheader("Gelir Geçmişi")
        
        denemek:
            yanıt = istekler.al(
                f"{API_URL}/gelir",
                parametreler={
                    "başlangıç_tarihi": st.oturum_durumu.başlangıç_tarihi,
                    "bitiş_tarihi": st.oturum_durumu.bitiş_tarihi
                }
            )
            
            Eğer response.status_code == 200 ise:
                gelir_listesi = yanıt.json()['gelir']
                
                eğer gelir listesi:
                    Toplam_gelir = toplam(i['miktar'] for i in gelir_listesi)
                    
                    sütun1, sütun2, sütun3 = st.sütunlar(3)
                    col1 ile:
                        st.metric("Toplam Gelir", f"₺{total_income:.2f}")
                    col2 ile:
                        st.metric("Gelir Sayısı", len(gelir_listesi))
                    col3 ile:
                        st.metric("Ortalama", f"₺{total_income/len(income_list):.2f}")
                    
                    # Gelir tablosu
                    df_income = pd.DataFrame(income_list)
                    df_income['amount'] = df_income['amount'].apply(lambda x: f"₺{x:.2f}")
                    st.dataframe(df_income[['date', 'source', 'amount', 'description']],
                               use_container_width=True, hide_index=True)
                    
                    # Gelir grafiği
                    df_chart = pd.DataFrame(income_list)
                    fig = px.bar(df_chart, x='date', y='amount', color='source',
                               başlık='Gelir Grafiği')
                    st.plotly_chart(fig, use_container_width=True)
                başka:
                    st.info("📭 Henüz gelir kaydı yok.")
        e istisnası hariç:
            st.error(f"❌ Hata: {str(e)}")

elif "Bütçe Yönetimi" st.session_state.page'de:
    st.title("🎯 Bütçe Yönetimi")
    
    tab1, tab2, tab3 = st.tabs(["➕ Bütçe Tablosu", "📊 Bütçe Durumu", "⚠️ Uyarılar"])
    
    tab1 ile:
        st.subheader("Yeni Bütçe Tablosu")
        
        sütun1, sütun2 = st.sütunlar(2)
        
        col1 ile:
            bütçe_kategorisi = st.seçim kutusu(
                "Kategori",
                ["Tümü", "Yemek & İçecek", "Ulaşım", "Alışveriş", "Eğlence",
                 "Konut", "Sağlık", "Eğitim", "Kişisel Bakım", "Seyahat", "Diğer"]
            )
            budget_amount = st.number_input("Bütçe Tutarı (₺)", min_value=0.0, step=100.0)
        
        col2 ile:
            bütçe_dönemi = st.selectbox("Dönem", ["aylık", "haftalık", "yıllık"])
            
            Eğer budget_period "monthly" ise:
                dönem_metni = "Aylık"
            elif budget_period == "weekly":
                dönem_metni = "Haftalık"
            başka:
                dönem_metni = "Yıllık"
        
        Eğer st.button("💾 Kaydet", type="primary", use_container_width=True ise):
            Eğer bütçe_miktarı > 0 ise:
                denemek:
                    yanıt = istekler.post(
                        f"{API_URL}/bütçe",
                        json={
                            "kategori": Eğer budget_category == "Tümü" ise None, aksi halde budget_category,
                            "miktar": bütçe_miktarı,
                            "dönem": bütçe_dönemi
                        }
                    )
                    Eğer response.status_code == 200 ise:
                        st.success(f"✅ {period_text} bütçe başarıyla belirlendi!")
                        st.rerun()
                    başka:
                        st.error("❌ Bütçeler gösterilirken hata oluştu.")
                e istisnası hariç:
                    st.error(f"❌ Hata: {str(e)}")
            başka:
                st.warning("⚠️ Lütfen geçerli bir tutar girin.")
    
    tab2 ile:
        st.subheader("Bütçe Durumu")
        
        denemek:
            yanıt = requests.get(f"{API_URL}/budget")
            
            Eğer response.status_code == 200 ise:
                bütçeler = yanıt.json()['bütçeler']
                
                bütçeler söz konusuysa:
                    Bütçeler içindeki bütçeler için:
                        kedi = bütçe['kategori'] veya "Genel Bütçe"
                        
                        # Bu kategori için harcamaları öğrenin
                        giderler = giderleri getir(
                            başlangıç_tarihi=st.oturum_durumu.başlangıç_tarihi,
                            bitiş_tarihi=st.oturum_durumu.bitiş_tarihi,
                            kategori=bütçe['kategori']
                        )
                        
                        harcanan = toplam(e['miktar'] için giderler)
                        kalan = bütçe['miktar'] - harcanan
                        yüzde = (harcanan / bütçe['miktar'] * 100) eğer bütçe['miktar'] > 0 ise aksi halde 0
                        
                        st.markdown(f"### {cat}")
                        
                        sütun1, sütun2, sütun3 = st.sütunlar(3)
                        col1 ile:
                            st.metric("Bütçe", f"₺{budget['amount']:.2f}")
                        col2 ile:
                            st.metric("Harcanan", f"₺{spent:.2f}", f"{percentage:.1f}%")
                        col3 ile:
                            st.metric("Kalan", f"₺{remaining:.2f}")
                        
                        # İlerleme çubuğu
                        Yüzde 100 veya daha yüksekse:
                            st.error(f"🚨 Bütçe aşıldı! (%{yüzde:.1f})")
                        elif percentage >= 80:
                            st.warning(f"⚠️ Bütçenin %{percentage:.1f}'i kırdı")
                        başka:
                            st.success(f"✅ Bütçe içindesiniz (%{yüzde:.1f})")
                        
                        st.progress(min(percentage / 100, 1.0))
                        st.markdown("---")
                başka:
                    st.info("📭 Henüz bütçe belirlenmemiş.")
        e istisnası hariç:
            st.error(f"❌ Hata: {str(e)}")
    
    tab3 ile:
        st.subheader("Bütçe Uyarıları")
        
        denemek:
            yanıt = requests.get(f"{API_URL}/budget/check")
            
            Eğer response.status_code == 200 ise:
                veri = yanıt.json()
                uyarılar = data.get('uyarılar', [])
                
                Eğer uyarılar varsa:
                    Uyarılar içindeki uyarılar için:
                        Eğer uyarı['durum'] 'aşıldı' ise:
                            st.markdown(f"""
                                <div class="danger-box">
                                    <h4>🚨 {uyarı['mesaj']}</h4>
                                    <p>Bütçe: ₺{uyarı['bütçe']:.2f} | Harcanan: ₺{uyarı['harcandı']:.2f</p>
                                    <p>Aşım: ₺{warning['spent'] - warning['budget']:.2f} (%{warning['percentage']:.1f})</p>
                                </div>
                            """, unsafe_allow_html=True)
                        başka:
                            st.markdown(f"""
                                <div class="warning-box">
                                    <h4>⚠️ {uyarı['mesaj']}</h4>
                                    <p>Bütçe: ₺{uyarı['bütçe']:.2f} | Harcanan: ₺{uyarı['harcandı']:.2f</p>
                                    <p>Kalan: ₺{warning['budget'] - warning['spent']:.2f}</p>
                                </div>
                            """, unsafe_allow_html=True)
                başka:
                    st.success("✅ Tüm bütçeler kontrol altında!")
        e istisnası hariç:
            st.error(f"❌ Hata: {str(e)}")

st.session_state.page'de elif "Hedefler":
    st.title("🎯 Tasarruf Hedefleri")
    
    tab1, tab2 = st.tabs(["➕ Hedef Ekle", "📊 Hedeflerim"])
    
    tab1 ile:
        st.subheader("Yeni Hedef Belirle")
        
        sütun1, sütun2 = st.sütunlar(2)
        
        col1 ile:
            gol_title = st.text_input("Hedef Adı", placeholder = "Örn: Tatil, Araba, Ev")
            hedef_miktarı = st.sayı_girişi("Hedef Tutar (₺)", min_değer=0.0, adım=1000.0)
        
        col2 ile:
            hedef_son_tarih = st.date_input("Hedef Tarihi", değer=datetime.now() + timedelta(gün=365))
        
        Eğer st.button("🎯 Hedef Ekle", type="primary", use_contain_width=True ise):
            Eğer hedef_başlığı ve hedef_miktarı 0'dan büyükse:
                denemek:
                    yanıt = istekler.post(
                        f"{API_URL}/hedefler",
                        json={
                            "başlık": hedef_başlığı,
                            "hedef_miktar": amaç_miktarı,
                            "son tarih": hedef_son_tarih.strftime("%Y-%m-%d")
                        }
                    )
                    Eğer response.status_code == 200 ise:
                        st.success("✅Hedef başarıyla eklendi!")
                        st.rerun()
                    başka:
                        st.error("❌ Hedef eklenirken hata oluştu.")
                e istisnası hariç:
                    st.error(f"❌ Hata: {str(e)}")
            başka:
                st.warning("⚠️ Lütfen tüm alanları doldurun.")
    
    tab2 ile:
        st.subheader("Aktif Hedefler")
        
        denemek:
            yanıt = istekler.get(f"{API_URL}/hedefler")
            
            Eğer response.status_code == 200 ise:
                hedefler = yanıt.json()['hedefler']
                
                Eğer hedefler:
                    Hedefler içindeki hedef için:
                        Eğer hedef['durum'] 'aktif' ise:
                            ilerleme = (hedef['mevcut_miktar'] / hedef['hedef_miktar'] * 100) eğer hedef['hedef_miktar'] > 0 ise aksi halde 0
                            kalan = hedef['hedef_miktar'] - hedef['mevcut_miktar']
                            
                            st.markdown(f"### 🎯 {goal['title']}")
                            
                            sütun1, sütun2, sütun3 = st.sütunlar(3)
                            col1 ile:
                                st.metric("Hedef", f"₺{goal['target_amount']:.2f}")
                            col2 ile:
                                st.metric("Biriken", f"₺{goal['current_amount']:.2f}", f"{progress:.1f}%")
                            col3 ile:
                                st.metric("Kalan", f"₺{remaining:.2f}")
                            
                            # İlerleme çubuğu
                            st.progress(min(progress / 100, 1.0))
                            
                            eğer hedef['son tarih'] ise:
                                son tarih = datetime.strptime(hedef['son tarih'], "%Y-%m-%d")
                                kalan_günler = (son tarih - tarih ve saat.şimdi()).günler
                                
                                Eğer kalan gün sayısı 0 ise:
                                    st.info(f"📅 Hedef zamanda {days_left} gün kaldı")
                                    
                                    # Gerekli aylık tasarrufları hesaplayın
                                    kalan_aylar = maksimum(kalan_günler / 30, 1)
                                    aylık_gereklilik = kalan / kalan_aylar
                                    st.info(f"💡 Hedefe ulaşmak için aylık ₺{monthly_required:.2f} biriktirmelisiniz")
                                başka:
                                    st.warning(f"⚠️ Hedef tarihi {abs(days_left)} gün önce geçti")
                            
                            st.markdown("---")
                başka:
                    st.info("📭 Henüz hedef belirlenmemiş.")
        e istisnası hariç:
            st.error(f"❌ Hata: {str(e)}")

elif "Düzenli Ödemeler" st.session_state.page'de:
    st.title("🔄 Düzenli Ödemeler")
    
    tab1, tab2 = st.tabs(["➕ Ödeme Ekle", "📋 Ödemelerim"])
    
    tab1 ile:
        st.subheader("Yeni Düzenli Ödeme Ekle")
        
        sütun1, sütun2 = st.sütunlar(2)
        
        col1 ile:
            ödeme_desc = st.text_input("Ödeme açıklaması", placeholder="Örn: Elektrik Faturası, Netflix")
            ödeme_kategorisi = st.seçim kutusu(
                "Kategori",
                ["Konut", "Eğlence", "Sağlık", "Eğitim", "Diğer"]
            )
            ödeme_miktarı = st.sayı_girişi("Tutar (₺)", min_değer=0.0, adım=50.0)
        
        col2 ile:
            ödeme_sıklığı = st.selectbox("Sıklık", ["aylık", "haftalık", "yıllık"])
            payment_due = st.date_input("Sonraki Ödeme Tarihi", value=datetime.now())
        
        if st.button("💾 Ödeme Ekle", type="primary", use_containing_width=True):
            Eğer payment_desc ve payment_amount 0'dan büyükse:
                denemek:
                    yanıt = istekler.post(
                        f"{API_URL}/tekrarlayan",
                        json={
                            "kategori": ödeme_kategorisi,
                            "miktar": ödeme_miktarı,
                            "açıklama": payment_desc,
                            "sıklık": ödeme_sıklığı,
                            "sonraki_vade_tarihi": ödeme_vadesi.strftime("%Y-%m-%d")
                        }
                    )
                    Eğer response.status_code == 200 ise:
                        st.success("✅ Düzenli ödeme başarıyla eklendi!")
                        st.rerun()
                    başka:
                        st.error("❌ Ödeme eklenirken hata oluştu.")
                e istisnası hariç:
                    st.error(f"❌ Hata: {str(e)}")
            başka:
                st.warning("⚠️ Lütfen tüm alanları doldurun.")
    
    tab2 ile:
        st.subheader("Düzenli Ödemeler")
        
        denemek:
            yanıt = istekler.get(f"{API_URL}/recurring")
            
            Eğer response.status_code == 200 ise:
                veri = yanıt.json()
                ödemeler = veri['ödemeler']
                yaklaşan = veri['yaklaşan']
                
                # Yaklaşan ödemeler
                Eğer yakında gelecekse:
                    st.markdown("### ⚠️ Yaklaşan Ödemeler")
                    Yakında yapılacak ödeme için:
                        günler = ödeme['günler_kadar']
                        
                        Eğer ödeme['gecikmişse']:
                            st.markdown(f"""
                                <div class="danger-box">
                                    <h4>🔴 {ödeme['açıklama']}</h4>
                                    <p>Tutar: ₺{ödeme['tutar']:.2f} | {abs(days)} gün gecikmiş</p>
                                    <p>Kategori: {payment['category']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        başka:
                            st.markdown(f"""
                                <div class="warning-box">
                                    <h4>🟡 {ödeme['açıklama']}</h4>
                                    <p>Tutar: ₺{ödeme['tutar']:.2f} | {days} gün kaldı</p>
                                    <p>Kategori: {payment['category']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # Tüm ödemeler
                ödemeler söz konusuysa:
                    st.markdown("### 📋 Tüm Düzenli Ödemeler")
                    
                    Toplam_aylık = toplam(p['miktar'] için p in ödemeler eğer p['sıklık'] == 'aylık')
                    
                    sütun1, sütun2 = st.sütunlar(2)
                    col1 ile:
                        st.metric("Toplam Aylık Ödeme", f"₺{total_monthly:.2f}")
                    col2 ile:
                        st.metric("Ödeme Sayısı", len(ödemeler))
                    
                    df_ödemeler = pd.DataFrame(ödemeler)
                    df_payments['amount'] = df_payments['amount'].apply(lambda x: f"₺{x:.2f}")
                    st.veri çerçevesi(
                        df_ödemeler[['açıklama', 'kategori', 'miktar', 'sıklık', 'sonraki_vade_tarihi']],
                        use_container_width=True,
                        hide_index=True
                    )
                başka:
                    st.info("📭 Henüz düzenli ödeme eklenmemiştir.")
        e istisnası hariç:
            st.error(f"❌ Hata: {str(e)}")

st.session_state.page'de elif "Raporlar":
    st.title("📈 Raporlar ve Analizler")
    
    # İstatistikleri al
    denemek:
        yanıt = istekler.al(
            f"{API_URL}/istatistikler",
            parametreler={
                "başlangıç_tarihi": st.oturum_durumu.başlangıç_tarihi,
                "bitiş_tarihi": st.oturum_durumu.bitiş_tarihi
            }
        )
        
        Eğer response.status_code == 200 ise:
            istatistikler = yanıt.json()
            
            # Özet kartları
            sütun1, sütun2, sütun3, sütun4 = st.sütunlar(4)
            
            col1 ile:
                st.metric("Toplam Harcama", f"₺{stats['total_expenses']:.2f}")
            col2 ile:
                st.metric("Toplam Gelir", f"₺{stats['total_income']:.2f}")
            col3 ile:
                denge_delta = istatistikler['denge']
                st.metric("Net Bakiye", f"₺{balance_delta:.2f}")
            col4 ile:
                st.metric("Ortalama Harcama", f"₺{stats['average_expense']:.2f}")
            
            st.markdown("---")
            
            # Detaylı grafikler
            Eğer istatistikler ['kategori_ayrıntısı'] ise:
                sütun1, sütun2 = st.sütunlar(2)
                
                col1 ile:
                    # Kategori pasta grafiği
                    df_cat = pd.DataFrame(
                        liste(istatistikler['kategori_ayrıntısı'].öğeler()),
                        sütunlar=['Kategori', 'Tutar']
                    )
                    fig_pie = px.pie(
                        df_cat,
                        değerler='Tutar',
                        isimler='Kategori',
                        title='Kategori Dağılımı',
                        delik=0.4
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                col2 ile:
                    # Kategori çubuk grafiği
                    fig_bar = px.bar(
                        df_cat.sort_values('Tutar', ascending=False),
                        x='Kategori',
                        y='Tutar',
                        title='Kategorilere Göre Harcama',
                        renk='Tutar',
                        renk_sürekli_ölçek='Kırmızılar'
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # Zaman serisi
            giderler = giderleri getir(
                başlangıç_tarihi=st.oturum_durumu.başlangıç_tarihi,
                bitiş_tarihi=geçmiş.oturum_durumu.bitiş_tarihi
            )
            
            Eğer masraflar:
                df_masraflar = pd.DataFrame(masraflar)
                df_expenses['date'] = pd.to_datetime(df_expenses['date'])
                
                # Günlük harcamalar
                günlük_harcama = df_harcamalar.gruplandırma('tarih')['miktar'].toplam().indeksi_sıfırla()
                
                fig_line = px.line(
                    günlük_harcama,
                    x='tarih',
                    y='miktar',
                    title='Günlük Harcama Trendi',
                    etiketler={'tarih': 'Tarih', 'miktar': 'Tutar (₺)'}
                )
                st.plotly_chart(fig_line, use_container_width=True)
                
                # Zaman içinde kategori
                kategori_zamanı = df_harcamalar.gruplandırma(['tarih', 'kategori'])['miktar'].toplam().indeksi_sıfırla()
                
                fig_area = px.area(
                    kategori_zamanı,
                    x='tarih',
                    y='miktar',
                    renk='kategori',
                    title='Kategorilere Göre Zaman Serisi'
                )
                st.plotly_chart(fig_area, use_container_width=True)
            
            # Dışa aktarma seçenekleri
            st.markdown("---")
            st.subheader("📥 Rapor İndir")
            
            sütun1, sütun2, sütun3 = st.sütunlar(3)
            
            col1 ile:
                Eğer masraflar:
                    df_export = pd.DataFrame(harcamalar)
                    csv = df_export.to_csv(index=False).encode('utf-8')
                    st.indirme_düğmesi(
                        etiket="📄 CSV İndir",
                        veri=csv,
                        dosya_adı=f"harcamalar_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            col2 ile:
                Eğer masraflar:
                    excel_buffer = BytesIO()
                    df_export.to_excel(excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)
                    
                    st.indirme_düğmesi(
                        etiket="📊 Excel İndir",
                        veri=excel_arabelleği,
                        dosya_adı=f"harcamalar_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            
            col3 ile:
                st.button("📑 PDF Rapor (Yakında)", disabled=True, use_container_width=True)
    
    e istisnası hariç:
        st.error(f"❌ Hata: {str(e)}")

st.session_state.page'de elif "Ayarlar":
    st.title("⚙️ Ayarlar")
    
    st.subheader("🗄️ Veritabanı Yönetimi")
    
    sütun1, sütun2 = st.sütunlar(2)
    
    col1 ile:
        if st.button("🗑️ Tüm Verileri Sil", type="ikincil", use_container_width=True):
            st.warning("⚠️ Bu işlemi geri alınamaz!")
            if st.checkbox("Eminim, tüm verileri silmek istiyorum"):
                st.error("Bu özellik henüz aktif değil.")
    
    col2 ile:
        if st.button("💾 Veritabanını Yedekle", use_container_width=True):
            st.info("💡 Yedekleme özelliği yakında eklenecek.")
    
    st.markdown("---")
    
    st.subheader("📊 İstatistikler")
    
    denemek:
        giderler = giderleri_getir()
        yanıt = istekler.get(f"{API_URL}/gelir")
        gelir_listesi = yanıt.json()['gelir'] eğer yanıt.durum_kodu == 200 ise aksi halde []
        
        sütun1, sütun2, sütun3 = st.sütunlar(3)
        
        col1 ile:
            st.metric("Toplam Harcama Kaydı", len(giderler))
        col2 ile:
            st.metric("Toplam Gelir Kaydı", len(income_list))
        col3 ile:
            Toplam_kayıtlar = len(giderler) + len(gelir_listesi)
            st.metric("Toplam Kayıt", total_records)
    
    hariç:
        geçmek
    
    st.markdown("---")
    
    st.subheader("ℹ️ Hakkında")
    st.info("""
    **AI Finans Asistanı Pro v2.0**
    
    Yapay zeka destekli kişisel finans yönetim uygulaması.
    
    Özellikler:
    - 🤖 AI destekli harcama analizi
    - 💰 Gelir ve gider takibi
    - 🎯 Tarım yönetimi
    - 📊 Detaylı raporlar ve tablolar
    - 🔄 Düzenli ödeme takibi
    - 🎯 Tasarruf Hedefleri
    
    Groq AI (Llama 3.3) tarafından desteklenmektedir.
    "")


# Altbilgi
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em; padding: 1rem;'>
    💰 AI Finans Asistanı Pro v2.0 | Groq AI tarafından desteklenmektedir
</div>
""", unsafe_allow_html=True)
