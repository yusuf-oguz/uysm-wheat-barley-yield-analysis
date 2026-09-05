import pandas as pd
import unicodedata

def normalize_sehir(s):
    if not s or pd.isna(s):
        return ""
    s = str(s).strip()
    tr_map = {
        "\u00e7": "c", "\u00c7": "C", "\u011f": "g", "\u011e": "G",
        "\u0131": "i", "\u0130": "I", "\u00f6": "o", "\u00d6": "O",
        "\u015f": "s", "\u015e": "S", "\u00fc": "u", "\u00dc": "U",
    }
    result = [tr_map.get(ch, ch) for ch in s]
    s = "".join(result)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().strip()
    replacements = {"k. maras": "kahramanmaras", "k.maras": "kahramanmaras"}
    return replacements.get(s, s)

IL_MAP = {
    "01": "Adana", "02": "Adiyaman", "03": "Afyonkarahisar", "04": "Agri",
    "05": "Amasya", "06": "Ankara", "07": "Antalya", "08": "Artvin",
    "09": "Aydin", "10": "Balikesir", "11": "Bilecik", "12": "Bingol",
    "13": "Bitlis", "14": "Bolu", "15": "Burdur", "16": "Bursa",
    "17": "Canakkale", "18": "Cankiri", "19": "Corum", "20": "Denizli",
    "21": "Diyarbakir", "22": "Edirne", "23": "Elazig", "24": "Erzincan",
    "25": "Erzurum", "26": "Eskisehir", "27": "Gaziantep", "28": "Giresun",
    "29": "Gumushane", "30": "Hakkari", "31": "Hatay", "32": "Isparta",
    "33": "Mersin", "34": "Istanbul", "35": "Izmir", "36": "Kars",
    "37": "Kastamonu", "38": "Kayseri", "39": "Kirklareli", "40": "Kirsehir",
    "41": "Kocaeli", "42": "Konya", "43": "Kutahya", "44": "Malatya",
    "45": "Manisa", "46": "Kahramanmaras", "47": "Mardin", "48": "Mugla",
    "49": "Mus", "50": "Nevsehir", "51": "Nigde", "52": "Ordu",
    "53": "Rize", "54": "Sakarya", "55": "Samsun", "56": "Siirt",
    "57": "Sinop", "58": "Sivas", "59": "Tekirdag", "60": "Tokat",
    "61": "Trabzon", "62": "Tunceli", "63": "Sanliurfa", "64": "Usak",
    "65": "Van", "66": "Yozgat", "67": "Zonguldak", "68": "Aksaray",
    "69": "Bayburt", "70": "Karaman", "71": "Kirikkale", "72": "Batman",
    "73": "Sirnak", "74": "Bartin", "75": "Ardahan", "76": "Igdir",
    "77": "Yalova", "78": "Karabuk", "79": "Kilis", "80": "Osmaniye",
    "81": "Duzce",
}

