# Prototip Analiz Özeti — HANSAY Buğday Verisi

**Veri:** `vAnaliz1.0.csv` — 617 kayıt, 42 il, outlier temizliği tamamlanmış  
**Tarih:** 2026-05-30  
**Not:** Bu prototip analizdir — fikir verme amaçlıdır. Detaylı istatistiksel analiz ayrıca yapılacak.

---

## 1. Tanımlayıcı İstatistikler

**C21 (Başak Sayısı Bazlı Verim):** medyan=580 g/m², ortalama=692 g/m², std=448, skewness=0.94  
**D21 (Tartım Bazlı Verim):** medyan=543 g/m², ortalama=623 g/m², std=387, skewness=0.82

Her iki verim sütunu da sağa çarpık dağılım gösteriyor; ortalamanın medyandan belirgin biçimde yüksek olması yüksek verimli birkaç ilin etkisini yansıtıyor.

**C21 ile D21 arasındaki korelasyon güçlü:** r=0.820, p<10⁻¹³⁹ (n=569). İki yöntem büyük ölçüde uyuşuyor.

**C21, D21'den sistematik olarak %12.3 yüksek** (Bland-Altman bias). 95% uyum limitleri [−61.5%, +86.1%] — oldukça geniş, bireysel kayıt düzeyinde iki yöntem önemli farklılıklar gösterebiliyor. Verim analizinde hangi yöntemin kullanıldığı belirtilmeli.

**Görseller:** `output/tanim/`
- `verim_dagilim.png` — C21/D21 histogram + KDE
- `c21_vs_d21.png` — iki yöntem karşılaştırması
- `basak_olcum_boxplot.png` — tüm başak ölçüm dağılımları

---

## 2. Coğrafi / İl Bazlı Analiz

**42 il** veri setinde temsil ediliyor. 5+ kayıtlı 34 il analiz edildi.

**En yüksek medyan C21 verimi (g/m²):** Tekirdağ, Edirne, Bursa gibi Marmara bölgesi illeri öne çıkıyor.  
**En düşük medyan:** Konya, Karaman, Niğde gibi iç Anadolu illeri — kuru tarım ağırlıklı.

Coğrafi dağılım haritasında (koordinat bazlı scatter) verimli alanların Ege kıyısı ve Marmara bölgesinde yoğunlaştığı, iç kesimlerde belirgin düşüş olduğu görülüyor.

**Görseller:** `output/cografi/`
- `il_verim_bar.png` — iller verime göre sıralı bar chart
- `il_verim_boxplot.png` — il bazında dağılım boxplot
- `harita_verim.png` — Türkiye koordinat scatter haritası
- `il_ozet.csv` — n, C21/D21 medyan, std, koordinat özeti

---

## 3. Alan Çarpanı (E13) Bazlı Analiz

E13 değerleri: 4 (1/4 m², n=119), 8 (1/8 m², n=369), 16 (1/16 m², n=129)

**Kruskal-Wallis testi anlamlı:** H=91.96, p<0.0001 — E13 grupları arasında verim farkı istatistiksel olarak anlamlı.

**Grup medyanları (C21):** E13=4 → 517 g/m², E13=8 → 511 g/m², E13=16 → **1052 g/m²**

E13=16 (1/16 m²) grubunun verimi yaklaşık 2 kat yüksek. Bu büyük ihtimalle gerçek bir verim farkı değil — küçük ölçüm alanı (1/16 m²) yüksek alan çarpanı nedeniyle ölçekleme hatasını büyütüyor olabilir. Detaylı analizde E13 grupları ayrı ele alınmalı veya normalize edilmeli.

**Görseller:** `output/alan/`
- `alan_carpani_verim.png` — E13 gruplarına göre C21/D21 boxplot + test
- `c11_dagilim.png` — başak sayımı E13 gruplarına göre

---

## 4. Başak Morfolojisi

