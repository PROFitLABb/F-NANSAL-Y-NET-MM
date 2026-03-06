import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# Page config
st.set_page_config(
    page_title="AI Finans Asistanı Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main {padding: 0rem 1rem;}
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {background-color: #45a049;}
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
        color: #000000;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 10px 0;
    }
    .danger-box {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Ana Sayfa'
if 'all_expenses' not in st.session_state:
    st.session_state.all_expenses = []

# Sidebar Navigation
with st.sidebar:
    st.title("💰 Finans Asistanı Pro")
    st.markdown("---")
    
    page = st.radio(
        "Menü",
        ["🏠 Ana Sayfa", "📊 Dashboard", "💸 Harcama Analizi", "💰 Gelir Takibi", 
         "🎯 Bütçe Yönetimi", "🎯 Hedefler", "🔄 Düzenli Ödemeler", 
         "📈 Raporlar", "⚙️ Ayarlar"],
        key="navigation"
    )
    st.session_state.page = page
    
    st.markdown("---")
    st.markdown("### 📅 Hızlı Filtreler")
    
    date_filter = st.selectbox(
        "Tarih Aralığı",
        ["Bu Ay", "Geçen Ay", "Son 3 Ay", "Son 6 Ay", "Bu Yıl", "Özel Tarih"]
    )
    
    if date_filter == "Özel Tarih":
        start_date = st.date_input("Başlangıç")
        end_date = st.date_input("Bitiş")
    else:
        today = datetime.now()
        if date_filter == "Bu Ay":
            start_date = today.replace(day=1)
            end_date = today
        elif date_filter == "Geçen Ay":
            end_date = today.replace(day=1) - timedelta(days=1)
            start_date = end_date.replace(day=1)
        elif date_filter == "Son 3 Ay":
            start_date = today - timedelta(days=90)
            end_date = today
        elif date_filter == "Son 6 Ay":
            start_date = today - timedelta(days=180)
            end_date = today
        elif date_filter == "Bu Yıl":
            start_date = today.replace(month=1, day=1)
            end_date = today
    
    st.session_state.start_date = start_date.strftime("%Y-%m-%d")
    st.session_state.end_date = end_date.strftime("%Y-%m-%d")

# Helper functions
def fetch_dashboard_data():
    try:
        response = requests.get(f"{API_URL}/dashboard")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def fetch_expenses(start_date=None, end_date=None, category=None):
    try:
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if category:
            params['category'] = category
        
        response = requests.get(f"{API_URL}/expenses", params=params)
        if response.status_code == 200:
            return response.json()['expenses']
    except:
        pass
    return []

def save_expenses_to_db(expenses):
    try:
        response = requests.post(f"{API_URL}/expenses/save", json=expenses)
        return response.status_code == 200
    except:
        return False

# Page routing
if "Ana Sayfa" in st.session_state.page:
    st.title("🏠 Ana Sayfa")
    st.markdown("### Hoş Geldiniz! AI Destekli Kişisel Finans Asistanınız")
    
    # Quick stats
    dashboard_data = fetch_dashboard_data()
    
    if dashboard_data:
        current = dashboard_data['current_month']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>₺{current['total_expenses']:.2f}</h3>
                    <p>Bu Ay Harcama</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>₺{current['total_income']:.2f}</h3>
                    <p>Bu Ay Gelir</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            balance_color = "#28a745" if current['balance'] >= 0 else "#dc3545"
            st.markdown(f"""
                <div class="metric-card" style="background: {balance_color};">
                    <h3>₺{current['balance']:.2f}</h3>
                    <p>Bakiye</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>{current['expense_count']}</h3>
                    <p>İşlem Sayısı</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Warnings
        if dashboard_data['budget_warnings']:
            st.subheader("⚠️ Bütçe Uyarıları")
            for warning in dashboard_data['budget_warnings']:
                if warning['status'] == 'exceeded':
                    st.markdown(f"""
                        <div class="danger-box">
                            <strong>🚨 {warning['message']}</strong><br>
                            Bütçe: ₺{warning['budget']:.2f} | Harcanan: ₺{warning['spent']:.2f}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="warning-box">
                            <strong>⚠️ {warning['message']}</strong><br>
                            Bütçe: ₺{warning['budget']:.2f} | Harcanan: ₺{warning['spent']:.2f}
                        </div>
                    """, unsafe_allow_html=True)
        
        # Upcoming payments
        if dashboard_data['upcoming_payments']:
            st.subheader("📅 Yaklaşan Ödemeler")
            for payment in dashboard_data['upcoming_payments']:
                days = payment['days_until']
                if payment['is_overdue']:
                    st.markdown(f"""
                        <div class="danger-box">
                            <strong>🔴 {payment['description']}</strong><br>
                            Tutar: ₺{payment['amount']:.2f} | {abs(days)} gün gecikmiş
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="warning-box">
                            <strong>🟡 {payment['description']}</strong><br>
                            Tutar: ₺{payment['amount']:.2f} | {days} gün kaldı
                        </div>
                    """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Hızlı İşlemler")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💸 Harcama Ekle", use_container_width=True):
            st.session_state.page = "💸 Harcama Analizi"
            st.rerun()
    
    with col2:
        if st.button("💰 Gelir Ekle", use_container_width=True):
            st.session_state.page = "💰 Gelir Takibi"
            st.rerun()
    
    with col3:
        if st.button("📊 Rapor Görüntüle", use_container_width=True):
            st.session_state.page = "📈 Raporlar"
            st.rerun()

elif "Dashboard" in st.session_state.page:
    st.title("📊 Dashboard")
    
    dashboard_data = fetch_dashboard_data()
    
    if dashboard_data:
        current = dashboard_data['current_month']
        last_month = dashboard_data['last_month']
        
        # Comparison metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            expense_change = ((current['total_expenses'] - last_month['total_expenses']) / 
                            last_month['total_expenses'] * 100) if last_month['total_expenses'] > 0 else 0
            st.metric(
                "Bu Ay Harcama",
                f"₺{current['total_expenses']:.2f}",
                f"{expense_change:+.1f}%"
            )
        
        with col2:
            income_change = ((current['total_income'] - last_month['total_income']) / 
                           last_month['total_income'] * 100) if last_month['total_income'] > 0 else 0
            st.metric(
                "Bu Ay Gelir",
                f"₺{current['total_income']:.2f}",
                f"{income_change:+.1f}%"
            )
        
        with col3:
            st.metric(
                "Bakiye",
                f"₺{current['balance']:.2f}",
                f"₺{current['balance'] - last_month['balance']:+.2f}"
            )
        
        # Category breakdown
        if current['category_breakdown']:
            st.subheader("📊 Kategori Dağılımı")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                df_cat = pd.DataFrame(list(current['category_breakdown'].items()), 
                                     columns=['Kategori', 'Tutar'])
                fig_pie = px.pie(df_cat, values='Tutar', names='Kategori',
                                title='Harcama Dağılımı', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                fig_bar = px.bar(df_cat.sort_values('Tutar', ascending=False),
                               x='Kategori', y='Tutar',
                               title='Kategorilere Göre Harcama')
                st.plotly_chart(fig_bar, use_container_width=True)

elif "Harcama Analizi" in st.session_state.page:
    st.title("💸 Harcama Analizi")
    
    # Expense input
    expense_text = st.text_area(
        "Harcama metninizi girin:",
        height=150,
        placeholder="Örnek: Market 250 TL, akşam yemeği 180 TL, taksi 50 TL"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        analyze_btn = st.button("📊 Analiz Et", type="primary", use_container_width=True)
    with col2:
        if st.button("🔄 Temizle", use_container_width=True):
            st.rerun()
    
    if analyze_btn and expense_text:
        with st.spinner("🤖 AI harcamalarınızı analiz ediyor..."):
            try:
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={"text": expense_text, "provider": "groq"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.analysis_result = result
                    
                    # Save to database
                    if result.get('expenses'):
                        save_expenses_to_db(result['expenses'])
                    
                    st.success("✅ Analiz tamamlandı ve veritabanına kaydedildi!")
                else:
                    st.error("❌ Analiz hatası.")
                    
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")
    
    # Show results (same as before)
    if 'analysis_result' in st.session_state:
        result = st.session_state.analysis_result
        
        if result.get('expenses'):
            expenses_df = pd.DataFrame(result['expenses'])
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            total_amount = sum(e['amount'] for e in result['expenses'])
            
            with col1:
                st.metric("Toplam", f"₺{total_amount:.2f}")
            with col2:
                st.metric("İşlem", f"{len(result['expenses'])}")
            with col3:
                st.metric("Ortalama", f"₺{total_amount/len(result['expenses']):.2f}")
            with col4:
                st.metric("Kategori", f"{len(set(e['category'] for e in result['expenses']))}")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                category_totals = expenses_df.groupby('category')['amount'].sum().reset_index()
                fig_pie = px.pie(category_totals, values='amount', names='category',
                                title='📊 Kategori Dağılımı', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_bar = px.bar(category_totals.sort_values('amount', ascending=False),
                               x='category', y='amount',
                               title='💰 Kategorilere Göre Harcama')
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Table
            st.subheader("📋 Harcama Detayları")
            display_df = expenses_df.copy()
            display_df['amount'] = display_df['amount'].apply(lambda x: f"₺{x:.2f}")
            if 'tags' in display_df.columns:
                display_df['tags'] = display_df['tags'].apply(
                    lambda x: ', '.join(x) if isinstance(x, list) else x
                )
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Summary and suggestions
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Özet")
                st.info(result.get('summary', ''))
            
            with col2:
                st.subheader("💡 Tasarruf Önerileri")
                for i, tip in enumerate(result.get('suggestions', []), 1):
                    st.markdown(f"""
                        <div class="stat-box">
                            <strong>{i}.</strong> {tip}
                        </div>
                    """, unsafe_allow_html=True)

elif "Gelir Takibi" in st.session_state.page:
    st.title("💰 Gelir Takibi")
    
    tab1, tab2 = st.tabs(["➕ Gelir Ekle", "📋 Gelir Geçmişi"])
    
    with tab1:
        st.subheader("Yeni Gelir Ekle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            income_source = st.text_input("Gelir Kaynağı", placeholder="Örn: Maaş, Freelance, Yatırım")
            income_amount = st.number_input("Tutar (₺)", min_value=0.0, step=100.0)
        
        with col2:
            income_date = st.date_input("Tarih", value=datetime.now())
            income_desc = st.text_area("Açıklama (Opsiyonel)", height=100)
        
        if st.button("💰 Gelir Ekle", type="primary", use_container_width=True):
            if income_source and income_amount > 0:
                try:
                    response = requests.post(
                        f"{API_URL}/income",
                        json={
                            "source": income_source,
                            "amount": income_amount,
                            "description": income_desc,
                            "date": income_date.strftime("%Y-%m-%d")
                        }
                    )
                    if response.status_code == 200:
                        st.success("✅ Gelir başarıyla eklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Gelir eklenirken hata oluştu.")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
            else:
                st.warning("⚠️ Lütfen tüm alanları doldurun.")
    
    with tab2:
        st.subheader("Gelir Geçmişi")
        
        try:
            response = requests.get(
                f"{API_URL}/income",
                params={
                    "start_date": st.session_state.start_date,
                    "end_date": st.session_state.end_date
                }
            )
            
            if response.status_code == 200:
                income_list = response.json()['income']
                
                if income_list:
                    total_income = sum(i['amount'] for i in income_list)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Toplam Gelir", f"₺{total_income:.2f}")
                    with col2:
                        st.metric("Gelir Sayısı", len(income_list))
                    with col3:
                        st.metric("Ortalama", f"₺{total_income/len(income_list):.2f}")
                    
                    # Income table
                    df_income = pd.DataFrame(income_list)
                    df_income['amount'] = df_income['amount'].apply(lambda x: f"₺{x:.2f}")
                    st.dataframe(df_income[['date', 'source', 'amount', 'description']], 
                               use_container_width=True, hide_index=True)
                    
                    # Income chart
                    df_chart = pd.DataFrame(income_list)
                    fig = px.bar(df_chart, x='date', y='amount', color='source',
                               title='Gelir Grafiği')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📭 Henüz gelir kaydı yok.")
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")

elif "Bütçe Yönetimi" in st.session_state.page:
    st.title("🎯 Bütçe Yönetimi")
    
    tab1, tab2, tab3 = st.tabs(["➕ Bütçe Belirle", "📊 Bütçe Durumu", "⚠️ Uyarılar"])
    
    with tab1:
        st.subheader("Yeni Bütçe Belirle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            budget_category = st.selectbox(
                "Kategori",
                ["Tümü", "Yemek & İçecek", "Ulaşım", "Alışveriş", "Eğlence", 
                 "Konut", "Sağlık", "Eğitim", "Kişisel Bakım", "Seyahat", "Diğer"]
            )
            budget_amount = st.number_input("Bütçe Tutarı (₺)", min_value=0.0, step=100.0)
        
        with col2:
            budget_period = st.selectbox("Periyot", ["monthly", "weekly", "yearly"])
            
            if budget_period == "monthly":
                period_text = "Aylık"
            elif budget_period == "weekly":
                period_text = "Haftalık"
            else:
                period_text = "Yıllık"
        
        if st.button("💾 Bütçe Kaydet", type="primary", use_container_width=True):
            if budget_amount > 0:
                try:
                    response = requests.post(
                        f"{API_URL}/budget",
                        json={
                            "category": None if budget_category == "Tümü" else budget_category,
                            "amount": budget_amount,
                            "period": budget_period
                        }
                    )
                    if response.status_code == 200:
                        st.success(f"✅ {period_text} bütçe başarıyla belirlendi!")
                        st.rerun()
                    else:
                        st.error("❌ Bütçe kaydedilirken hata oluştu.")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
            else:
                st.warning("⚠️ Lütfen geçerli bir tutar girin.")
    
    with tab2:
        st.subheader("Bütçe Durumu")
        
        try:
            response = requests.get(f"{API_URL}/budget")
            
            if response.status_code == 200:
                budgets = response.json()['budgets']
                
                if budgets:
                    for budget in budgets:
                        cat = budget['category'] or "Genel Bütçe"
                        
                        # Get spending for this category
                        expenses = fetch_expenses(
                            start_date=st.session_state.start_date,
                            end_date=st.session_state.end_date,
                            category=budget['category']
                        )
                        
                        spent = sum(e['amount'] for e in expenses)
                        remaining = budget['amount'] - spent
                        percentage = (spent / budget['amount'] * 100) if budget['amount'] > 0 else 0
                        
                        st.markdown(f"### {cat}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Bütçe", f"₺{budget['amount']:.2f}")
                        with col2:
                            st.metric("Harcanan", f"₺{spent:.2f}", f"{percentage:.1f}%")
                        with col3:
                            st.metric("Kalan", f"₺{remaining:.2f}")
                        
                        # Progress bar
                        if percentage >= 100:
                            st.error(f"🚨 Bütçe aşıldı! (%{percentage:.1f})")
                        elif percentage >= 80:
                            st.warning(f"⚠️ Bütçenin %{percentage:.1f}'i kullanıldı")
                        else:
                            st.success(f"✅ Bütçe içindesiniz (%{percentage:.1f})")
                        
                        st.progress(min(percentage / 100, 1.0))
                        st.markdown("---")
                else:
                    st.info("📭 Henüz bütçe belirlenmemiş.")
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
    
    with tab3:
        st.subheader("Bütçe Uyarıları")
        
        try:
            response = requests.get(f"{API_URL}/budget/check")
            
            if response.status_code == 200:
                data = response.json()
                warnings = data.get('warnings', [])
                
                if warnings:
                    for warning in warnings:
                        if warning['status'] == 'exceeded':
                            st.markdown(f"""
                                <div class="danger-box">
                                    <h4>🚨 {warning['message']}</h4>
                                    <p>Bütçe: ₺{warning['budget']:.2f} | Harcanan: ₺{warning['spent']:.2f}</p>
                                    <p>Aşım: ₺{warning['spent'] - warning['budget']:.2f} (%{warning['percentage']:.1f})</p>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="warning-box">
                                    <h4>⚠️ {warning['message']}</h4>
                                    <p>Bütçe: ₺{warning['budget']:.2f} | Harcanan: ₺{warning['spent']:.2f}</p>
                                    <p>Kalan: ₺{warning['budget'] - warning['spent']:.2f}</p>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.success("✅ Tüm bütçeler kontrol altında!")
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")

elif "Hedefler" in st.session_state.page:
    st.title("🎯 Tasarruf Hedefleri")
    
    tab1, tab2 = st.tabs(["➕ Hedef Ekle", "📊 Hedeflerim"])
    
    with tab1:
        st.subheader("Yeni Hedef Belirle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            goal_title = st.text_input("Hedef Adı", placeholder="Örn: Tatil, Araba, Ev")
            goal_amount = st.number_input("Hedef Tutar (₺)", min_value=0.0, step=1000.0)
        
        with col2:
            goal_deadline = st.date_input("Hedef Tarihi", value=datetime.now() + timedelta(days=365))
        
        if st.button("🎯 Hedef Ekle", type="primary", use_container_width=True):
            if goal_title and goal_amount > 0:
                try:
                    response = requests.post(
                        f"{API_URL}/goals",
                        json={
                            "title": goal_title,
                            "target_amount": goal_amount,
                            "deadline": goal_deadline.strftime("%Y-%m-%d")
                        }
                    )
                    if response.status_code == 200:
                        st.success("✅ Hedef başarıyla eklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Hedef eklenirken hata oluştu.")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
            else:
                st.warning("⚠️ Lütfen tüm alanları doldurun.")
    
    with tab2:
        st.subheader("Aktif Hedefler")
        
        try:
            response = requests.get(f"{API_URL}/goals")
            
            if response.status_code == 200:
                goals = response.json()['goals']
                
                if goals:
                    for goal in goals:
                        if goal['status'] == 'active':
                            progress = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
                            remaining = goal['target_amount'] - goal['current_amount']
                            
                            st.markdown(f"### 🎯 {goal['title']}")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Hedef", f"₺{goal['target_amount']:.2f}")
                            with col2:
                                st.metric("Biriken", f"₺{goal['current_amount']:.2f}", f"{progress:.1f}%")
                            with col3:
                                st.metric("Kalan", f"₺{remaining:.2f}")
                            
                            # Progress bar
                            st.progress(min(progress / 100, 1.0))
                            
                            if goal['deadline']:
                                deadline = datetime.strptime(goal['deadline'], "%Y-%m-%d")
                                days_left = (deadline - datetime.now()).days
                                
                                if days_left > 0:
                                    st.info(f"📅 Hedef tarihine {days_left} gün kaldı")
                                    
                                    # Calculate required monthly savings
                                    months_left = max(days_left / 30, 1)
                                    monthly_required = remaining / months_left
                                    st.info(f"💡 Hedefe ulaşmak için aylık ₺{monthly_required:.2f} biriktirmelisiniz")
                                else:
                                    st.warning(f"⚠️ Hedef tarihi {abs(days_left)} gün önce geçti")
                            
                            st.markdown("---")
                else:
                    st.info("📭 Henüz hedef belirlenmemiş.")
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")

elif "Düzenli Ödemeler" in st.session_state.page:
    st.title("🔄 Düzenli Ödemeler")
    
    tab1, tab2 = st.tabs(["➕ Ödeme Ekle", "📋 Ödemelerim"])
    
    with tab1:
        st.subheader("Yeni Düzenli Ödeme Ekle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            payment_desc = st.text_input("Ödeme Açıklaması", placeholder="Örn: Elektrik Faturası, Netflix")
            payment_category = st.selectbox(
                "Kategori",
                ["Konut", "Eğlence", "Sağlık", "Eğitim", "Diğer"]
            )
            payment_amount = st.number_input("Tutar (₺)", min_value=0.0, step=50.0)
        
        with col2:
            payment_frequency = st.selectbox("Sıklık", ["monthly", "weekly", "yearly"])
            payment_due = st.date_input("Sonraki Ödeme Tarihi", value=datetime.now())
        
        if st.button("💾 Ödeme Ekle", type="primary", use_container_width=True):
            if payment_desc and payment_amount > 0:
                try:
                    response = requests.post(
                        f"{API_URL}/recurring",
                        json={
                            "category": payment_category,
                            "amount": payment_amount,
                            "description": payment_desc,
                            "frequency": payment_frequency,
                            "next_due_date": payment_due.strftime("%Y-%m-%d")
                        }
                    )
                    if response.status_code == 200:
                        st.success("✅ Düzenli ödeme başarıyla eklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Ödeme eklenirken hata oluştu.")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
            else:
                st.warning("⚠️ Lütfen tüm alanları doldurun.")
    
    with tab2:
        st.subheader("Düzenli Ödemeler")
        
        try:
            response = requests.get(f"{API_URL}/recurring")
            
            if response.status_code == 200:
                data = response.json()
                payments = data['payments']
                upcoming = data['upcoming']
                
                # Upcoming payments
                if upcoming:
                    st.markdown("### ⚠️ Yaklaşan Ödemeler")
                    for payment in upcoming:
                        days = payment['days_until']
                        
                        if payment['is_overdue']:
                            st.markdown(f"""
                                <div class="danger-box">
                                    <h4>🔴 {payment['description']}</h4>
                                    <p>Tutar: ₺{payment['amount']:.2f} | {abs(days)} gün gecikmiş</p>
                                    <p>Kategori: {payment['category']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="warning-box">
                                    <h4>🟡 {payment['description']}</h4>
                                    <p>Tutar: ₺{payment['amount']:.2f} | {days} gün kaldı</p>
                                    <p>Kategori: {payment['category']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # All payments
                if payments:
                    st.markdown("### 📋 Tüm Düzenli Ödemeler")
                    
                    total_monthly = sum(p['amount'] for p in payments if p['frequency'] == 'monthly')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Toplam Aylık Ödeme", f"₺{total_monthly:.2f}")
                    with col2:
                        st.metric("Ödeme Sayısı", len(payments))
                    
                    df_payments = pd.DataFrame(payments)
                    df_payments['amount'] = df_payments['amount'].apply(lambda x: f"₺{x:.2f}")
                    st.dataframe(
                        df_payments[['description', 'category', 'amount', 'frequency', 'next_due_date']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("📭 Henüz düzenli ödeme eklenmemiş.")
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")

elif "Raporlar" in st.session_state.page:
    st.title("📈 Raporlar ve Analizler")
    
    # Get statistics
    try:
        response = requests.get(
            f"{API_URL}/statistics",
            params={
                "start_date": st.session_state.start_date,
                "end_date": st.session_state.end_date
            }
        )
        
        if response.status_code == 200:
            stats = response.json()
            
            # Summary cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Toplam Harcama", f"₺{stats['total_expenses']:.2f}")
            with col2:
                st.metric("Toplam Gelir", f"₺{stats['total_income']:.2f}")
            with col3:
                balance_delta = stats['balance']
                st.metric("Net Bakiye", f"₺{balance_delta:.2f}")
            with col4:
                st.metric("Ortalama Harcama", f"₺{stats['average_expense']:.2f}")
            
            st.markdown("---")
            
            # Detailed charts
            if stats['category_breakdown']:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Category pie chart
                    df_cat = pd.DataFrame(
                        list(stats['category_breakdown'].items()),
                        columns=['Kategori', 'Tutar']
                    )
                    fig_pie = px.pie(
                        df_cat,
                        values='Tutar',
                        names='Kategori',
                        title='Kategori Dağılımı',
                        hole=0.4
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    # Category bar chart
                    fig_bar = px.bar(
                        df_cat.sort_values('Tutar', ascending=False),
                        x='Kategori',
                        y='Tutar',
                        title='Kategorilere Göre Harcama',
                        color='Tutar',
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # Time series
            expenses = fetch_expenses(
                start_date=st.session_state.start_date,
                end_date=st.session_state.end_date
            )
            
            if expenses:
                df_expenses = pd.DataFrame(expenses)
                df_expenses['date'] = pd.to_datetime(df_expenses['date'])
                
                # Daily spending
                daily_spending = df_expenses.groupby('date')['amount'].sum().reset_index()
                
                fig_line = px.line(
                    daily_spending,
                    x='date',
                    y='amount',
                    title='Günlük Harcama Trendi',
                    labels={'date': 'Tarih', 'amount': 'Tutar (₺)'}
                )
                st.plotly_chart(fig_line, use_container_width=True)
                
                # Category over time
                category_time = df_expenses.groupby(['date', 'category'])['amount'].sum().reset_index()
                
                fig_area = px.area(
                    category_time,
                    x='date',
                    y='amount',
                    color='category',
                    title='Kategorilere Göre Zaman Serisi'
                )
                st.plotly_chart(fig_area, use_container_width=True)
            
            # Export options
            st.markdown("---")
            st.subheader("📥 Rapor İndir")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if expenses:
                    df_export = pd.DataFrame(expenses)
                    csv = df_export.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📄 CSV İndir",
                        data=csv,
                        file_name=f"harcamalar_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with col2:
                if expenses:
                    excel_buffer = BytesIO()
                    df_export.to_excel(excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label="📊 Excel İndir",
                        data=excel_buffer,
                        file_name=f"harcamalar_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            
            with col3:
                st.button("📑 PDF Rapor (Yakında)", disabled=True, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Hata: {str(e)}")

elif "Ayarlar" in st.session_state.page:
    st.title("⚙️ Ayarlar")
    
    st.subheader("🗄️ Veritabanı Yönetimi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Tüm Verileri Sil", type="secondary", use_container_width=True):
            st.warning("⚠️ Bu işlem geri alınamaz!")
            if st.checkbox("Eminim, tüm verileri silmek istiyorum"):
                st.error("Bu özellik henüz aktif değil.")
    
    with col2:
        if st.button("💾 Veritabanını Yedekle", use_container_width=True):
            st.info("💡 Yedekleme özelliği yakında eklenecek.")
    
    st.markdown("---")
    
    st.subheader("📊 İstatistikler")
    
    try:
        expenses = fetch_expenses()
        response = requests.get(f"{API_URL}/income")
        income_list = response.json()['income'] if response.status_code == 200 else []
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Toplam Harcama Kaydı", len(expenses))
        with col2:
            st.metric("Toplam Gelir Kaydı", len(income_list))
        with col3:
            total_records = len(expenses) + len(income_list)
            st.metric("Toplam Kayıt", total_records)
    
    except:
        pass
    
    st.markdown("---")
    
    st.subheader("ℹ️ Hakkında")
    st.info("""
    **AI Finans Asistanı Pro v2.0**
    
    Yapay zeka destekli kişisel finans yönetim uygulaması.
    
    Özellikler:
    - 🤖 AI destekli harcama analizi
    - 💰 Gelir ve gider takibi
    - 🎯 Bütçe yönetimi
    - 📊 Detaylı raporlar ve grafikler
    - 🔄 Düzenli ödeme takibi
    - 🎯 Tasarruf hedefleri
    
    Powered by Groq AI (Llama 3.3)
    """)


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em; padding: 1rem;'>
    💰 AI Finans Asistanı Pro v2.0 | Powered by Groq AI
</div>
""", unsafe_allow_html=True)
