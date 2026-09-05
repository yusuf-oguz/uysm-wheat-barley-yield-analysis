# processed/ — Dizin Yapısı

## Klasörler

### active/
Üzerinde aktif olarak çalışılan, kalıcı CSV dosyaları.
`vAnaliz1.0.csv` analiz için kullanılacak nihai dosyadır.

### archive/
Geri dönüş için saklanan kritik versiyonlar + superseded dosyalar.
Active ile aynı dosya olabilir — duplicate olmasında sorun yok, amaç güvenli kopyayı korumak.

| Dosya | Neden arşivde | Geri dönüş senaryosu |
|---|---|---|
| `hansay_ham_full.csv` | Ham veri, hiçbir değer değiştirilmemiş | Sıfırdan başlamak |
| `hansay_formuller.csv` | Excel formülleri referans | Formül kontrolü |
| `hansay_processed_v2.1.csv` | Buğday+arpa, belirsiz bitki adları çıkarılmış | Arpa analizine dönmek |
| `hansay_processed_v6.0.csv` | Outlier öncesi temiz başlangıç (639 satır, sadece buğday, vld_genel=True) | Outlier analizini baştan uygulamak |
| `hansay_processed_v7.3.csv` | b1-b10 seri içi+IQR sonrası, global MAD öncesi | Sadece klasik IQR analiziyle yetinmek |
| `hansay_processed_v7.9.csv` | Tüm global outlier sonrası, satır eleme öncesi | Farklı satır eleme kriterleri denemek |
| `hansay_processed_v8.1.csv` | null_sayisi≥25 elendi, C21+D21 null olanlar henüz tutulmuş | Verim null kararını değiştirmek |
| `hansay_processed_v8.2.csv` | Nihai işlenmiş veri, tüm False'lar işaretli (617 True) | False kararlarını gözden geçirmek |
| `vAnaliz1.0.csv` | Analiz verisi — False satırlar ve geçici sütunlar çıkarılmış | Referans kopya |
| `hansay_processed_v5.4.csv` | Eski outlier skor yaklaşımı (superseded) | — |
| `hansay_processed_v6.1–v6.4.csv` | Sap outlier ara versiyonları (superseded) | — |

### tmp/
İnceleme ve karşılaştırma scriptlerinin çıktıları. Geçici referans içindir;
tekrar üretilebilir, silinebilir.

| Dosya | Açıklama | Üreten Script |
|---|---|---|
| `baslik_tutarliligi.csv` | Etiket hücrelerinde dosyalar arası tutarsızlıklar | `scripts/inspect/check_baslik_tutarliligi.py` |
| `j15_25_dolu_dosyalar.csv` | J15–J25 aralığı dolu olan 6 dosyanın değerleri | `scripts/inspect/` |
| `kapsam_disi_hucreler.csv` | A1:M45 aralığında aktif CSV'ye alınmayan dolu hücreler (geniş format) | `scripts/inspect/check_kapsam_disi_hucreler.py` |
| `kapsam_disi_kontrol.csv` | Kapsam dışı hücre kontrolü (özet) | `scripts/inspect/check_kapsam_disi_hucreler.py` |
| `plaka_uyusmazlik.xlsx` | Dosya adı ile C6 istasyon kodu arasında il plakası uyuşmayan 19 kayıt | `scripts/inspect/kontrol_koordinat_il.py` (manuel) |
| `false6_inceleme.xlsx` | `il_uyusma == False` olan 6 kayıt — inceleme için | `scripts/inspect/kontrol_koordinat_il.py` (manuel) |
| `hansay_formuller_kalan.csv` | I5/I7 hücrelerindeki formül incelemesi — geçici referans | `scripts/inspect/` |
| `kmz_ham.xlsx` | KMZ'den çıkarılan ham nokta verisi | `scripts/inspect/` |

---

## Docs Belgeler Rehberi