**Korelasyon matrisi (Spearman) öne çıkan bulgular:**
- Başak ağırlığı (C40) → C21 verimi: **r=0.701** (güçlü pozitif)
- Dane sayısı (D40) → C21 verimi: **r=0.612** (orta-güçlü pozitif)
- Sap boyu (J39) → C21 verimi: il bazında **r=0.724** (güçlü pozitif)
- Başak uzunluğu (B40) ile sap boyu (J39) arasında pozitif ilişki var — uzun bitkiler hem uzun sap hem uzun başak taşıyor.

**Dane oranı (D41):** Medyan=0.74, D41>1 olan kayıt **yok** — outlier analizi bu biyolojik imkânsızlığı başarıyla temizlemiş.

**Görseller:** `output/morfoloji/`
- `korelasyon_matrisi.png` — ısı haritası
- `dane_orani_dagilim.png` — D41 dağılımı
- `basak_agirlik_vs_verim.png` — il renklendirmeli scatter
- `sap_vs_basak_uzunluk.png` — morfolojik oran (renk=verim)

---

## 5. Verim Bileşen Analizi

**C21 = C20 × C12** zinciri:
- C20 (tek başak dane ağırlığı) ile C21 korelasyonu güçlü
- C12 (m² başak sayısı) ile C21 korelasyonu da güçlü
- İki bileşenin katkısı benzer büyüklükte — verim hem yoğunluktan (C12) hem başak kalitesinden (C20) etkileniyor

**C41 (ham tartım) → D21 zinciri:** Pozitif korelasyon beklenen yönde, ancak D41 (dane oranı) çarpanının değişkenliği D21'deki varyansı artırıyor.

**C21-D21 Bland-Altman:** C21 sistematik olarak D21'den yüksek. Yüksek verimli örneklerde fark daha belirgin — muhtemelen başak sayısı bazlı hesaplamanın aşırı tahmin etmesinden kaynaklanıyor.

**Görseller:** `output/verim/`
- `c21_bilesenleri.png` — C20, C12, C21 scatter matris
- `c41_vs_d21.png` — ham tartım vs verim
- `c21_d21_fark.png` — Bland-Altman uyum analizi

---

## 6. Sap Boyu Analizi

**Bileşenler:**
- Sap başak boyu (H39): medyan ≈ 7 cm — kısa, başağın direkt sap üstü kısmı
- Sap alt boyu (I39): medyan ≈ 68 cm — ana sap uzunluğu
- Toplam sap (J39 = H+I): medyan ≈ 75 cm

İl bazında toplam sap boyu ile C21 verimi arasında **r=0.724** (p<0.001, n=30 il) — verimli bölgelerin daha uzun saplı çeşitler kullandığı veya çevre koşullarının hem sap uzunluğunu hem verimi olumlu etkilediği görülüyor. Nedensellik ilişkisi detaylı analizde irdelenebilir.

**Görseller:** `output/sap/`
- `sap_boy_dagilim.png` — H39, I39, J39 dağılım boxplot
- `sap_boy_vs_verim.png` — il bazında sap boyu vs verim scatter

---

## Öne Çıkan Bulgular (Özet)

| Bulgu | Değer | Not |
|---|---|---|
| C21 medyan verim | 580 g/m² | Sağa çarpık dağılım |
| D21 medyan verim | 543 g/m² | C21'den ~%12 düşük |
| C21-D21 korelasyonu | r=0.820 | Güçlü uyum |
| E13=16 grubu verim anomalisi | 1052 g/m² (2× diğerleri) | Ölçekleme etkisi olabilir |
| Başak ağırlığı → verim | r=0.701 | En güçlü morfoloji-verim ilişkisi |
| Sap boyu → verim (il) | r=0.724 | Coğrafi düzeyde güçlü |
| D41>1 (biyolojik imkânsız) | 0 kayıt | Temizlik başarılı |
| En yüksek verimli bölge | Marmara / Ege | Coğrafi örüntü net |

---

## 7. Enlem / Boylam Korelasyon Analizi

16 sayısal sütunun her biri ile enlem ve boylam arasındaki Spearman korelasyonları hesaplandı (|r|≥0.30 ve p<0.05 anlamlılık eşiği).

**Ana bulgu: Koordinatlarla anlamlı ilişki neredeyse yok.**

