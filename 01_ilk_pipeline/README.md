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

The raw data source is **291 Excel (.xlsx) files** under `data/source/UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA/`. Each file represents one measurement day at one station, and contains:

- GPS coordinates (latitude/longitude, in a raw integer format)
- Station code and measurement date
- Crop type and variety name
- 10 individual ear measurements (awned-ear and grain weight, in mg)
- Ear count per square meter
- Grain weight computed two different ways (labeled HESAP/"calculated" and GERÇEK/"actual", in g/m²)
- Plant and ear height measurements

The pipeline's output is one consolidated, quality-flagged CSV ready for analysis: `data/processed/UYSM_merged.csv`.

## Folder structure

```
01_ilk_pipeline/
├── README.md
├── .claude/
│   └── settings.json               Claude Code permission settings
│
├── scripts/
│   ├── pipeline/                   The main ETL pipeline, run in the order below
│   │   ├── extract_data.py
│   │   ├── verify_calculations.py
│   │   ├── check_anomalies.py
│   │   ├── explore_coords.py
│   │   ├── add_city_columns.py
│   │   ├── update_city_columns.py
│   │   ├── check_city_match.py
│   │   ├── duplicate_incele.py
│   │   ├── build_merged_v2.py
│   │   ├── update_merged2.py
│   │   ├── build_unified_csv.py
│   │   ├── finalize_data.py
│   │   ├── analyze_dane.py
│   │   └── kopyala_hatali_koordinatlar.py
│   │
│   ├── viz/                        Visualization scripts
│   │   ├── create_map.py
│   │   ├── create_validity_map.py
│   │   ├── visualize.py
│   │   ├── hansay_gorsel.py
│   │   ├── hansay_ilk_gorsel.py
│   │   └── hansay_ilk_temiz_harita.py
│   │
│   └── inspect/                    One-off inspection and debug scripts
│       ├── inspect_structure.py
│       ├── inspect_formulas.py
│       ├── inspect_formulas2.py
│       ├── inspect_calc.py
│       ├── inspect_one.py
│       ├── inspect_01118.py
│       ├── test_geocode.py
│       └── read_docx.py
│
├── data/
│   ├── source/                     Raw source data (untouched)
│   │   ├── UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA/   291 xlsx files
│   │   ├── hansay.xlsx             Hansay station list, current version
│   │   ├── hansay_ilk.xls          Hansay station list, first version
│   │   └── uysm ek veri.pdf        Supplementary reference document
│   │
│   └── processed/                  Pipeline outputs
│       ├── UYSM_merged.csv         The main output, 291 rows, all columns
│       ├── UYSM_merged_v2.csv      An intermediate version enriched with Hansay data
│       ├── UYSM_hesap_kontrol.csv  Calculation-verification intermediate table
│       ├── hansay_koordinatlar.csv
│       ├── hansay_ilk_koordinatlar.csv
│       ├── Koordinati Hatali Veriler/   Copies of the xlsx files with bad coordinates
│       ├── Koordinati Hatali Veriler.zip
│       └── sadece_bizde_24.txt     24 stations that only appear in our dataset
│
├── output/
│   ├── maps/                       Interactive HTML maps
│   │   ├── UYSM_harita.html         All valid stations
│   │   ├── turkey_validity_map.html
│   │   ├── hansay_harita.html
│   │   ├── hansay_ilk_harita.html
│   │   ├── hansay_ilk_temiz_harita.html
│   │   └── hansay_ilk_200_1200_harita.html
│   │
│   └── charts/                     PNG charts
│       ├── UYSM_dagilim.png
│       └── UYSM_hesap_vs_gercek.png
│
└── docs/
    ├── EXCEL_VERI_YAPISI.md        Excel file structure and cell-to-column mapping
    └── HATALI_VERILER.txt          A record of every data issue found
```

## Pipeline flow

The scripts were run in this order:

```
1. extract_data.py           Extracts raw data from the 291 xlsx files -> UYSM_merged.csv (first version)
2. verify_calculations.py    Compares Excel's own calculations against the raw data -> UYSM_hesap_kontrol.csv
3. check_anomalies.py        Outlier and inconsistency analysis
4. explore_coords.py         Examines the coordinate distribution, flags problems
5. add_city_columns.py       Adds a province match via shapefile
6. update_city_columns.py    Updates the province columns (with buffer analysis)
7. check_city_match.py       Detects station-code vs. coordinate-province mismatches
8. duplicate_incele.py       Reviews duplicate records
9. build_merged_v2.py        Builds a v2 enriched with Hansay data
10. update_merged2.py        Further updates on top of v2
11. build_unified_csv.py     Merges all validation columns, adds a status column
12. finalize_data.py         Final cleanup and column standardization
13. analyze_dane.py          Statistical analysis, by crop type
14. kopyala_hatali_koordinatlar.py   Copies files with bad coordinates into a separate folder
```

Visualization (independent, run after the pipeline):
```
viz/create_map.py             -> UYSM_harita.html (interactive, via folium)
viz/create_validity_map.py    -> turkey_validity_map.html (coordinate validity map)
viz/visualize.py              -> PNG charts
viz/hansay_*.py                -> Hansay data visualizations
```

