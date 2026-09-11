# UYSM Field Measurement ETL Pipeline

> This is the **first stage** of a two-stage project. For the overview and what came next, see the [parent README](../README.md).

<details>
<summary>🇹🇷 Türkçe özet için tıklayın</summary>

Türkiye genelindeki istasyonlardan toplanan buğday/arpa saha ölçüm verilerini, tarımsal rekolte tahmini için işlemeye yönelik bir ETL pipeline'ı. Ham veri: 291 adet Excel dosyası, her biri bir istasyonun tek ölçüm gününü temsil ediyor (GPS koordinatı, istasyon kodu, tarih, bitki türü, 10 başak ölçümü, iki farklı yöntemle hesaplanmış dane ağırlığı).

14 adımlık pipeline, hepsi tek bir birleşik CSV'ye (`UYSM_merged.csv`) çıkıyor: veri çıkarma, hesap doğrulama, aykırı değer analizi, koordinat inceleme, il eşleştirme, tekrar kontrolü, Hansay verisiyle zenginleştirme, son standardizasyon, istatistiksel analiz. 291 kayıttan 239'u analize dahil edilebilir kalitede (44'ü Türkiye sınırları dışı koordinat, 20'si hesap hatası tespit edilip düzeltilmiş, 4'ü koordinatsız, 4'ü veri hatası).

İki gerçek hesap hatası bulunup düzeltildi: 12 dosyada bir Excel formülü yerine sabit bir değer kalmış (hesap 10-25 kat küçük çıkıyordu), 8 dosyada 10 yerine 9 başak ölçümü girilmiş (Excel yine de 10'a bölüyordu). Ham koordinatlar Excel'de tam sayı formatında (ör. `3643467` → `36.43467°`), Türkiye il sınırlarına karşı (11 km buffer ile) doğrulandı.

</details>

---

## What this pipeline does

Built to process wheat and barley field measurement data collected from stations across Türkiye, for crop yield estimation.

The raw data source is **291 Excel (.xlsx) files**. Each file represents one measurement day at one station, and contains:

- GPS coordinates (latitude/longitude, in a raw integer format)
- Station code and measurement date
- Crop type and variety name
- 10 individual ear measurements (awned-ear and grain weight, in mg)
- Ear count per square meter
- Grain weight computed two different ways (labeled HESAP/"calculated" and GERÇEK/"actual", in g/m²)
- Plant and ear height measurements

The pipeline's output is one consolidated, quality-flagged CSV ready for analysis: `data/processed/UYSM_merged.csv`. It runs in 14 steps: extraction, calculation verification, outlier and coordinate checks, province matching, duplicate review, a Hansay-enriched merge, final standardization, and a by-crop-type statistical summary. Visualization scripts (interactive maps and charts) run independently afterward.

## Data errors found

Two real calculation errors were caught by recomputing every value from the raw measurement rows and flagging mismatches against Excel's own output:

1. **The E39 = 948 constant bug** (12 files): the cell should hold `=SUM(E29:E38)`, but a constant `948` copied from a template survived instead. `xls_hesap_gram` came out 10 to 25 times too small. Recalculated from the raw rows.
2. **9 ears instead of 10** (8 files): the protocol calls for 10 ear measurements, but only 9 rows were filled in these files. Since Excel always divides by 10, the average came out about 11% low. Fixed by detecting the actual filled-row count before dividing.

Coordinate problems accounted for most of the remaining exclusions: 5 files had clearly impossible coordinates (Egypt, Russia, Iran), 23 were just off the Mediterranean/Aegean coast outside the land boundary even with an 11 km buffer, 16 fell beyond the Syrian border, and 4 had an empty or non-numeric coordinate cell. A further 5 files had other issues (an unexpectedly large field-weighing value, or a station code that didn't match its coordinate). Full detail: `docs/HATALI_VERILER.txt`.

## Main output: `UYSM_merged.csv`

| `analiz_durumu` value | Records | Meaning |
|---|---|---|
| `kullanilabilir` | 219 | Clean, needed no correction |
| `duzeltilmis` | 20 | An error was found and recalculated from raw data |
| `koordinat_disi` | 44 | Coordinate falls outside Türkiye's borders |
| `koordinat_yok` | 4 | Coordinate cell was empty |
| `veri_hatasi` | 4 | Template file or a C41 inconsistency |
| **Total** | **291** | |

**Records included in analysis (`analize_dahil == True`): 239.** The preferred column for analysis is `duzeltilmis_gercek_gram` (the weighing-based yield estimate, recalculated in Python), since it's more reliable than the count-based `duzeltilmis_hesap_gram`.

## Coordinate conversion

Raw coordinates were entered into Excel as plain integers, decoded as:

```
decimal = raw_int / 10^(len(str(raw_int)) - 2)
```

For example, `3643467` (7 digits) becomes `3643467 / 10^5` = **36.43467°**. Every coordinate was then checked against Türkiye's provincial borders with an 11 km buffer, which recovered legitimate coastal stations that fell just outside the strict boundary.

## Folder structure

`data/source/`, `data/processed/`, and `output/maps/` are git-ignored (real institutional field data, see the [parent README](../README.md#repository-structure)) and only exist locally.

```
01_ilk_pipeline/
├── scripts/
│   ├── pipeline/    The 14-step ETL, extraction through the final statistical summary
│   ├── viz/         Interactive maps and charts
│   └── inspect/     One-off inspection and debug scripts
├── data/            Source spreadsheets and pipeline outputs (git-ignored)
├── output/          Generated maps and charts (git-ignored)
└── docs/
    ├── EXCEL_VERI_YAPISI.md   Excel file structure and cell-to-column mapping
    └── HATALI_VERILER.txt     Full record of every data issue found
```

## Tools

Python: `openpyxl` for reading the source spreadsheets, `pandas` for processing, `geopandas`/`shapely` for the geographic boundary validation, `folium` for interactive maps, `matplotlib`/`seaborn` for charts.

The pipeline scripts contain absolute local paths from where they were originally run, since they're one-off analysis scripts rather than a package meant to be re-run elsewhere; they document the pipeline logic rather than serving as turnkey-executable code.
