import hashlib
import requests
import subprocess
import shutil
from googlesearch import search
import json
import tempfile

class SpeculumEngine:
    """
    Speculum projesinin ana tarama motoru.
    Tüm OSINT (Açık Kaynak İstihbarat) işlemleri bu sınıf üzerinden yönetilir.
    """

    @staticmethod
    def _check_command_installed(cmd):
        """Yardımcı Fonksiyon: Gerekli araç (örn: holehe) bilgisayarda yüklü mü?"""
        return shutil.which(cmd) is not None

    @staticmethod
    def scan_gravatar(email):
        """E-posta adresinin Gravatar/WordPress profilini kontrol eder."""
        email = email.strip().lower()
        # Gravatar, e-postanın MD5 hash'i ile çalışır
        email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
        url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
        
        try:
            # 3 saniye zaman aşımı koyuyoruz ki sistem donmasın
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                return {
                    "platform": "Gravatar",
                    "status": "Profil Resmi Mevcut",
                    "url": f"https://www.gravatar.com/{email_hash}",
                    "image": url
                }
        except:
            pass
        return None

    @staticmethod
    def scan_github(email):
        """E-postadan kullanıcı adı türetip GitHub'ı kontrol eder."""
        # Örnek: ahmet@gmail.com -> ahmet
        username = email.split('@')[0]
        url = f"https://github.com/{username}"
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                return {
                    "platform": "GitHub",
                    "status": "Kullanıcı Adı Eşleşti",
                    "url": url,
                    "image": None # GitHub profil resmini çekmek için ekstra işlem gerekir, şimdilik boş.
                }
        except:
            pass
        return None

    @staticmethod
    def deep_scan_holehe(email):
        """
        Holehe aracını kullanarak 120+ sitede hesap kontrolü yapar.
        Bu işlem terminal komutunu arka planda çalıştırarak yapılır.
        """
        findings = []
        
        # Holehe yüklü değilse hata döndürmeden çık (Sistem çökmemesi için)
        if not SpeculumEngine._check_command_installed("holehe"):
            return [{"platform": "Sistem Uyarısı", "status": "Holehe kütüphanesi bulunamadı.", "url": "#", "image": None}]

        try:
            # Komutu çalıştır: holehe <email> --only-used --no-color
            # --only-used: Sadece bulunanları gösterir
            # --no-color: Renk kodlarını temizler, metni okumayı kolaylaştırır
            process = subprocess.Popen(
                ["holehe", email, "--only-used", "--no-color"],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            stdout, _ = process.communicate()

            # Çıktıyı satır satır analiz et
            for line in stdout.splitlines():
                # Holehe bulduğu siteleri '[+]' işaretiyle başlatır
                if "[+]" in line:
                    site = line.replace("[+]", "").strip()
                    findings.append({
                        "platform": site,
                        "status": "Hesap Tespit Edildi",
                        # Doğrudan link bulmak zor olduğu için Google aramasına yönlendiriyoruz
                        "url": f"https://google.com/search?q=site:{site} {email}",
                        "image": None
                    })
        except Exception as e:
            print(f"Holehe Hatası: {e}")
        
        return findings

    @staticmethod
    def deep_scan_sherlock(username):
        """
        Sherlock CLI aracını kullanarak kullanıcı adını birçok platformda arar.
        Çıktıyı ham metin olarak döndürürüz (parçalama yerine ham metni UI'da gösteriyoruz).
        """
        findings = []

        if not username:
            return findings

        if not SpeculumEngine._check_command_installed("sherlock"):
            return [{"platform": "Sherlock", "status": "Sherlock bulunamadı (yüklü değil)", "url": "#", "image": None}]

        try:
            process = subprocess.Popen(
                ["sherlock", username],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=120)

            # Döndüğümüz yapı, UI'da ham çıktıyı gösterebilmek için tek bir kayda koyuyor
            findings.append({
                "platform": "Sherlock",
                "status": "Çıktı (ham)",
                "url": None,
                "image": None,
                "raw": stdout if stdout else stderr
            })
        except Exception as e:
            findings.append({"platform": "Sherlock", "status": f"Hata: {e}", "url": "#", "image": None})

        return findings

    @staticmethod
    def deep_scan_theharvester(domain_or_email):
        """
        theHarvester CLI ile domain veya e-posta domain'i tarar.
        """
        findings = []
        if not domain_or_email:
            return findings

        if not SpeculumEngine._check_command_installed("theHarvester"):
            return [{"platform": "theHarvester", "status": "theHarvester bulunamadı (yüklü değil)", "url": "#", "image": None}]

        # If an email provided, extract domain
        target = domain_or_email
        if "@" in domain_or_email:
            target = domain_or_email.split('@')[1]

        try:
            process = subprocess.Popen([
                "theHarvester", "-d", target, "-b", "all"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=120)
            findings.append({
                "platform": "theHarvester",
                "status": "Çıktı (ham)",
                "url": None,
                "image": None,
                "raw": stdout if stdout else stderr
            })
        except Exception as e:
            findings.append({"platform": "theHarvester", "status": f"Hata: {e}", "url": "#", "image": None})

        return findings

    @staticmethod
    def deep_scan_spiderfoot(target):
        """
        SpiderFoot CLI wrapper — hedef olarak e-posta, domain veya IP alır.
        SpiderFoot büyük bir araçtır; burada sadece CLI çıktısını yakalayıp UI'ya döndürüyoruz.
        """
        findings = []
        if not target:
            return findings

        if not SpeculumEngine._check_command_installed("spiderfoot"):
            return [{"platform": "SpiderFoot", "status": "SpiderFoot bulunamadı (yüklü değil)", "url": "#", "image": None}]

        try:
            process = subprocess.Popen([
                "spiderfoot", "-s", target, "-o", "stdout"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=180)
            findings.append({
                "platform": "SpiderFoot",
                "status": "Çıktı (ham)",
                "url": None,
                "image": None,
                "raw": stdout if stdout else stderr
            })
        except Exception as e:
            findings.append({"platform": "SpiderFoot", "status": f"Hata: {e}", "url": "#", "image": None})

        return findings

    @staticmethod
    def search_google(name):
        """İsim Soyisim için Google Dorking araması yapar."""
        links = []
        if not name: return links
        
        try:
            query = f'"{name}"' # Tırnak içinde tam eşleşme arıyoruz
            # Türkçe sonuçlar öncelikli, 5 sonuç yeterli
            for url in search(query, num_results=5, lang="tr"):
                links.append(url)
        except:
            pass
            
        return links

    def run_full_scan(self, name, email, use_deep_scan=False, use_sherlock=False, use_theharvester=False, use_spiderfoot=False):
        """
        Bütün tarama fonksiyonlarını tek bir çatı altında sırasıyla çalıştırır.
        """
        results = []
        
        # 1. Hızlı Taramalar (Anlık - API bazlı)
        if email:
            gravatar = self.scan_gravatar(email)
            if gravatar: results.append(gravatar)
            
            github = self.scan_github(email)
            if github: results.append(github)

        # 2. Derin Taramalar (Holehe - Yavaş ama detaylı)
        if email and use_deep_scan:
            holehe_results = self.deep_scan_holehe(email)
            results.extend(holehe_results)

        # 2b. Sherlock taraması (kullanıcı adı bazlı) -- isteğe bağlı
        if use_sherlock:
            # Sherlock genelde kullanıcı adı ile çalışır; e-posta varsa yerel kısmı (before @) kullan
            username = None
            if email:
                username = email.split('@')[0]
            elif name:
                # isimden username çıkarımı garanti değil; bu bir fallback
                username = name.split()[0].lower()

            if username:
                sherlock_results = self.deep_scan_sherlock(username)
                results.extend(sherlock_results)

        # theHarvester (domain/e-posta domain'i üzerinden bilgi toplama)
        if use_theharvester:
            target = email if email else name
            harvester_results = self.deep_scan_theharvester(target)
            results.extend(harvester_results)

        # SpiderFoot (daha geniş OSINT taraması)
        if use_spiderfoot:
            target = email if email else name
            spider_results = self.deep_scan_spiderfoot(target)
            results.extend(spider_results)

        # 3. Google Taraması (İsim Soyisim)
        google_results = self.search_google(name)

        return results, google_results