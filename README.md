# UYSM: Wheat and Barley Yield Analysis from Field Data

<details>
<summary>🇹🇷 Türkçe özet için tıklayın</summary>

TARBİL (Tarımsal İzleme ve Bilgi Sistemi) kapsamında toplanan Türkiye geneli buğday/arpa saha ölçüm verisinin işlenmesi ve analizi. İTÜ'de staj (2026 bahar) sürecinde başlayıp, staj sonrasında bağımsız olarak genişletilerek devam ettirilmiş bir çalışma.

**Bu repo private tutuluyor.** Veri, TARBİL/İTÜ UHUZAM ve proje yürütücülerinin (Necmettin Türkoğlu, Serdar Bağış) sahada topladığı kurumsal saha verisi, kullanıcının kendi ürettiği bir veri değil. Bu nedenle veri/metodolojinin yayın izni netleşmeden repo public yapılmıyor.

**İki aşama:** `01_ilk_pipeline/` (staj döneminde yapılan ilk çalışma, 291 Excel dosyasından tek bir analiz-hazır CSV üreten 14 adımlık ETL) ve `02_genisletilmis_analiz/` (staj sonrası bağımsız devam çalışması, veri seti 79 il/~800 ölçüme genişletildi, 7 kategoride gerçek istatistiksel analiz eklendi).

88 GB'lık ham flash bellek dökümü ve 2 akademik referans PDF bu repoya dahil değil (nedenleri aşağıda İngilizce bölümde).

</details>

Processing and analysis of wheat and barley field measurement data collected across Türkiye under TARBİL (Tarımsal İzleme ve Bilgi Sistemi, the National Agricultural Monitoring and Information System). The work started during an internship at İTÜ (spring 2026) and kept growing independently afterward.

**This repo is kept private.** The data was collected in the field by TARBİL, İTÜ UHUZAM, and the project's principal investigators (Necmettin Türkoğlu, Serdar Bağış). It isn't self-generated data, so the repo stays private until permission to publish the data and methodology is confirmed.

## Two stages

The work happened in two chronological stages.

### `01_ilk_pipeline/`: the internship-era work

A 14-step ETL pipeline turning 291 field-measurement Excel files (`UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA/`) into one analysis-ready CSV, with 239 records clean enough to include. See [`01_ilk_pipeline/README.md`](01_ilk_pipeline/README.md) for the details.

**This folder is what the İTÜ internship report (see the `internship1-tarbil` project) describes.** That report only covers the first half of this work; the real continuation is in `02_genisletilmis_analiz/` below.

### `02_genisletilmis_analiz/`: the independent continuation after the internship

The source data grew from 291 files to **769 plus 291 (the Hansay set plus the older VERİM 3 set, 264 overlapping)**, covering 79 provinces and roughly 800 unique field measurements. The pipeline became iterative (`hansay_processed_v1` through `v8.2`, about 90 intermediate versions). On top of that, **real statistical analysis across 7 categories** was added: descriptive statistics, province-level geographic distribution, measurement-area effects, ear morphology, yield component analysis, stem length relationships, and latitude/longitude correlation (including Spearman, Kruskal-Wallis, and Bland-Altman tests).

Summary of the main findings: [`02_genisletilmis_analiz/output/ANALIZ_OZET.md`](02_genisletilmis_analiz/output/ANALIZ_OZET.md)
Full inventory of the raw data (the 88 GB flash drive dump): [`02_genisletilmis_analiz/docs/DURUM_RAPORU[eski].md`](<02_genisletilmis_analiz/docs/DURUM_RAPORU[eski].md>)

## A note on raw data

This repo holds only **code, documentation, and the intermediate/processed data the pipeline produced.** It deliberately excludes:

- **The 88 GB raw flash drive dump** (`uysm_flash_bellek_degistirilmemis/`): field photos, İTÜ UHUZAM satellite classification shapefiles, TARBİL's official yield reports. Kept locally as a read-only source, to be backed up externally.
- **2 academic reference PDFs** (`ekstra_kaynaklar/`): a Springer book chapter (Üstündağ, on the KLR model) and a TARBİL agro-meteorology paper. Both are copyrighted third-party publications, cited here as references rather than included as files.

## Known redundant files (not deleted, safe to remove if disk space is needed)

Two files are full, byte-for-byte verified (checked with `diff`) backup copies of the folders next to them. They carry no extra information, just disk space:

1. `uysm-wheat-barley-yield-analysis/UYSM_Project_2/yusuf_oguz_calismalari.zip` (30 MB): an old zip backup of this repo's `02_genisletilmis_analiz/` folder, sitting one level above the repo itself.
2. `01_ilk_pipeline/data/processed/Koordinati Hatali Veriler.zip` (about 500 KB): a zip backup of the folder next to it.

Both are excluded from this repo via `.gitignore` (no need for version control on them), but neither has been deleted from disk.

## A note on paths

The scripts in both stages (`scripts/pipeline/`, `scripts/inspect/`) contain **absolute Windows paths** (`D:\_Development\Projects\...`) specific to where they were originally run. These were left as-is, since they're one-off analysis and ETL scripts rather than a package meant to be re-run elsewhere. Anyone wanting to actually re-run this pipeline (including a future version of me) would need to update those paths first. The code is here to show the pipeline logic and analysis methodology, not for turnkey re-execution.

## Tools

Python: `pandas`, `openpyxl`, `geopandas`/`shapely` for geographic validation, `folium` for interactive maps, `matplotlib`/`seaborn` for charts, `scipy` for statistical tests.