| Dosya | Ne işe yarar |
|---|---|
| `docs/OUTLIER_ANALIZI.md` | Tüm outlier analizi metodolojisi, her aşamanın rakamları, akademik gerekçeler ve paper için İngilizce metodoloji metni |
| `docs/VERI_KAYIPLARI.md` | 769 ham dosyadan 617 analiz satırına giden süreçteki her satır/hücre kaybının hikayesi ve versiyonu. Bazı bilgiler hatalı olabilir — doğrulama için bu README'yi ve active/ altındaki versiyonları incele. |
| `docs/SUTUN_ONCELIK.md` | Ham ve türetilmiş sütunların katman sırası; outlier analiz sırasının özeti; vAnaliz1.0'da hangi sütunların kaldığı/çıkarıldığı |
| `docs/FORMUL_REFERANS.json` | Tüm türetilmiş sütun formülleri — 6 grup (A–F); v7.0'da mean(skipna=True) ile güncellendi |
| `docs/VERI_NOTLARI.md` | Yanıltıcı sütun adları, C21 vs D21 farkı, E13/E14 çarpan açıklaması, vAnaliz1.0'dan çıkarılan ara sütunlar |
| `docs/figures/` | 15 `line_*.png` (türetilmiş sütunlar) + 7 `b1b10_line_*.png` (ham b1-b10 dağılımı) — hepsi vAnaliz1.0 verisiyle güncel |

---

## İşleme Versiyonları

Ham veriden başlayarak her filtreleme/düzeltme adımı ayrı bir versiyonlu dosya olarak kaydedilir.
Bu sayede strateji değişikliği veya hata durumunda istenen adıma geri dönmek mümkün olur.

**İsimlendirme:** `hansay_processed_vN.csv` (N = versiyon numarası)

