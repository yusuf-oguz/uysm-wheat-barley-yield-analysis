# UYSM — Buğday/Arpa Verim Tahmini: Saha Verisi Analizi

TARBİL (Tarımsal İzleme ve Bilgi Sistemi) kapsamında toplanan Türkiye geneli buğday/arpa saha ölçüm verisinin işlenmesi ve analizi. İTÜ'de staj (2026 bahar) sürecinde başlayıp, staj sonrasında bağımsız olarak genişletilerek devam ettirilmiş bir çalışma.

**Bu repo private tutuluyor.** Veri, TARBİL/İTÜ UHUZAM ve proje yürütücülerinin (Necmettin Türkoğlu, Serdar Bağış) sahada topladığı kurumsal saha verisidir — kullanıcının kendi ürettiği bir veri değildir. Bu nedenle, verinin/metodolojinin yayın izni netleşmeden repo public yapılmıyor.

---

## İki Aşama

Çalışma kronolojik olarak iki aşamadan oluşuyor:

### `01_ilk_pipeline/` — Staj döneminde yapılan ilk çalışma

291 saha ölçüm Excel dosyasından (`UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA/`), analiz için hazır tek bir CSV üreten 14 adımlık ETL pipeline'ı. 239 kayıt analize dahil edilebilir kalitede. Detaylar için → [`01_ilk_pipeline/README.md`](01_ilk_pipeline/README.md).

**Bu klasör, İTÜ staj raporunun (bkz. `Staj1` projesi) anlattığı çalışmanın karşılığıdır** — ancak rapor bu çalışmanın yalnızca ilk yarısını kapsar; asıl devamı aşağıdaki `02_genisletilmis_analiz/`'de.

### `02_genisletilmis_analiz/` — Staj sonrası bağımsız devam çalışması

Kaynak veri 291 dosyadan **769+291 dosyaya (Hansay + eski VERİM 3 seti, 264'ü örtüşen)** genişletildi — 79 il, ~800 benzersiz saha ölçümü. Pipeline artık iteratif (`hansay_processed_v1` → `v8.2`, ~90 ara versiyon). Üzerine **7 kategoride gerçek istatistiksel analiz** eklendi: tanımlayıcı istatistik, il bazlı coğrafi dağılım, ölçüm-alanı etkisi, başak morfolojisi, verim bileşen analizi, sap boyu ilişkisi, enlem/boylam korelasyonu (Spearman, Kruskal-Wallis, Bland-Altman testleri dahil).

Ana bulgular özeti → [`02_genisletilmis_analiz/output/ANALIZ_OZET.md`](02_genisletilmis_analiz/output/ANALIZ_OZET.md)
Ham verinin (88 GB flash bellek dökümü) tam envanteri → [`02_genisletilmis_analiz/docs/DURUM_RAPORU[eski].md`](<02_genisletilmis_analiz/docs/DURUM_RAPORU[eski].md>)

---

## Ham Veri Notu

Bu repo yalnızca **kod, dokümantasyon ve pipeline'dan geçmiş ara/işlenmiş veriyi** içerir. Aşağıdakiler repoya dahil değildir:

- **88 GB'lık ham flash bellek dökümü** (`uysm_flash_bellek_degistirilmemis/`) — saha fotoğrafları, İTÜ UHUZAM uydu sınıflandırma shapefile'ları, TARBİL'in resmi verim raporları. Salt okunur kaynak olarak yerelde tutuluyor, harici diske yedeklenecek.
- **2 akademik referans PDF** (`ekstra_kaynaklar/`) — Springer kitap bölümü (Üstündağ, KLR modeli) ve TARBİL agro-meteoroloji makalesi. Telif hakkı olan üçüncü taraf yayın; kaynakça olarak burada anılıyor, dosya olarak dahil edilmiyor.

## Bilinen Fazlalık Dosyalar (silinmedi, disk alanı gerekirse silinebilir)

İki dosya, yanlarındaki klasörlerin **byte-birebir doğrulanmış** (diff ile kontrol edildi) tam yedek kopyası — hiçbir ek bilgi taşımıyorlar, sadece disk yeri kaplıyorlar:

1. `UYSM_PROJECTS/UYSM_Project_2/yusuf_oguz_calismalari.zip` (30 MB) — bu repo'nun `02_genisletilmis_analiz/` klasörünün eski bir zip yedeği (repo'nun bir üst dizininde, dışında duruyor).
2. `01_ilk_pipeline/data/processed/Koordinati Hatali Veriler.zip` (~500 KB) — yanındaki `Koordinati Hatali Veriler/` klasörünün zip yedeği.

Her ikisi de `.gitignore` ile bu repodan hariç tutuldu (versiyon kontrolüne gerek yok), ama diskten silinmedi.

## Path Uyarısı

Her iki aşamadaki scriptler (`scripts/pipeline/`, `scripts/inspect/`), o an çalıştırıldıkları ortama özgü **sabit (absolute) Windows yolları** içeriyor (`D:\_Development\Projects\...`). Bunlar tek seferlik çalıştırılmış analiz/ETL scriptleri olduğu için olduğu gibi bırakıldı — projeyi yeniden çalıştırmak isteyen biri (veya ileride kendisi) önce bu sabit yolları güncellemeli. Kod, üretilen pipeline mantığını ve analiz metodolojisini göstermek amacıyla burada; birebir yeniden-çalıştırılabilirlik hedeflenmedi.

## Kullanılan Araçlar

Python — `pandas`, `openpyxl`, `geopandas`/`shapely` (coğrafi doğrulama), `folium` (interaktif harita), `matplotlib`/`seaborn` (grafikler), `scipy` (istatistiksel testler).
