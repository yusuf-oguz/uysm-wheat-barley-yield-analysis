# Sütun Öncelik Sırası — Hesaplama Verileri

Ham olan önce, ondan türetilen sonra gelir.
Koordinat, kimlik, geçerlilik sütunları bu belgede yer almaz.

---

## Ham / Türetilmiş Özet

> Outlier analizinde **önce ham sütunlar** incelendi. Türetilmiş sütunlar her temizleme adımı sonrası `mean(skipna=True)` ile yeniden hesaplandı. Tüm outlier analizi **tamamlandı** (`vAnaliz1.0.csv`).

### Ham Sütunlar — Doğrudan Ölçülen veya Elle Girilen

| Grup | Sütunlar | Kaynak |
|---|---|---|
| **b1–b10 başak ölçümleri** | `bN_uzunluk_cm`, `bN_agirlik_mg`, `bN_dane_sayisi`, `bN_dane_agirlik_mg`, `bN_sap_basak_boyu_cm`, `bN_sap_alt_cm`, `bN_sap_boy_cm` (70 sütun) | Sahada kumpas/terazi ile ölçüm |
| **Ölçüm alanı sayımları** | `olcum_alani_basak__C11`, `basaksiz_bitki_sayisi__C13` | Sahada elle sayım |
| **Alan çarpanı** | `olcum_alani_carpani__E13` | Elle girilmiş (4 / 8 / 16) |
| **Lab tartımı** | `olcum_basak_agirlik_ham__C41` | Laboratuvarda tartılmış, formülsüz |
| ~~Sap ağırlığı ham~~ | ~~`on_basak_sap_agirlik_ham__J24`~~ | **v5.0'da çıkarıldı** — J25 ile eşdeğer, analizde kullanılmadı |

> `bN_sap_boy_cm__JXX` = H + I. Outlier analizinde H ve I incelendi, J otomatik güncellendi.

### Türetilmiş Sütunlar — Hesaplama Ürünü

Tüm aşamalar tamamlandı. Aşağıdaki sütunlardan bir kısmı `vAnaliz1.0.csv`'den çıkarılmıştır (ara hesap veya kopya oldukları için).