## Main output: `UYSM_merged.csv` columns

| Column | Source | Description |
|---|---|---|
| `dosya_adi` | File name | The source xlsx file |
| `rapor_no` | Cell J4 | Report number |
| `istasyon_no` | Cell C6 | Province code + station (e.g. `16.03`) |
| `tarih` | Cell C5 | Measurement date |
| `bitki_adi` | Cell C9 | `bugday` (wheat) or `arpa` (barley) |
| `cesit_adi` | Cell C10 | Variety name |
| `enlem` | Cell E3, converted | Latitude, decimal degrees |
| `boylam` | Cell E4, converted | Longitude, decimal degrees |
| `m2_basak_sayisi` | Cell C12 | Ears per square meter |
| `xls_hesap_gram` | Cell C21 | Excel's HESAP-method grain weight (g/m²) |
| `xls_gercek_gram` | Cell D21 | Excel's GERÇEK-method grain weight (g/m²) |
| `duzeltilmis_hesap_gram` | Recomputed from raw rows | HESAP, recalculated in Python |
| `duzeltilmis_gercek_gram` | Recomputed from raw rows | GERÇEK, recalculated in Python |
| `ortalama_bitki_boyu_cm` | Cell C23 | Plant height, cm |
| `ortalama_basak_boyu_cm` | Cell C24 | Ear height, cm |
| `analiz_durumu` | Computed | See below |
| `duzeltme_notu` | Computed | Why a record was corrected |
| `analize_dahil` | Computed | True/False filter column |

### `analiz_durumu` values

| Value | Records | Meaning |
|---|---|---|
| `kullanilabilir` | 219 | Clean, needed no correction |
| `duzeltilmis` | 20 | An error was found and recalculated from raw data |
| `koordinat_disi` | 44 | Coordinate falls outside Türkiye's borders |
| `koordinat_yok` | 4 | Coordinate cell was empty |
| `veri_hatasi` | 4 | Template file or a C41 inconsistency |
| **Total** | **291** | |

**Records included in analysis (`analize_dahil == True`): 239**

## Data errors found (summary)

Full detail: `docs/HATALI_VERILER.txt`

### Calculation errors (corrected)
1. **The E39 = 948 constant bug** (12 files): the cell should hold `=SUM(E29:E38)`, but a constant `948` copied from a template survived instead. `xls_hesap_gram` came out 10 to 25 times too small. Recalculated from the raw rows.
2. **9 ears instead of 10** (8 files): the protocol calls for 10 ear measurements, but only 9 rows were filled in these files. Since Excel always divides by 10, the average came out about 11% low. Fixed by detecting the actual filled-row count before dividing.

### Coordinate problems (excluded from analysis)
- **5 files**: clearly impossible coordinates (Egypt, Russia, Iran)
- **23 files**: right off the Mediterranean/Aegean coast, just outside the land boundary (not caught even with an 11 km buffer)
- **16 files**: coordinates beyond the Syrian border (south of Gaziantep/Hatay/Şanlıurfa)
- **4 files**: coordinate cell was empty or held text

### Other
- **3 files**: the C41 field-weighing value was about 7 times higher than expected (suspected unit mix-up)
- **2 files**: the station code was most likely entered wrong (doesn't match the coordinate)

## Coordinate conversion

The raw coordinates were entered into Excel as plain integers:

```
decimal = raw_int / 10^(len(str(raw_int)) - 2)
```

Examples:
- `3643467` (7 digits) -> `3643467 / 10^5` = **36.43467°**
- `35150` (5 digits) -> `35150 / 10^3` = **35.150°**
- `37435578` (8 digits) -> `37435578 / 10^6` = **37.435578°**

## Geographic validation

- Shapefile: `D:\_Development\Datasets\Turkey Shapefile\gadm41_TUR_shp\gadm41_TUR_1.shp`
- Every coordinate was checked against Türkiye's provincial borders (standard boundary plus an 11 km buffer)
- Legitimate coastal stations that fell just outside the strict boundary were recovered by the buffer

## Python libraries used

| Library | Purpose |
|---|---|
| `openpyxl` | Reading raw data from the xlsx files |
| `pandas` | Data processing and analysis |
| `geopandas` | Analysis against the Türkiye border shapefile |
| `folium` | Interactive HTML map generation |
| `matplotlib` / `seaborn` | Charts |
| `shapely` | Buffer geometry calculations |

Environment: `D:\_Development\Tools\base_env` (all libraries installed there)

## Notes

- **The preferred column for analysis is `duzeltilmis_gercek_gram`**, since it's weighing-based and more reliable.
- **Filter:** `analize_dahil == True` gives 239 records.
- The scripts' paths are rooted at `D:\_Development\Projects\UYSM_Projects\`.
- The shapefile dependency (`D:\_Development\Datasets\...`) is required by some scripts.
- Excel file format: see `docs/EXCEL_VERI_YAPISI.md`.
- Full error detail: see `docs/HATALI_VERILER.txt`.