| Versiyon | Yapılan İşlem | Durum |
|---|---|---|
| `hansay_ham_full.csv` | Ham veri — hiçbir değer değiştirilmemiş | Tamamlandı |
| `hansay_processed_v1.csv` | `bitki_adi__C9` normalizasyonu — varyantlar `bugday` / `arpa` olarak birleştirildi | Tamamlandı |
| `hansay_processed_v2.1.csv` | Bitki filtresi — `bugday` ve `arpa` dışındaki belirsiz/geçersiz bitki adı satırları çıkarıldı; 769 → 730 satır (655 buğday + 75 arpa); arpa bu versiyonda hâlâ mevcut | Tamamlandı |
| `hansay_processed_v2.2.csv` | Koordinat format düzeltmesi — 5 dosyada yazım hatası giderildi (fazladan virgül, eksik `"`, sondaki boşluk) | Tamamlandı |
| `hansay_processed_v2.3.csv` | `0202 30 m 17.xlsx` boylam düzeltmesi — `38°20'5861"` → `38°20'58.61"` (ondalık nokta eksikliği) | Tamamlandı |
| `hansay_processed_v2.4.csv` | `2706 145.xlsx` boylam düzeltmesi — `36.53'21.12"` → `36°53'21.12"` (`°` yerine `.` yazılmış) | Tamamlandı |
| `hansay_processed_v2.5.csv` | `7003 3km 651.xlsx` ve `7005 20km 650.xlsx` koordinat düzeltmesi — ham değerler ondalık derece olarak yorumlanıp DMS'e çevrildi (**şüpheli**, teyit gerekli) | Tamamlandı |
| `hansay_processed_v2.6.csv` | `4213 istaston(b) 739.xlsx` koordinat düzeltmesi — `37557191`/`33983746` ondalık derece olarak yorumlandı → `37°33'25.89"`/`33°59'01.49"`, Konya il sınırlarıyla ve komşu kayıtlarla uyuşuyor | Tamamlandı |
| `hansay_processed_v2.7.csv` | Koordinat doğrulama — `enlem_dd`/`boylam_dd`, `turkiye_ici` (730/730 True), `il_plaka_adi`, `il_plaka_c6` (C6 hücresinden), `il_plaka_final` (3 dosyada C6 override: `195 30km 195.xlsx`, `3610 300m 403.xlsx`, `4006 aydınlar 465.xlsx`), `il_koordinat_adi` (GADM sjoin), `koordinat_ili_komsu` (GADM komşuluk matrisi), `il_uyusma` (True:675, komsu:49, False:6) sütunları eklendi | Tamamlandı |
| `hansay_processed_v2.8.csv` | KMZ entegrasyonu — `Yerlerim.kmz`'den 2105 nokta çekildi; her satır için `kmz_enlem_dd`, `kmz_boylam_dd`, `kmz_il`, `kmz_esleme` (tek/sira/coklu/yok) sütunları eklendi. `il_koordinat_final` (6 False satırdan 5'i KMZ'den düzeltildi), `il_uyusma_final` (True:680, komsu:49, False:1) güncellendi | Tamamlandı |
| `hansay_processed_v2.9.csv` | Koordinat final sütunları — `enlem_raw_final`, `boylam_raw_final`, `enlem_dd_final`, `boylam_dd_final` eklendi; 5 dosyada KMZ koordinatları kullanıldı, diğerlerinde ham veri | Tamamlandı |
| `hansay_processed_v2.10.csv` | Koordinat temizliği — ara/ham koordinat sütunları kaldırıldı; `koordinat_gecerli` (729 True, 1 False) ve `koordinat_gecersiz_neden` öne alındı; final koordinat ve il sütunları ilk sıralara taşındı (140 sütun) | Tamamlandı |
| `hansay_processed_v3.0.csv` | Sütun azaltma — analizde kullanılmayacak 16 sütun çıkarıldı (başlık, sulama, kamera, çeşit, fenolojik evre, bilinmeyen vb.); 140 → 124 sütun | Tamamlandı |
| `hansay_processed_v3.1.csv` | Sütun sıralama — 7 işlevsel gruba ayrıldı: kimlik → ana verim → başak/bitki özellikleri → toplam/ort+lab → 10 başak ham ölçümleri → düşük öncelik → koordinat | Tamamlandı |
| `hansay_processed_v3.2.csv` | Eksiklik sayım sütunları — 7 ölçüm tipi için (uzunluk, agirlik, dane_sayisi, dane_agirlik, sap_basak, sap_alt, sap_boy) b1–b10 arasında kaç tanesinin boş/0 olduğunu sayan 7 sütun eklendi; kimlik sütunlarının hemen ardına yerleştirildi | Tamamlandı |
| `hansay_processed_v3.3.csv` | sap_basak_boyu düzeltmesi — H=0 olan 120 hücre J-I formülüyle dolduruldu; eksik_sap_basak sayım sütunu güncellendi (120 → 0) | Tamamlandı |
| `hansay_processed_v3.4.csv` | Geçerlilik sütunları — `vld_` prefix sistemi kuruldu; `koordinat_gecerli` → `vld_koordinat`, `koordinat_gecersiz_neden` → `vld_genel_neden` olarak yeniden adlandırıldı; `vld_sap_alt` eklendi (sap_alt 10/10 eksik olan 1 satır False); tüm `vld_` sütunlarını birleştiren `vld_genel` eklendi (True:728, False:2); tüm `vld_` sütunları en sona taşındı | Tamamlandı |
| `hansay_processed_v3.5.csv` | sap_alt doldurma — `4801 700m 82.xlsx` ve `6315 183.xlsx` dosyalarındaki 1'er eksik sap_alt hücresi o verinin diğer 9 örneğinin ortalamasıyla dolduruldu (85.56 ve 78.11); `vld_genel` ve `vld_genel_neden` en başa taşındı | Tamamlandı |
| `hansay_processed_v3.6.csv` | agirlik doldurma — `0111 6.xlsx` dosyasındaki `b10_agirlik_mg__C38` (=0) diğer 9 örneğin ortalamasıyla dolduruldu (2239.89 mg); `eksik_agirlik` sütunu silindi | Tamamlandı |
| `hansay_processed_v3.7.csv` | dane_agirlik temizleme — 1-2 eksik olan 34 satırda eksik hücreler o verinin diğer başaklarının ortalamasıyla dolduruldu; 3+ eksik olan 2 satır (`4216 10km 622`, `4208 50m 594`) `vld_dane_agirlik=False` yapıldı; `vld_genel` güncellendi (True:726, False:4) | Tamamlandı |
| `hansay_processed_v3.8.csv` | dane_sayisi temizleme — 1-2 eksik olan 36 satırda eksik hücreler ortalamıyla dolduruldu; 3+ eksik olan 3 satır (`4216 10km 622`, `4208 50m 594`, `7008 611`) `vld_dane_sayisi=False` yapıldı; `vld_genel` güncellendi (True:725, False:5) | Tamamlandı |
| `hansay_processed_v3.9.csv` | Tutarsızlık tespiti — `vld_genel=True` olan 725 satır için J=H+I denklem kontrolü yapıldı (7250 işlem); tutarsız örnek sayısını gösteren `sap_boy_tutarsiz` sütunu eklendi | Tamamlandı |
| `hansay_processed_v3.10.csv` | sap_boy düzeltmeleri — `0201 3.xlsx`, `0203 4.xlsx`, `0205 5.xlsx` `vld_sap_boy=False` yapıldı (10/10 tutarsız); `3809 500m 514.xlsx` tüm J değerleri H+I'dan yeniden hesaplandı (satır kayması); `4801` ve `6315` tutarsız J hücreleri H+I ile düzeltildi; `sap_boy_tutarsiz` silindi; `vld_genel` güncellendi (True:722, False:8) | Tamamlandı |
| `hansay_processed_v3.11.csv` | H39/I39/J39 düzeltme — 33 satırda ortalama sap boy sütunları (H39, I39, J39) b1–b10 ham verilerinden yeniden hesaplandı; `sap_ort_tutarsiz` güncellendi (722/722 temiz); B39/B40 kontrolü için `uzunluk_tutarsiz` sütunu eklendi (1 satırda 2 hata) | Tamamlandı |
| `hansay_processed_v3.12.csv` | B39/B40 düzeltme — `0201 9.xlsx` B39/B40 yeniden hesaplandı; `sap_ort_tutarsiz` ve `uzunluk_tutarsiz` silindi; C39/C40 kontrolü için `agirlik_tutarsiz` eklendi (6 satırda C39,C40 tutarsız) | Tamamlandı |
| `hansay_processed_v3.13.csv` | C39/C40 düzeltme — 6 satır yeniden hesaplandı; `agirlik_tutarsiz` silindi; D39/D40 kontrolü için `dane_sayisi_tutarsiz` eklendi (36 satırda D39,D40 tutarsız) | Tamamlandı |
| `hansay_processed_v3.14.csv` | D39/D40 düzeltme — 36 satır yeniden hesaplandı; `dane_sayisi_tutarsiz` silindi; E39/E40 kontrolü için `dane_agirlik_tutarsiz` eklendi (37 satırda E39,E40 tutarsız) | Tamamlandı |
| `hansay_processed_v3.15.csv` | E39/E40 düzeltme — 37 satır yeniden hesaplandı; `dane_agirlik_tutarsiz` silindi; D41=E40/C40 kontrolü için `d41_tutarsiz` eklendi (43 satırda D41 tutarsız) | Tamamlandı |
| `hansay_processed_v3.16.csv` | D41 düzeltme — 43 satır yeniden hesaplandı; `d41_tutarsiz` silindi; E41=C41*D41 kontrolü için `e41_tutarsiz` eklendi (43 satırda E41 tutarsız) | Tamamlandı |
| `hansay_processed_v3.17.csv` | E41 düzeltme — 43 satır yeniden hesaplandı; `e41_tutarsiz` silindi; E42=E41*E14 kontrolü için `e42_tutarsiz` eklendi (43 satırda E42 tutarsız) | Tamamlandı |
| `hansay_processed_v3.18.csv` | E42 düzeltme — 43 satır yeniden hesaplandı; `e42_tutarsiz` silindi; tüm formül tutarsızlık kontrolleri tamamlandı | Tamamlandı |
| `hansay_processed_v3.19.csv` | J41 inceleme — `j41_tutarsiz` (61 satırda J41≠J25), `bilinmeyen__J25`, `on_sap_agirlik_mg__J41`, `j41_formul` sütunları başa alındı; `j41_formul` hansay_formuller.csv'den eşleştirilerek eklendi (`=J25`:329, `=J24`:246, boş:155) | Tamamlandı |
| `hansay_processed_v3.20.csv` | J41 düzeltme — 61 satırda `on_sap_agirlik_mg__J41` değeri `bilinmeyen__J25` ile güncellendi (formülsüz duplicate değer); j41_tutarsiz 722/722 temiz | Tamamlandı |
| `hansay_processed_v3.21.csv` | C16=J41 kontrolü — `j41_tutarsiz` silindi; `c16_tutarsiz` eklendi (61 satırda C16≠J41) | Tamamlandı |
| `hansay_processed_v3.22.csv` | C16 düzeltme — 61 satırda C16 J41 ile güncellendi (veri kopyalama problemi); `c16_tutarsiz` silindi; 722/722 temiz | Tamamlandı |
| `hansay_processed_v3.23.csv` | Etiket sütunları kaldırıldı — `olcum_birimi_etiketi__C3`, `olcum_alani_etiketi__A11`, `olcum_alani_etiketi__B41` çıkarıldı (hiçbir formülde kullanılmıyor, E13/E14 ile tutarsız); E13=E14 her satırda doğrulandı (4:137, 8:437, 16:156); 130 → 127 sütun | Tamamlandı |
| `hansay_processed_v3.24.csv` | C12=C11*E13 kontrolü — 40 satırda `m2_basak_sayisi__C12` sabit değer (30 veya 40) içeriyor, formül uygulanmamış; `c12_tutarsiz` sütunu eklendi | Tamamlandı |
| `hansay_processed_v3.25.csv` | C12 düzeltme — 40 satırda C12 = C11*E13 ile yeniden hesaplandı; `c12_tutarsiz` silindi; 722/722 temiz | Tamamlandı |
| `hansay_processed_v3.26.csv` | C14=C13*E14 kontrolü — 722/722 temiz, tutarsızlık yok; `c14_tutarsiz` eklendi (hepsi False) | Tamamlandı |
| `hansay_processed_v3.27.csv` | C15=C12+C14 kontrolü — aynı 40 satırda C15 sabit değer (30/40/70) içeriyor; `c15_tutarsiz` eklendi | Tamamlandı |
| `hansay_processed_v3.28.csv` | C15 düzeltme — 40 satırda C15 = C12+C14 ile yeniden hesaplandı; `c15_tutarsiz` silindi; 722/722 temiz | Tamamlandı |
| `hansay_processed_v3.29.csv` | C17=C16/10000*C12/1000 kontrolü — 85 satırda tutarsızlık tespit edildi; `c17_tutarsiz` eklendi, ilgili sütunlar başa alındı | Tamamlandı |
| `hansay_processed_v3.30.csv` | C17 düzeltme — 85 satırda C17 = C16/10000*C12/1000 ile yeniden hesaplandı; `c17_tutarsiz` silindi; 722/722 temiz | Tamamlandı |
| `hansay_processed_v3.31.csv` | C18=C40 kontrolü — 6 satırda tutarsızlık; `c18_tutarsiz` eklendi, ilgili sütunlar başa alındı | Tamamlandı |
| `hansay_processed_v3.32.csv` | C18 düzeltme — 6 satırda C18 = C40 ile güncellendi; `c18_tutarsiz` silindi; 722/722 temiz | Tamamlandı |
| `hansay_processed_v3.33.csv` | Referans kopyalar kontrolü — C19=D40 (36 tutarsız), C20=E40/1000 (29 tutarsız), C23=J39 (4 tutarsız), C24=B40 (1 tutarsız); ilgili sütunlar ve `_tutarsiz` flagleri başa alındı | Tamamlandı |
| `hansay_processed_v3.34.csv` | Referans kopyalar düzeltme — C19=D40 (36), C20=E40/1000 (29), C23=J39 (4), C24=B40 (1) güncellendi; tüm `_tutarsiz` flagleri silindi; 722/722 temiz | Tamamlandı |
| `hansay_processed_v3.35.csv` | Temizlik ve sıralama — `c14_tutarsiz`, `j41_formul` silindi; `bilinmeyen__J24/J25` yeniden adlandırıldı; sütunlar işlevsel gruplara göre yeniden sıralandı (kimlik→vld→koordinat→alan→verim→başak özellikleri→lab→toplam→b1–b10); 128 → 126 sütun | Tamamlandı |
| `hansay_processed_v4.0.csv` | Sütun adı revizyonu — 9 sütun yeniden adlandırıldı: birim düzeltmeleri (`C18`: gram→mg), açıklayıcı isimler (`C16`, `C20`), copy sistemi (`C19`→`_copy`, `C23`→`_copy`, `C24`→`_copy`), alan çarpanı standardizasyonu (`E14`→`carpani2`), birim ekleme (`B40`, `J39`→`_cm`) | Tamamlandı |
| `hansay_processed_v4.1.csv` | C21=C20*C12 kontrolü ve düzeltme — 30 satırda tutarsızlık (C20 daha önce güncellenmiş, C21 yeniden hesaplanmamıştı; 1 satırda `/1000` fazladan); `c21_tutarsiz` eklendi, ilgili sütunlar başa alındı; 722/722 temiz | Tamamlandı |
| `hansay_processed_v4.2.csv` | D21=E42/1000 kontrolü — 43 satırda tutarsızlık; `d21_tutarsiz` eklendi, ilgili sütunlar başa alındı | Tamamlandı |
| `hansay_processed_v4.3.csv` | D21 düzeltme — 43 satırda D21 = E42/1000 ile yeniden hesaplandı; `d21_tutarsiz` silindi; 722/722 temiz | Tamamlandı |
| `hansay_processed_v4.4.csv` | C22=E40/D40 kontrolü ve düzeltme — 11 satırda tutarsızlık; yeniden hesaplandı; 722/722 temiz | Tamamlandı |
| `hansay_processed_v4.5.csv` | I5=C6 karşılaştırması — 35 satırda `sehir_istasyon__I5` ≠ `istasyon_no__C6`; `i5_c6_farki` etiket sütunu eklendi, ilgili sütunlar başa alındı | Tamamlandı |
| `hansay_processed_v4.6.csv` | Temizlik ve sıralama — `i5_c6_farki`, `c21_tutarsiz` silindi; `sehir_istasyon__I5` → `istasyon_no_alt__I5` olarak yeniden adlandırıldı; sütunlar yeniden sıralandı; 128 → 126 sütun | Tamamlandı |
| `hansay_processed_v4.7.csv` | Null/zero analizi ve düzeltmeler — (1) `ort_sap_basak_boyu__H39` 117 satırda b1–b10 ortalamasından yeniden hesaplandı (pipeline eksikliği); (2) `ort_kilcikli_basak_agirlik_mg__C18` 2 satır, `ort_dane_sayisi_copy__C19` 1 satır kaynak sütundan güncellendi; (3) `6305 140.xlsx` (idx=603) `vld_genel=False` yapıldı (C41 lab tartımı hiç girilmemiş, D21 güvenilmez); (4) `basaksiz_bitki_sayisi__C13` 4 satır null → 0; vld_genel: True=721, False=9 | Tamamlandı |
| `hansay_processed_v4.8.csv` | `sulama_tipi__G6` ve `fenolojik_evre__G9` ham veriden geri eklendi (bitki_adi'ndan sonra); sulama_tipi normalize edildi (KURU/kuru → kuru, 0 → NaN); 126 → 128 sütun | Tamamlandı |
| `hansay_processed_v4.9.csv` | Son formül kontrolü (vld_genel=True 721 satır) — Grup A–F tüm formüller doğrulandı; 3 tutarsızlık giderildi: (1) `bir_basaktaki_ort_dane_agirlik_gram__C20` 8 satır yeniden hesaplandı (E40 daha önce güncellenmişti, C20 kalmıştı); (2) `bin_dane_agirlik_gram__C22` 7 satır yeniden hesaplandı (aynı nedenle); (3) `m2_sap_agirlik_kg__C17` 11 satır yeniden hesaplandı (Excel'de C16 yanlış sabit değerle hesaplanmıştı); zincirleme olarak `dane_m2_hesap_gram__C21` 8 satır güncellendi | Tamamlandı |
| `hansay_processed_v5.0.csv` | Sütun temizliği — 24 sütun çıkarıldı, 128 → 104 sütun. **Grup 1 (tekrar/eşdeğer):** `istasyon_no_alt__I5`, `rapor_no_xlsx__J3`, `olcum_alani_carpani2__E14`, `ort_kilcikli_basak_agirlik_mg__C18`, `ort_dane_sayisi_copy__C19`, `ort_sap_boy_cm_copy__C23`, `ort_basak_uzunluk_cm_copy__C24`, `on_basak_sap_agirlik_ham__J24`, `on_basak_sap_agirlik_sum__J25`. **Grup 2 (ara hesap):** `dane_m2_tartim_hesap__E42`, `olcum_basak_dane_agirlik_hesap__E41`, `toplam_basak_uzunluk__B39`, `toplam_basak_agirlik_mg__C39`, `toplam_dane_sayisi__D39`, `toplam_dane_agirlik_mg__E39`, `on_sap_agirlik_mg__J41`, `on_basaktaki_toplam_sap_agirlik_mg__C16`. **Grup 3 (seçilen):** `vld_koordinat`, `vld_sap_alt`, `vld_dane_agirlik`, `vld_dane_sayisi`, `vld_sap_boy`, `enlem_raw_final`, `boylam_raw_final`. Çıkarılan tüm sütunlar `hansay_cikarilan_sutunlar.csv`'ye eklendi (45 sütun) | Tamamlandı |
| `hansay_processed_v5.1.csv` | Kopyalanmış veri tespiti ve `kismi_not` sütunu — b1–b10 sap ölçümlerinin tümünün aynı olduğu 10 satır tespit edildi; `sap_basak_boyu` (10), `sap_alt_cm` (9), `sap_boy_cm` (9) sütunları null yapıldı; türetilmiş `H39`/`I39`/`J39` ortalamaları da null yapıldı; `kismi_not` sütunu eklendi (vld_genel_neden'den hemen sonra) — kısmen güvenilmez sütunları açıklar, vld_genel=True kalır; 104 → 105 sütun | Tamamlandı |
| `hansay_processed_v5.2.csv` | Satır düzeyinde kopya tespiti — 74 ham ölçüm sütunu üzerinden karşılaştırma; 5 kopya çifti bulundu; her çiftten orijinal belirlendi, kopya olan `vld_genel=False` yapıldı: `0109 50m 352` (5106 orijinal), `0614 350 668` (669 orijinal), `3602 250m 796` (736 orijinal), `8001 13` (6310 orijinal), `6804 istasyon(a) 560` (561 orijinal); vld_genel: True=716, False=14 | Tamamlandı |
| `hansay_processed_v5.3.csv` | Kopya tespiti devamı — b1-b10 70 sütun üzerinden karşılaştırma; 5 yeni kopya çifti bulundu: `3103 741` (2714 orijinal), `4203 istasyon kendi parseli 588` (4011 orijinal), `7008 5km148` (7002 orijinal) → vld_genel=False; `3503 2km 68` ve `3503 69` çifti başta geçerli sanıldı (C11/C41 farklı) ancak 10 başağın tüm ölçümlerinin birebir aynı olması istatistiksel olarak imkânsız olduğundan ikisi de False yapıldı; `6408 792` kısmen kopya (uzunluk/ağırlık/dane b1-b10 kopyalanmış, sap farklı) → null + kismi_not; vld_genel: True=711, False=19; kismi_not dolu=10 | Tamamlandı |
| `hansay_processed_v6.0.csv` | Çalışma seti — `vld_genel=True` ve `bitki_adi=bugday` filtresi uygulandı; 730 → 639 satır (arpa 75 + False 19 çıkarıldı); 105 sütun; outlier analizi bu versiyon üzerinden yürütüldü | Tamamlandı |
| `hansay_processed_v6.5.csv` | 3 sap sütunu (sap_basak_boyu/sap_alt/sap_boy) için sistematik outlier analizi — her sütun için 2 tur (p1/p99 → MAD>10 → log-IQR 3x); 30 satırda kismi_not güncellendi; swap (3 dosya), null (toplam ~25 hücre), H39/I39/J39 `mean(skipna=True)` ile güncellendi; 105 sütun | Tamamlandı |
| `hansay_processed_v6.6.csv` | uzunluk_cm outlier analizi (2 tur) — 8 hücre null (1546, 86, 85, 76, 65, 56.5, 35, 1.1 cm kesin hatalar); B40 ve C24 `mean(skipna=True)` ile güncellendi | Tamamlandı |
| `hansay_processed_v6.7.csv` | agirlik_mg outlier analizi (2 tur) — 32 hücre null (5 üst kesin hata + 17 alt >5x sapma + 10 MAD>10); C39/C40/C18 `mean(skipna=True)` ile güncellendi | Tamamlandı |
| `hansay_processed_v6.8.csv` | dane_sayisi outlier analizi (2 tur) — 23 hücre null (5 üst kesin hata + 15 alt >5x + 3 MAD>10); D39/D40/C19 güncellendi | Tamamlandı |
| `hansay_processed_v6.9.csv` | dane_agirlik_mg outlier analizi (2 tur) — 72 hücre null (68 ratio>5 + 4 MAD>10); E39/E40/C20 güncellendi | Tamamlandı |
| `hansay_processed_v7.0.csv` | Tüm türetilmiş sütunlar yeniden hesaplandı — A (J=H+I), B (toplamlar), C (ortalamalar `mean(skipna=True)` — artık sabit /10 değil), D (kopya/özet), E (verim zincirleri); C17 güncellenemedi (kaynak C16/J41 v5.0'da çıkarılmıştı); FORMUL_REFERANS.json güncellendi | Tamamlandı |
| `hansay_processed_v7.1.csv` | Alan ham değerleri outlier analizi — C11 ve C13 temiz (müdahale yok); C41=3.481.185 mg (`6309 23.xlsx`) log-IQR 3x hata, null yapıldı; D41/E41/E42/D21 zincirleme güncellendi | Tamamlandı |
| `hansay_processed_v7.2.csv` | Outlier analizi devamı — Adım 4 (C41 vs C11×C40 ilişki: 2 C41 null) + Adım 5 (C21/D21 verim: müdahale yok, log-IQR 3x'te gerçek hata çıkmadı); 639 satır, 115 sütun, kismi_not dolu=124 satır | Tamamlandı |
| `hansay_processed_v7.3.csv` | C41 normalize outlier — `c41_m2_norm = C41×E13` sütunu eklendi; standart IQR 3x ile 3 satır yakalandı (0902/3106/3102, hepsi E13=16, c41_m2 4.5-16.7M mg/m²); C41 null, E41/E42/D21 zincirleme güncellendi | Tamamlandı |
| `hansay_processed_v7.4.csv` | AŞAMA 3a — b1-b10 Global IQR 3x: 70 sütun (7 ölçüm tipi × 10), ~6390 değer üzerinden Q1-3×IQR/Q3+3×IQR sınırı uygulandı; 15 hücre null (uzunluk:1, agirlik:6, dane_agirlik:7, sap_alt:1); kismi_not güncellendi | Tamamlandı |
| `hansay_processed_v7.5.csv` | AŞAMA 3b — b1-b10 Global MAD 3.5: aynı 70 sütun, \|0.6745×(x−median)\|/MAD > 3.5 → null; 130 hücre null (uzunluk:16, agirlik:41, dane_sayisi:14, dane_agirlik:48, sap_basak:3, sap_alt:8); türetilmiş sütunlar (Katman 3–5) yeniden hesaplandı | Tamamlandı |
| `hansay_processed_v7.6.csv` | AŞAMA 4a — C11 ve C41 Global IQR 3x: C11'de 1 outlier null; C41 (c41_m2_norm üzerinden) outlier yok; türetilmiş sütunlar yeniden hesaplandı | Tamamlandı |
| `hansay_processed_v7.7.csv` | AŞAMA 4b — C11 ve C41 Global MAD 3.5: C11=31 null, C41 (c41_m2_norm)=13 null; türetilmiş sütunlar yeniden hesaplandı | Tamamlandı |
| `hansay_processed_v7.8.csv` | AŞAMA 5a — Türetilmiş sütunlara Global IQR 3x (n=639): 15 sütun incelendi; 21 null (D41:5, C12:2, C21:2, C41:12) | Tamamlandı |
| `hansay_processed_v7.9.csv` | AŞAMA 5b — Türetilmiş sütunlara Global MAD 3.5: 68 null (C22:1, D41:9, C12:2, C21:19, D21:3, C11:10, C41:24) | Tamamlandı |
| `hansay_processed_v8.0.csv` | `null_sayisi` sütunu eklendi — her satır için 105 ölçüm sütunundaki null hücre sayısı (meta/vld/koordinat sütunları hariç); kismi_not'tan hemen sonra; 117 sütun | Tamamlandı |
| `hansay_processed_v8.1.csv` | `null_sayisi >= 25` olan 9 satır `vld_genel=False` yapıldı (kopyalanmış/güvenilmez veri); `vld_genel_neden` güncellendi; True=630, False=9 | Tamamlandı |
| `hansay_processed_v8.2.csv` | C21 ve D21 ikisi birden null olan 13 satır `vld_genel=False` yapıldı (outlier analizi sonucu verim hesaplanamayan satırlar); True=617, False=22 | Tamamlandı |
| `vAnaliz1.0.csv` | **ANALİZ VERİSİ** — v8.2'den False satırlar çıkarıldı (617 satır); geçici/ara hesap sütunları çıkarıldı (13 sütun); 104 sütun. Arpa, koordinatsız, geçersiz, kopyalanmış ve verimi hesaplanamayan tüm kayıtlar dışarıda. | Tamamlandı |
