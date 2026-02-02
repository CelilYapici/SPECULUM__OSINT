import time
import streamlit as st

# Modüllerimizi klasör yapısına göre içe aktarıyoruz
try:
    from src.frontend.ui import SpeculumUI
    from src.backend.engine import SpeculumEngine
except ImportError as e:
    st.error(f"⚠️ Kurulum Hatası: Modüller bulunamadı. Lütfen dosya yapısının doğru olduğundan emin olun.\nHata Detayı: {e}")
    st.stop()

def main():
    # 1. ARAYÜZÜ HAZIRLA
    # UI sınıfını başlat ve sayfayı çiz
    ui = SpeculumUI()
    ui.setup_page()
    ui.render_header()

    # 2. VERİLERİ AL
    # Formu göster ve kullanıcının girdiği verileri değişkenlere ata
    submitted, name, email, deep_scan, sherlock_scan, harvester_scan, spiderfoot_scan = ui.render_form()

    # 3. İŞLEM YAP (BUTONA BASILDIYSA)
    if submitted:
        # Basit bir doğrulama: İkisi de boşsa hata ver
        if not name and not email:
            st.error("❌ Hata: Lütfen analiz için en az bir bilgi (İsim veya E-posta) girin.")
            return

        # Motoru başlat
        engine = SpeculumEngine()

        # Yükleniyor ekranı (Progress bar ve durum bilgisi)
        # st.status Streamlit'in yeni ve şık yükleme çubuğudur
        with st.status("Speculum Motoru Çalışıyor...", expanded=True) as status:
            st.write("📡 Veri okyanusu taranıyor...")
            
            if deep_scan:
                st.write("🕵️ Derin tarama modu aktif (Bu işlem biraz zaman alabilir)...")
            
            # Backend'deki fonksiyonu çağır
            # Bu fonksiyon bize iki liste döndürecek: hesaplar ve google linkleri
            accounts, google_links = engine.run_full_scan(
                name,
                email,
                deep_scan,
                use_sherlock=sherlock_scan,
                use_theharvester=harvester_scan,
                use_spiderfoot=spiderfoot_scan
            )
            
            time.sleep(0.5) # Kullanıcı bitişi hissetsin diye ufak bekleme (UX)
            status.update(label="Analiz Tamamlandı!", state="complete", expanded=False)

        # 4. SONUÇLARI GÖSTER
        # UI sınıfına sonuçları gönder, o da ekrana bassın
        ui.display_results(accounts, google_links)

# Python dosyasının ana giriş noktası olduğunu belirtir
if __name__ == "__main__":
    main()