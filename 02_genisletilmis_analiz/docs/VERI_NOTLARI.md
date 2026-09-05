# Veri Notları — HANSAY İşlenmiş Veri

**Güncel versiyon:** `vAnaliz1.0.csv` (617 satır, 104 sütun)

## Bilinen İsimlendirme / Birim Hataları

> Bu hatalar ham Excel dosyalarından gelip CSV'ye aktarılmıştır. Sütun adları yanıltıcı olsa da **değerler doğrudur**. Aşağıdaki sütun adları `vAnaliz1.0.csv`'deki güncel adlardır (v4.0'da yeniden adlandırıldı).

| Sütun (güncel ad) | Yanıltıcı olan | Gerçek Anlam |
|---|---|---|
| `ort_kilcikli_basak_agirlik_mg__C18` | "kılcıklı" ibaresi — kılcık ayrımı değil | C40'ın kopyası: mg cinsinden ortalama başak ağırlığı (dane+sap). **vAnaliz1.0'dan çıkarıldı** (redundant). |
| `bir_basaktaki_ort_dane_agirlik_gram__C20` | "gram" — birim doğru | E40/1000: ortalama başak dane ağırlığı, gram cinsinden |
| `bin_dane_agirlik_gram__C22` | "bin dane ağırlığı gram" | Aslında **tek dane ağırlığı (mg/dane)** — E40/D40. İsim yanıltıcı ama 1000 dane gram = 1 dane mg eşitliği nedeniyle sayısal değer aynı. |

---

## Verim Sütunları: C21 ve D21

Bu iki sütun farklı metodolojilerle aynı şeyi ölçer: **1 m² alandan elde edilen dane ağırlığı (gram).**

### C21 — `dane_m2_hesap_gram` — Başak Sayısı Bazlı Tahmin

```
C21 = C20 × C12
    = (E40 / 1000) × (C11 × E13)
```

| Bileşen | Sütun | Açıklama |
|---|---|---|
| C20 | `basak_ort_dane_agirlik_gram__C20` | Ortalama başak dane ağırlığı (gram) — 10 örneğin ortalaması |
| C12 | `m2_basak_sayisi__C12` | 1 m²'deki başak sayısı — C11 × E13 |

**Yöntem:** "Bu alanda kaç başak var? Her başakta ortalama kaç gram dane var? Çarp."

---

### D21 — `dane_m2_gercek_gram` — Tartım Bazlı Verim

```
D21 = E42 / 1000
E42 = E41 × E14
E41 = C41 × D41
D41 = E40 / C40
```

| Bileşen | Sütun | Açıklama |
|---|---|---|
| C41 | `olcum_basak_agirlik_ham__C41` | Ölçüm alanındaki **tüm** başakların tartılmış toplam ağırlığı (mg) — **elle girilmiş, lab tartımı, formülsüz** |
| D41 | `basak_dane_oran__D41` | Dane oranı = E40/C40 = ortalama dane ağırlığı / ortalama başak ağırlığı |
| E41 | `olcum_basak_dane_agirlik_hesap__E41` | Ölçüm alanındaki dane ağırlığı (mg) = C41 × D41. **vAnaliz1.0'dan çıkarıldı** (ara hesap). |
| E13/E14 | `olcum_alani_carpani__E13` | Alan çarpanı (ölçüm alanından 1 m²'ye ölçekleme). E14 v5.0'da çıkarıldı, E13 kullanılır. |
| E42 | `dane_m2_tartim_hesap__E42` | 1 m²'deki dane ağırlığı (mg) = E41 × E13. **vAnaliz1.0'dan çıkarıldı** (ara hesap). |

**Yöntem:** "Ölçüm alanındaki başakları tartıyoruz. Bu ağırlığın ne kadarının dane olduğunu biliyoruz (D41). 1 m²'ye ölçekliyoruz."

> **Not:** C41 **hiçbir dosyada formül içermiyor** — sahadan getirilen başakların laboratuvarda tartılmış değeridir. B41 etiketi "1/4 başaklı ağırlık" olarak geçiyor ancak bu etiket tutarsızdır (E13/E14 çarpanı her dosyada farklı).

---

### C21 vs D21 Farkı

- **C21:** Başak *sayısına* dayalı — "kaç başak × başak başına dane"
- **D21:** Başak *ağırlığına* dayalı — "toplam ağırlık × dane oranı × alan çarpanı"

İkisi teorik olarak yakın ama aynı olmak zorunda değil. C21 sayım hatasına, D21 ise tartım hatasına duyarlıdır.

---

## Ölçüm Alanı Çarpanları: E13 ve E14

- E13 = E14 (her satırda eşit, doğrulandı)
- Üç değer: `4` (137 satır), `8` (437 satır), `16` (156 satır)
- Anlamı: ölçüm alanı 1/4, 1/8 veya 1/16 m² — çarpanla 1 m²'ye ölçekleniyor
- **A11, B41, C3 etiket sütunları güvenilmez** — aynı etiket farklı çarpan değerleriyle kullanılmış; E13/E14 otoritedir
