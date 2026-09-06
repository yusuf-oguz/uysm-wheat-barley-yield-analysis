# Extended Analysis: The Continuation After the Internship

> This is the **second, extended stage** of a two-stage project. For the overview and the first stage, see the [parent README](../README.md).

<details>
<summary>🇹🇷 Türkçe özet için tıklayın</summary>

Kaynak veri, ilk aşamadaki 291 dosyadan **769 (Hansay) + 291 (VERİM 3, 264'ü Hansay ile örtüşen)** dosyaya genişletildi, 79 il, ~800 benzersiz saha ölçümü. Pipeline iteratif ilerledi (~90 ara versiyon), süreç boyunca aşılan denemeler ayrı bir arşiv klasörüne ayrıldı.

**Öne çıkan bulgular:** başak ağırlığı ile verim arasında güçlü korelasyon (r=0.701), il bazında sap boyu ile verim arasında da güçlü ilişki (r=0.724); iki farklı hesaplama yöntemi arasında güçlü uyum (r=0.820) ama sistematik ~%12 fark; enlem/boylamla doğrudan anlamlı bir ilişki yok, bölgesel farkların iklim/sulama/çeşit gibi il-bazlı faktörlerden kaynaklandığını düşündürüyor.

Detaylı bulgular, ham veri envanteri ve metodoloji dökümanları için aşağıdaki İngilizce tabloya bakılabilir.

</details>

---

The source data grew from the first stage's 291 files to **769 (the Hansay set) plus 291 (the older VERİM 3 set, 264 overlapping with Hansay)**, covering 79 provinces and roughly 800 unique field measurements. The pipeline became iterative (`data/processed/active/hansay_processed_v1.csv` through `v8.2.csv`, about 90 intermediate versions), with superseded attempts moved into `data/processed/archive/` along the way.

## Where to start

| Looking for | Where to look |
|---|---|
| **Analysis findings** (statistical tests, correlations, charts) | [`output/ANALIZ_OZET.md`](output/ANALIZ_OZET.md) |
| Outlier-cleaning methodology | [`docs/OUTLIER_ANALIZI.md`](docs/OUTLIER_ANALIZI.md) |
| Which columns took priority in the analysis | [`docs/SUTUN_ONCELIK.md`](docs/SUTUN_ONCELIK.md) |
| Notes on data loss and missing data | [`docs/VERI_KAYIPLARI.md`](docs/VERI_KAYIPLARI.md) |
| Excel cell to formula mapping | [`docs/FORMUL_REFERANS.json`](docs/FORMUL_REFERANS.json) |
| Pipeline scripts (run order: `pipeline/` then `inspect/`) | [`scripts/`](scripts/) |

## Highlights

- Ear weight correlates strongly with yield (r=0.701); at the province level, stem length also correlates strongly with yield (r=0.724).
- The two different yield-calculation methods (C21/D21) agree strongly (r=0.820), but with a systematic ~12% offset, characterized with a Bland-Altman analysis.
- Latitude and longitude show no direct significant relationship with yield, suggesting the regional differences come from province-level factors like climate, irrigation, and variety rather than raw geographic position.

Full detail and every chart: see [`output/ANALIZ_OZET.md`](output/ANALIZ_OZET.md).

## Note

`data/source/`, `data/processed/active/`, `data/processed/archive/`, `data/processed/tmp/`, `data/il_verim/`, and `data/extracted_images/` are git-ignored, since they hold institutional data collected in the field by TARBİL/İTÜ UHUZAM (or images extracted from their documents). `docs/DURUM_RAPORU[eski].md`, a detailed raw-data inventory, is excluded for the same reason. See the ownership note in the [parent README](../README.md#a-note-on-raw-data).