| Değişken | Enlem r | Boylam r | Anlamlı? |
|---|---|---|---|
| C11 — Başak sayımı | +0.021 | **+0.327** | Sadece boylam (p<0.001) |
| Dane oranı (D41) | +0.161 | −0.021 | Hayır |
| C21 Verim | +0.015 | −0.136 | Hayır |
| D21 Verim | −0.113 | +0.074 | Hayır |
| Başak uzunluğu | −0.027 | −0.203 | Hayır |
| Sap boyu | −0.031 | −0.137 | Hayır |
| Tüm diğer değişkenler | |r|<0.21 | Hayır |

**Tek anlamlı ilişki:** C11 (ölçüm alanındaki başak sayımı) ile **boylam** arasında r=+0.327 (p<0.001) pozitif korelasyon var. Batıya doğru (düşük boylam) başak sayısı azalıyor, doğuya doğru artıyor. Bu muhtemelen gerçek bir biyolojik örüntüden değil, doğu illerinde daha küçük ölçüm alanı (E13=16, yani 1/16 m²) kullanılmasından ve dolayısıyla daha az sayım yapılmasından kaynaklanıyor olabilir.

**Verim (C21, D21), başak morfolojisi (uzunluk, ağırlık, sap boyu) ve dane özellikleri koordinatlarla anlamlı düzeyde ilişkili değil.** Bu, coğrafi konumun (enlem/boylam) tek başına tarımsal performansı açıklamadığını — belirleyici faktörlerin iklim, çeşit ve toprak gibi koordinatla doğrudan eşleşmeyen değişkenler olduğunu düşündürüyor.

İl bazında görülen güçlü coğrafi örüntü (Bölüm 2) koordinatların ham korelasyonunda kayboldu — bu da bölgesel etkinin doğrusal bir enlem/boylam gradyanından değil, il bazında kümelenen faktörlerden (iklim zonu, sulama altyapısı, yaygın çeşitler) kaynaklandığına işaret ediyor.

**Görseller:** `output/koordinat/`
- `koordinat_korelasyon_heatmap.png` — tüm değişkenler için enlem/boylam korelasyon ısı haritası
- `boylam_korelasyon_scatter.png` — C11 vs boylam scatter (ham + il medyanı)
- `koordinat_korelasyon.csv` — tüm r ve p değerleri

---

## Detaylı Analizde Önerilen Sonraki Adımlar

1. **E13 gruplarını normalize etmek** — 1/16 m² ölçüm alanı verimleri ayrı değerlendirilmeli
2. **Bölgesel regresyon** — il veya bölge bazında C21/D21 belirleyicilerini modellemek
3. **C21 vs D21 seçimi** — hangi yöntemin referans alınacağı metodoloji olarak sabitlenmeli
4. **Çeşit/sulama etkisi** — sulama tipi bilgisi 611/617'de eksik; bu bilgi tamamlanabilirse önemli bir değişken
5. **Sap boyu - verim nedenselliği** — çevre faktörleri (yağış, toprak) kontrol edilmeden korelasyon yorumlanmamalı

---

## Dosya Dizini

```
output/
├── ANALIZ_OZET.md          ← bu dosya
├── koordinat/
│   ├── koordinat_korelasyon.csv
│   ├── koordinat_korelasyon_heatmap.png
│   └── boylam_korelasyon_scatter.png
├── tanim/
│   ├── ozet_istatistik.csv
│   ├── verim_dagilim.png
│   ├── c21_vs_d21.png
│   └── basak_olcum_boxplot.png
├── cografi/
│   ├── il_ozet.csv
│   ├── il_verim_bar.png
│   ├── il_verim_boxplot.png
│   └── harita_verim.png
├── alan/
│   ├── alan_carpani_verim.png
│   └── c11_dagilim.png
├── morfoloji/
│   ├── korelasyon_matrisi.png
│   ├── dane_orani_dagilim.png
│   ├── basak_agirlik_vs_verim.png
│   └── sap_vs_basak_uzunluk.png
├── verim/
│   ├── c21_bilesenleri.png
│   ├── c41_vs_d21.png
│   └── c21_d21_fark.png
└── sap/
    ├── sap_boy_dagilim.png
    └── sap_boy_vs_verim.png
```
