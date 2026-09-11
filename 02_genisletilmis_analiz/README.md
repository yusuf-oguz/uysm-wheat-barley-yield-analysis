# Extended Analysis: The Continuation After the Internship

> This is the **second, extended stage** of a two-stage project. For the overview and the first stage, see the [parent README](../README.md).

<details>
<summary>🇹🇷 Türkçe özet için tıklayın</summary>

Kaynak veri, ilk aşamadaki 291 dosyadan **769 (Hansay) + 291 (VERİM 3, 264'ü Hansay ile örtüşen)** dosyaya, ~800 ham ölçüme (79 il) genişletildi. Pipeline ~90 versiyonluk iteratif bir süreçten geçti, her bir veri kaybı tek tek belgelendi. Sonuç: **617 analiz-hazır kayıt, 42 il**; ham Hansay setinden %19.8 net azalma, ama her adımı gerekçeli.

**Öne çıkan bulgular:** başak ağırlığı ile verim arasında güçlü korelasyon (r=0.701), il bazında sap boyu ile verim arasında da güçlü ilişki (r=0.724); iki farklı hesaplama yöntemi arasında güçlü uyum (r=0.820) ama sistematik ~%12 fark; enlem/boylamla doğrudan anlamlı bir ilişki yok, bölgesel farkların iklim/sulama/çeşit gibi il-bazlı faktörlerden kaynaklandığını düşündürüyor.

Detaylı bulgular, veri kaybı kronolojisi ve aykırı değer metodolojisi için aşağıdaki İngilizce tabloya bakılabilir.

</details>

---

The source data grew from the first stage's 291 files to **769 (the Hansay set) plus 291 (the older VERİM 3 set, 264 overlapping with Hansay)**, roughly 800 raw measurements across 79 provinces. Getting from that raw pool to something analysis-ready took about 90 iterative pipeline versions, with every dropped row or cell documented rather than silently discarded. The result: **617 analysis-ready records across 42 provinces**, a 19.8% net reduction from the raw Hansay set, achieved through 24 individually justified cleaning steps plus a multi-stage, citation-backed outlier detection process (within-series MAD, global IQR, global Modified Z-Score).

## Where to start

| Looking for | Where to look |
|---|---|
| **Analysis findings** (statistical tests, correlations, charts) | [`output/ANALIZ_OZET.md`](output/ANALIZ_OZET.md) |
| **Why 152 rows were dropped**, step by step | [`docs/VERI_KAYIPLARI.md`](docs/VERI_KAYIPLARI.md) |
| **Outlier-detection methodology**, with academic citations | [`docs/OUTLIER_ANALIZI.md`](docs/OUTLIER_ANALIZI.md) |
| Which columns took priority in the analysis | [`docs/SUTUN_ONCELIK.md`](docs/SUTUN_ONCELIK.md) |
| Excel cell to formula mapping | [`docs/FORMUL_REFERANS.json`](docs/FORMUL_REFERANS.json) |
| Pipeline scripts (run order: `pipeline/` then `inspect/`) | [`scripts/`](scripts/) |

## Highlights

- Ear weight correlates strongly with yield (r=0.701); at the province level, stem length also correlates strongly with yield (r=0.724).
- The two different yield-calculation methods (C21/D21) agree strongly (r=0.820), but with a systematic ~12% offset, characterized with a Bland-Altman analysis.
- Latitude and longitude show no direct significant relationship with yield, suggesting the regional differences come from province-level factors like climate, irrigation, and variety rather than raw geographic position.
- A measurement-area group (1/16 m² plots) showed roughly double the yield of the others, most likely a scaling artifact rather than a real effect, flagged rather than reported as a finding.

Full detail and every chart: see [`output/ANALIZ_OZET.md`](output/ANALIZ_OZET.md).

## Data note

`data/source/`, `data/processed/active/`, `data/processed/archive/`, `data/processed/tmp/`, `data/il_verim/`, and `data/extracted_images/` are git-ignored, since they hold institutional data collected in the field by TARBİL/İTÜ UHUZAM. See the ownership note in the [parent README](../README.md).