| Katman | Sütunlar | vAnaliz1.0'da? |
|---|---|---|
| Katman 3 — Toplamlar | `toplam_basak_uzunluk__B39`, `toplam_basak_agirlik_mg__C39`, `toplam_dane_sayisi__D39`, `toplam_dane_agirlik_mg__E39` | ✗ çıkarıldı |
| Katman 3 — Ortalamalar | `ort_basak_uzunluk_cm__B40`, `ort_basak_agirlik_mg__C40`, `ort_dane_sayisi__D40`, `ort_dane_agirlik_mg__E40`, `ort_sap_basak_boyu__H39`, `ort_sap_basak_alti_boyu__I39`, `ort_sap_boy_cm__J39` | ✓ mevcut |
| Katman 4 — Kopya/özet | `ort_kilcikli_basak_agirlik_mg__C18`, `ort_dane_sayisi_copy__C19`, `ort_sap_boy_cm_copy__C23`, `ort_basak_uzunluk_cm_copy__C24` | ✗ çıkarıldı |
| Katman 4 — Hesaplama | `bir_basaktaki_ort_dane_agirlik_gram__C20`, `bin_dane_agirlik_gram__C22`, `basak_dane_oran__D41` | ✓ mevcut |
| Katman 5 — Verim zincirleri | `m2_basak_sayisi__C12`, `m2_basaksiz_bitki__C14`, `m2_toplam_bitki__C15`, `dane_m2_hesap_gram__C21`, `dane_m2_gercek_gram__D21` | ✓ mevcut |
| Katman 5 — Ara hesap | `olcum_basak_dane_agirlik_hesap__E41`, `dane_m2_tartim_hesap__E42`, `c41_m2_norm` | ✗ çıkarıldı |
| Katman 6 — Sap zinciri | `m2_sap_agirlik_kg__C17` | ✓ mevcut (güncellenemez — kaynak v5.0'da çıkarıldı) |

### Outlier Analiz Sırası (TAMAMLANDI)

Detaylı metodoloji ve rakamlar için → `docs/OUTLIER_ANALIZI.md`

```
✓ AŞAMA 1  →  b1-b10 ham ölçümler (v6.5–v6.9)
               └─ Her ölçüm tipi için 2 tur:
                    TUR 1: p1/p99 → Seri içi MAD>10 → Global IQR 3x
                    TUR 2: Seri içi MAD>10 → Global IQR 3x
                    Son: Türetilmiş sütunlar mean(skipna=True) ile güncellendi

✓ AŞAMA 2  →  Ölçüm alanı ham değerleri (v7.1–v7.3)
               └─ C11: IQR 3x (temiz)
                  C41: c41_m2_norm üzerinden IQR 3x → 6 null

✓ AŞAMA 3  →  b1-b10 Global IQR 3x + MAD 3.5 (v7.4–v7.5)
               └─ 70 sütun, ~6390 gözlem/tip
                  IQR 3x: 15 hücre null
                  MAD 3.5: 130 hücre null
                  Türetilmiş sütunlar yeniden hesaplandı

✓ AŞAMA 4  →  C11/C41 Global IQR 3x + MAD 3.5 (v7.6–v7.7)
               └─ IQR 3x: 1 null | MAD 3.5: 44 null

✓ AŞAMA 5  →  Türetilmiş sütunlar Global IQR 3x + MAD 3.5 (v7.8–v7.9)
               └─ IQR 3x: 21 null | MAD 3.5: 68 null

✓ AŞAMA 6  →  Satır eleme (v8.1–v8.2)
               └─ null_sayisi ≥ 25: 9 satır False
                  C21+D21 ikisi null: 13 satır False
```

### Outlier Analiz Kuralları (Uygulandı)

- Null yapılan her hücre `kismi_not` sütununa kaydedildi
- Türetilmiş ortalamalar her zaman `mean(skipna=True)` — sabit /10 değil
- Sap_boy (J) = H + I; H veya I null yapılırsa J de null yapıldı
- Kaynak null → türetilen null zinciri otomatik korundu

---

## Katman 1 — Ham Ölçümler (b1–b10)

Sahadaki 10 başaktan doğrudan ölçülen değerler. Hiçbir hesaplama uygulanmamış.

| Sütun | Açıklama | Birim |
|---|---|---|
| `bN_uzunluk_cm__BXX` | N. başağın uzunluğu | cm |
| `bN_agirlik_mg__CXX` | N. başağın toplam ağırlığı (dane+sap) | mg |
| `bN_dane_sayisi__DXX` | N. başaktaki dane sayısı | adet |
| `bN_dane_agirlik_mg__EXX` | N. başaktaki toplam dane ağırlığı | mg |
| `bN_sap_basak_boyu_cm__HXX` | N. başağın başak boyu (sap üstü) | cm |
| `bN_sap_alt_cm__IXX` | N. başağın sap altı boyu | cm |
| `bN_sap_boy_cm__JXX` | N. başağın toplam sap boyu (H+I) | cm |

> N = 1–10, XX = Excel satır numarası (29–38)

---

## Katman 2 — Ölçüm Alanı Ham Değerleri

Sahadaki ölçüm alanından doğrudan elde edilen sayımlar ve tartımlar.

| Sütun | Açıklama | Birim | Kaynak |
|---|---|---|---|
| `olcum_alani_basak__C11` | Ölçüm alanındaki başak sayısı | adet | Elle sayım |
| `basaksiz_bitki_sayisi__C13` | Ölçüm alanındaki başaksız bitki sayısı | adet | Elle sayım |
| `olcum_alani_carpani__E13` | Alan çarpanı (ölçüm alanı → 1 m²) | — | Elle girilmiş (4, 8 veya 16) |
| `olcum_alani_carpani2__E14` | Alan çarpanı (E13 ile her zaman eşit) | — | Elle girilmiş |
| `olcum_basak_agirlik_ham__C41` | Ölçüm alanındaki tüm başakların tartılmış toplam ağırlığı | mg | Lab tartımı, elle girilmiş, formülsüz |

---

## Katman 3 — 10 Başak Toplamları ve Ortalamaları

b1–b10 ham verilerinden hesaplanan toplam ve ortalama sütunları.

| Sütun | Formül | Birim |
|---|---|---|
| `toplam_basak_uzunluk__B39` | SUM(B29:B38) | cm |
| `toplam_basak_agirlik_mg__C39` | SUM(C29:C38) | mg |
| `toplam_dane_sayisi__D39` | SUM(D29:D38) | adet |
| `toplam_dane_agirlik_mg__E39` | SUM(E29:E38) | mg |
| `ort_sap_basak_boyu__H39` | SUM(H29:H38)/10 | cm |
| `ort_sap_basak_alti_boyu__I39` | SUM(I29:I38)/10 | cm |
| `ort_basak_uzunluk_cm__B40` | B39/10 | cm |
| `ort_basak_agirlik_mg__C40` | C39/10 — ortalama başak ağırlığı (dane+sap) | mg |
| `ort_dane_sayisi__D40` | D39/10 — bir başaktaki ortalama dane sayısı | adet |
| `ort_dane_agirlik_mg__E40` | E39/10 — bir başaktaki ortalama dane ağırlığı | mg |
| `ort_sap_boy_cm__J39` | SUM(J29:J38)/10 — ortalama toplam sap boyu | cm |

---

## Katman 4 — 10 Başak Toplamlarından Türetilen Özet Değerler

Katman 3 değerlerinden hesaplanan birim dönüşümleri ve oranlar.

| Sütun | Formül | Birim | Not |
|---|---|---|---|
| `ort_kilcikli_basak_agirlik_mg__C18` | =C40 | mg | C40 kopyası — ortalama başak ağırlığı (dane+sap) |
| `ort_dane_sayisi_copy__C19` | =D40 | adet | D40 kopyası |
| `bir_basaktaki_ort_dane_agirlik_gram__C20` | =E40/1000 | gram | E40'ın gram cinsine çevrimi |
| `bin_dane_agirlik_gram__C22` | =E40/D40 | mg/adet | Tek dane ağırlığı (1000 dane gram = 1 dane mg) |
| `ort_basak_uzunluk_cm_copy__C24` | =B40 | cm | B40 kopyası |
| `ort_sap_boy_cm_copy__C23` | =J39 | cm | J39 kopyası |
| `basak_dane_oran__D41` | =E40/C40 | — | Dane oranı: başak ağırlığının ne kadarı dane |

---

## Katman 5 — Ölçüm Alanı Ölçekleme (C41 zinciri)

C41 (ham tartım) ve dane oranından (D41) türetilen alan bazlı hesaplamalar.

| Sütun | Formül | Birim | Açıklama |
|---|---|---|---|
| `olcum_basak_dane_agirlik_hesap__E41` | =C41×D41 | mg | Ölçüm alanındaki dane ağırlığı tahmini |
| `dane_m2_tartim_hesap__E42` | =E41×E14 | mg | 1 m²'ye ölçeklenmiş dane ağırlığı |
| `dane_m2_gercek_gram__D21` | =E42/1000 | gram | **Tartım bazlı 1 m² dane verimi** |

---

## Katman 5 — Başak Sayısı Bazlı Ölçekleme (C11 zinciri)

C11 (başak sayımı) ve alan çarpanından türetilen alan bazlı hesaplamalar.

| Sütun | Formül | Birim | Açıklama |
|---|---|---|---|
| `m2_basak_sayisi__C12` | =C11×E13 | adet/m² | 1 m²'deki başak sayısı |
| `m2_basaksiz_bitki__C14` | =C13×E14 | adet/m² | 1 m²'deki başaksız bitki sayısı |
| `m2_toplam_bitki__C15` | =C12+C14 | adet/m² | 1 m²'deki toplam bitki sayısı |
| `dane_m2_hesap_gram__C21` | =C20×C12 | gram | **Başak sayısı bazlı 1 m² dane verimi** |

---

## Katman 6 — Sap Ağırlığı Zinciri

| Sütun | Formül | Birim | Açıklama |
|---|---|---|---|
| `on_basak_sap_agirlik_ham__J24` | Elle girilmiş | mg | 10 başağın sap ağırlığı (ham) |
| `on_basak_sap_agirlik_sum__J25` | =SUM(J15:J24) | mg | J24'ü toplayan formül — J24 ile pratikte eşit |
| `on_basaktaki_toplam_sap_agirlik_mg__C16` | =J41 | mg | J41 kopyası |
| `on_sap_agirlik_mg__J41` | =J25 veya =J24 | mg | 10 başağın sap ağırlığı |
| `m2_sap_agirlik_kg__C17` | =C16/10000×C12/1000 | kg/m² | 1 m²'deki sap ağırlığı |

---

## Özet: İki Temel Verim Hesabı

```
HAM                         TÜRETME ZİNCİRİ                  SONUÇ
─────────────────────────────────────────────────────────────────────
C11 (başak sayımı)     → ×E13 → C12 → ×C20 →          C21 (hesap verim)
C41 (tartım)           → ×D41 → E41 → ×E14 → E42/1000 → D21 (gerçek verim)
```

**C21:** Başak sayısına dayalı tahmin — sayım hatasına duyarlı
**D21:** Lab tartımına dayalı — tartım hatasına duyarlı
