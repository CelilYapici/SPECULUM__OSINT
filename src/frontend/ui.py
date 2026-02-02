import streamlit as st

class SpeculumUI:
    """
    Speculum projesinin arayüz, tasarım (CSS) ve form elemanlarını yöneten sınıf.
    """
    
    @staticmethod
    def setup_page():
        """Sayfa başlığı, ikon ve CSS ayarlarını yükler."""
        st.set_page_config(
            page_title="SPECULUM | OSINT Tool",
            page_icon="🛡️",
            layout="centered"
        )
        
        # Özel CSS - Dark Mode, Neon Mavisi ve Siber Güvenlik Teması
        st.markdown("""
            <style>
            /* Ana arka plan */
            .main { background-color: #0e1117; }
            
            /* Başlık stili */
            h1 { 
                color: #00d4ff; 
                text-align: center; 
                font-family: 'Courier New', monospace; 
                text-shadow: 0 0 10px #00d4ff;
            }
            
            /* Buton stili */
            .stButton>button {
                width: 100%; 
                background-color: #00d4ff; 
                color: #000;
                font-weight: bold; 
                border-radius: 5px; 
                border: none;
                transition: 0.3s;
            }
            .stButton>button:hover { 
                background-color: #0099cc; 
                color: white; 
                box-shadow: 0 0 15px #00d4ff;
            }
            
            /* Sonuç Kartları */
            .result-card {
                background-color: #1a1c24;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #00d4ff;
                margin-bottom: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            .result-title { 
                color: #fff; 
                font-size: 1.1em; 
                font-weight: bold; 
                margin-bottom: 5px;
            }
            .result-status { 
                color: #aaa; 
                font-size: 0.9em; 
                margin-bottom: 10px;
            }
            a { 
                color: #00d4ff; 
                text-decoration: none; 
                font-weight: bold;
            }
            a:hover { text-decoration: underline; }
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_header():
        """Logo, Başlık ve Slogan alanı."""
        st.title("S P E C U L U M")
        st.markdown("<div style='text-align: center; color: gray; margin-bottom: 30px; letter-spacing: 2px;'>DİJİTAL YANSIMANIZLA YÜZLEŞİN</div>", unsafe_allow_html=True)

    @staticmethod
    def render_form():
        """
        Kullanıcıdan veri alan formu oluşturur.
        Return: (Butona basıldı mı?, İsim, Email, Derin Tarama?)
        """
        with st.form("main_form"):
            st.write("### 🔍 Hedef Bilgileri")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("İsim Soyisim", placeholder="Örn: Ahmet Yılmaz")
            with col2:
                email = st.text_input("E-Posta Adresi", placeholder="Örn: ahmet@mail.com")
            
            st.markdown("---")
            st.write("### ⚙️ Tarama Ayarları")
            
            # Derin tarama açıklaması
            deep_scan = st.checkbox("Derin Tarama (Holehe Modu)", value=False)
            sherlock_scan = st.checkbox("Sherlock Taraması (kullanıcı adı bazlı)", value=False)
            harvester_scan = st.checkbox("theHarvester (domain/e-posta tabanlı)", value=False)
            spiderfoot_scan = st.checkbox("SpiderFoot (Geniş OSINT taraması)", value=False)
            if deep_scan:
                st.caption("⚠️ Derin tarama seçildiği için işlem biraz uzun sürecektir.")
            
            submitted = st.form_submit_button("ANALİZİ BAŞLAT")

            return submitted, name, email, deep_scan, sherlock_scan, harvester_scan, spiderfoot_scan

    @staticmethod
    def display_results(accounts, google_links):
        """Backend'den gelen sonuçları ekrana basar."""
        st.markdown("## 📊 Analiz Raporu")
        
        # 1. HESAPLAR BÖLÜMÜ
        if accounts:
            st.info(f"Toplam {len(accounts)} adet potansiyel hesap veya veri noktası tespit edildi.")
            for item in accounts:
                # Eğer Sherlock'dan ham çıktı geldiyse, bunu kod bloğu olarak göster
                if item.get('platform') == 'Sherlock' and item.get('raw'):
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">{item.get('platform')}</div>
                        <div class="result-status">{item.get('status')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(item.get('raw'))
                    continue

                # Eğer resim varsa resmi ve bilgiyi yan yana koy
                if item.get('image'):
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        st.image(item.get('image'), width=70)
                    with c2:
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-title">{item.get('platform')}</div>
                            <div class="result-status">{item.get('status')}</div>
                            <a href="{item.get('url')}" target="_blank">🔗 Profili İncele</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Resim yoksa sadece kart göster (url olmayabilir)
                    url_html = f'<a href="{item.get("url")}" target="_blank">🔗 Kaynağa Git</a>' if item.get('url') else ''
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">{item.get('platform')}</div>
                        <div class="result-status">{item.get('status')}</div>
                        {url_html}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("E-posta adresine bağlı belirgin bir hesap bulunamadı.")

        # 2. GOOGLE BÖLÜMÜ
        if google_links:
            st.markdown("### 🌍 Google İndeksleri")
            for link in google_links:
                st.markdown(f"- 🔗 [{link}]({link})")