# Komsu il ciftleri (her ikisi de siraya eklendi)
KOMSU = {
    frozenset(["adana", "mersin"]), frozenset(["adana", "hatay"]),
    frozenset(["adana", "osmaniye"]), frozenset(["adana", "kahramanmaras"]),
    frozenset(["adiyaman", "sanliurfa"]), frozenset(["adiyaman", "malatya"]),
    frozenset(["adiyaman", "kahramanmaras"]), frozenset(["adiyaman", "diyarbakir"]),
    frozenset(["aydin", "mugla"]), frozenset(["aydin", "izmir"]),
    frozenset(["aydin", "denizli"]), frozenset(["aydin", "manisa"]),
    frozenset(["balikesir", "izmir"]), frozenset(["balikesir", "bursa"]),
    frozenset(["balikesir", "canakkale"]), frozenset(["balikesir", "manisa"]),
    frozenset(["balikesir", "kutahya"]),
    frozenset(["batman", "diyarbakir"]), frozenset(["batman", "mardin"]),
    frozenset(["batman", "siirt"]), frozenset(["batman", "sirnak"]),
    frozenset(["bingol", "diyarbakir"]), frozenset(["bingol", "elazig"]),
    frozenset(["bursa", "canakkale"]), frozenset(["bursa", "bilecik"]),
    frozenset(["canakkale", "balikesir"]),
    frozenset(["denizli", "mugla"]), frozenset(["denizli", "aydin"]),
    frozenset(["denizli", "manisa"]), frozenset(["denizli", "izmir"]),
    frozenset(["diyarbakir", "mardin"]), frozenset(["diyarbakir", "siirt"]),
    frozenset(["diyarbakir", "batman"]), frozenset(["diyarbakir", "sanliurfa"]),
    frozenset(["gaziantep", "sanliurfa"]), frozenset(["gaziantep", "adiyaman"]),
    frozenset(["gaziantep", "kahramanmaras"]), frozenset(["gaziantep", "kilis"]),
    frozenset(["gaziantep", "hatay"]),
    frozenset(["hatay", "adana"]), frozenset(["hatay", "osmaniye"]),
    frozenset(["izmir", "manisa"]), frozenset(["izmir", "mugla"]),
    frozenset(["izmir", "aydin"]),
    frozenset(["kilis", "gaziantep"]), frozenset(["kilis", "hatay"]),
    frozenset(["mardin", "diyarbakir"]), frozenset(["mardin", "batman"]),
    frozenset(["mardin", "sirnak"]),
    frozenset(["mersin", "adana"]), frozenset(["mersin", "konya"]),
    frozenset(["mugla", "aydin"]), frozenset(["mugla", "denizli"]),
    frozenset(["mugla", "manisa"]), frozenset(["mugla", "izmir"]),
    frozenset(["manisa", "izmir"]), frozenset(["manisa", "aydin"]),
    frozenset(["osmaniye", "adana"]), frozenset(["osmaniye", "hatay"]),
    frozenset(["sanliurfa", "gaziantep"]), frozenset(["sanliurfa", "adiyaman"]),
    frozenset(["sanliurfa", "mardin"]), frozenset(["sanliurfa", "diyarbakir"]),
}

df = pd.read_csv(r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv")
df_dahil = df[df["analize_dahil"] == True].copy()

def il_kodu_cek(istasyon_no):
    try:
        s = str(istasyon_no).strip()
        kod = s.split(".")[0].zfill(2) if "." in s else s[:2].zfill(2)
        return kod
    except:
        return None

df_dahil["il_kodu"] = df_dahil["istasyon_no"].apply(il_kodu_cek)
df_dahil["il_adi_dosya"] = df_dahil["il_kodu"].map(IL_MAP)

def sehir_uyusumu(row):
    d = normalize_sehir(row.get("il_adi_dosya", ""))
    k = normalize_sehir(row.get("il_koordinat_bufferli", ""))
    if not d or not k or k in ("turkiye disi", "nan", ""):
        return "belirsiz"
    return "uyumlu" if d == k else "uyumsuz"

def komsu_mu(row):
    d = normalize_sehir(row.get("il_adi_dosya", ""))
    k = normalize_sehir(row.get("il_koordinat_bufferli", ""))
    return frozenset([d, k]) in KOMSU

df_dahil["sehir_uyum"] = df_dahil.apply(sehir_uyusumu, axis=1)
df_dahil["komsu_il"] = df_dahil.apply(komsu_mu, axis=1)

uyumsuz = df_dahil[df_dahil["sehir_uyum"] == "uyumsuz"].copy()
uyumsuz["kategori"] = uyumsuz["komsu_il"].map({True: "komsu_il", False: "UZAK_IL"})

print("=== UYUMSUZ 71 KAYIT KATEGORISI ===")
print(uyumsuz["kategori"].value_counts().to_string())

print("\n=== UZAK IL UYUMSUZLUKLARI (komsu degil) ===")
uzak = uyumsuz[uyumsuz["kategori"] == "UZAK_IL"][[
    "dosya_adi", "istasyon_no", "il_kodu", "il_adi_dosya",
    "il_koordinat_bufferli", "il_koordinat_buffersiz", "enlem", "boylam"
]]
print(uzak.to_string(index=False))
