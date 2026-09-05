# Genişletilmiş Analiz — Staj Sonrası Devam Çalışması

> Bu, iki aşamalı çalışmanın **ikinci/genişletilmiş aşaması**. Genel bakış ve ilk aşama için → [üst dizin README](../README.md).

**Hazırlayan:** Yusuf Oğuz

Kaynak veri, ilk aşamadaki 291 dosyadan **769 (Hansay) + 291 (VERİM 3, 264'ü Hansay ile örtüşen)** dosyaya genişletildi — 79 il, ~800 benzersiz saha ölçümü. Pipeline iteratif ilerledi (`data/processed/active/hansay_processed_v1.csv` → `v8.2.csv`, ~90 ara versiyon; süreç boyunca aşılan denemeler `data/processed/archive/`'a ayrıldı).

## Nereden Başlanır

| Ne arıyorsun | Nereye bak |
|---|---|
| **Analiz bulguları** (istatistiksel testler, korelasyonlar, grafikler) | [`output/ANALIZ_OZET.md`](output/ANALIZ_OZET.md) |
| **Ham verinin (88 GB flash bellek) tam envanteri** — hangi klasör ne işe yaradı, hangisi kullanılmadı | [`docs/DURUM_RAPORU[eski].md`](<docs/DURUM_RAPORU[eski].md>) |
| Aykırı değer temizliği metodolojisi | [`docs/OUTLIER_ANALIZI.md`](docs/OUTLIER_ANALIZI.md) |
| Hangi sütunun analiz için öncelikli olduğu | [`docs/SUTUN_ONCELIK.md`](docs/SUTUN_ONCELIK.md) |
| Veri kayıpları / eksik veri notları | [`docs/VERI_KAYIPLARI.md`](docs/VERI_KAYIPLARI.md) |
| Excel hücre → formül eşleşmesi | [`docs/FORMUL_REFERANS.json`](docs/FORMUL_REFERANS.json) |
| Pipeline scriptleri (çalıştırma sırası: `pipeline/` → `inspect/`) | [`scripts/`](scripts/) |

## Öne Çıkan Bulgular (özet)

- Başak ağırlığı ile verim arasında güçlü korelasyon (r=0.701); il bazında sap boyu ile verim arasında da güçlü ilişki (r=0.724)
- İki farklı hesaplama yöntemi (C21/D21) arasında güçlü uyum (r=0.820) ama sistematik ~%12 fark — Bland-Altman analizi ile karakterize edildi
- Enlem/boylamla doğrudan anlamlı bir ilişki yok — bölgesel farkların iklim/sulama/çeşit gibi il-bazlı kümelenen faktörlerden kaynaklandığını düşündürüyor

Tam detay ve tüm görseller için → [`output/ANALIZ_OZET.md`](output/ANALIZ_OZET.md)

## Not

`data/`, `output/`, `docs/` altındaki dosyaların çoğu TARBİL/İTÜ UHUZAM'ın sahada topladığı kurumsal veriden türetilmiştir — bkz. üst dizin README'sindeki gizlilik/mülkiyet notu.
