"""
UYSM Gorselleştirme
-------------------
1. Dagilim karsilastirmasi (histogram + KDE): hesap vs gercek
2. Hesap vs Gercek scatter (1:1 çizgisi ile)
3. İnteraktif Folium haritasi (renkli noktalar)

Çiktilar:
  UYSM_dagilim.png
  UYSM_hesap_vs_gercek.png
  UYSM_harita.html
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

MERGED = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"

df = pd.read_csv(MERGED)
df = df[df["analize_dahil"] == True].copy()

# Kullanilacak sutunlar
HESAP  = "duzeltilmis_hesap_gram"
GERCEK = "duzeltilmis_gercek_gram"

# Gecerli satirlar (her iki deger de dolu)
her_ikisi = df[HESAP].notna() & df[GERCEK].notna()
df_iki    = df[her_ikisi].copy()
df_h      = df[df[HESAP].notna()].copy()
df_g      = df[df[GERCEK].notna()].copy()

print(f"Analize dahil    : {len(df)}")
print(f"Her ikisi dolu   : {len(df_iki)}")
print(f"Sadece hesap dolu: {len(df_h)}")
print(f"Sadece gercek dolu:{len(df_g)}")
print(f"\n--- HESAP istatistikleri ---")
print(df_h[HESAP].describe().round(1))
print(f"\n--- GERCEK istatistikleri ---")
print(df_g[GERCEK].describe().round(1))

# ── RENK VE STIL ──────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", font_scale=1.1)
RENK_HESAP  = "#2E86AB"  # mavi
RENK_GERCEK = "#E84855"  # kirmizi

# ══════════════════════════════════════════════════════════════════════════════
# FIGÜR 1: Dagilim Karsilastirmasi
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=False)
fig.suptitle("1 m² Dane Agirliginin Dagilimi  (n=%d)" % len(df_iki), fontsize=14, fontweight="bold")

def dagilim_plot(ax, seri, renk, baslik, n):
    sns.histplot(seri, bins=30, kde=True, color=renk, alpha=0.6,
                 line_kws={"lw": 2}, ax=ax)
    ax.axvline(seri.median(), color="black", ls="--", lw=1.5,
               label=f"Medyan: {seri.median():.0f} g")
    ax.axvline(seri.mean(), color="gray", ls=":", lw=1.5,
               label=f"Ortalama: {seri.mean():.0f} g")
    ax.set_title(f"{baslik}  (n={n})", fontsize=12)
    ax.set_xlabel("Dane agirligı (g/m²)")
    ax.set_ylabel("Olcum sayisi")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

dagilim_plot(axes[0], df_h[HESAP],  RENK_HESAP,  "HESAP yontemi",  len(df_h))
dagilim_plot(axes[1], df_g[GERCEK], RENK_GERCEK, "GERCEK yontemi", len(df_g))

plt.tight_layout()
plt.savefig(r"D:\_Development\Projects\UYSM_Projects\output\charts\UYSM_dagilim.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nUYSM_dagilim.png kaydedildi.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGÜR 2: Hesap vs Gercek Scatter
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 8))

# Duzeltilmis vs kullanilabilir renkleri
renk_map = {"duzeltilmis": "#F4A261", "kullanilabilir": "#264653"}
renkler  = df_iki["analiz_durumu"].map(renk_map).fillna("#264653")

scatter = ax.scatter(df_iki[HESAP], df_iki[GERCEK],
                     c=renkler, alpha=0.65, s=40, linewidths=0)

# 1:1 çizgisi
lim = max(df_iki[HESAP].max(), df_iki[GERCEK].max()) * 1.05
ax.plot([0, lim], [0, lim], "k--", lw=1.2, label="1:1 çizgisi", zorder=0)
ax.set_xlim(0, lim); ax.set_ylim(0, lim)

# Korelasyon
r = df_iki[[HESAP, GERCEK]].corr().iloc[0, 1]
ax.text(0.05, 0.92, f"r = {r:.3f}", transform=ax.transAxes,
        fontsize=12, color="black",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

# Efsane
from matplotlib.lines import Line2D
legend_els = [
    Line2D([0],[0], marker="o", color="w", markerfacecolor="#264653", ms=8, label="kullanilabilir"),
    Line2D([0],[0], marker="o", color="w", markerfacecolor="#F4A261", ms=8, label="duzeltilmis"),
    Line2D([0],[0], color="k", ls="--", label="1:1 cizgisi"),
]
ax.legend(handles=legend_els, fontsize=9, loc="lower right")

ax.set_xlabel("HESAP  (g/m²)", fontsize=12)
ax.set_ylabel("GERCEK  (g/m²)", fontsize=12)
ax.set_title(f"HESAP vs GERCEK Dane Agirligı  (n={len(df_iki)})", fontsize=13, fontweight="bold")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

plt.tight_layout()
plt.savefig(r"D:\_Development\Projects\UYSM_Projects\output\charts\UYSM_hesap_vs_gercek.png", dpi=150, bbox_inches="tight")
plt.close()
print("UYSM_hesap_vs_gercek.png kaydedildi.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGÜR 3: İnteraktif Folium Haritasi
# ══════════════════════════════════════════════════════════════════════════════
try:
    import folium
    from folium.plugins import MarkerCluster
    import branca.colormap as cm

    df_harita = df_g[df_g["enlem"].notna() & df_g["boylam"].notna()].copy()

    # Renk skalasi: gerçek dane agirligina gore
    vmin = df_harita[GERCEK].quantile(0.02)
    vmax = df_harita[GERCEK].quantile(0.98)
    colormap = cm.LinearColormap(
        colors=["#313695", "#4575b4", "#74add1", "#abd9e9",
                "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"],
        vmin=vmin, vmax=vmax,
        caption="Dane agirligı — GERCEK (g/m²)"
    )

    harita = folium.Map(
        location=[39.0, 35.0],
        zoom_start=6,
        tiles="CartoDB positron"
    )
    colormap.add_to(harita)

    for _, row in df_harita.iterrows():
        gercek_val = row[GERCEK]
        hesap_val  = row.get(HESAP, None)
        renk = colormap(gercek_val)

        durum_emoji = "ok" if row["analiz_durumu"] == "kullanilabilir" else "duz"

        popup_html = f"""
        <div style="font-family:monospace; font-size:12px; min-width:200px">
          <b>{row['dosya_adi']}</b><br>
          <hr style="margin:4px 0">
          Istasyon  : {row.get('istasyon_no','?')}<br>
          Tarih     : {row.get('tarih','?')}<br>
          Bitki     : {row.get('bitki_adi','?')} — {row.get('cesit_adi','?')}<br>
          Il        : {row.get('il_koordinat_bufferli','?')}<br>
          <hr style="margin:4px 0">
          <b>GERCEK   : {gercek_val:.1f} g/m²</b><br>
          HESAP    : {f"{hesap_val:.1f}" if pd.notna(hesap_val) else "—"} g/m²<br>
          <hr style="margin:4px 0">
          Durum     : {row['analiz_durumu']}<br>
          Enlem     : {row['enlem']:.5f}<br>
          Boylam    : {row['boylam']:.5f}
        </div>
        """

        folium.CircleMarker(
            location=[row["enlem"], row["boylam"]],
            radius=6,
            color="white",
            weight=0.8,
            fill=True,
            fill_color=renk,
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"{row.get('il_koordinat_bufferli','?')} — {gercek_val:.0f} g/m²"
        ).add_to(harita)

    harita.save(r"D:\_Development\Projects\UYSM_Projects\output\maps\UYSM_harita.html")
    print("UYSM_harita.html kaydedildi.")

except ImportError as e:
    print(f"Folium yuklu degil, harita atlandi: {e}")
