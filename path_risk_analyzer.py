import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# 1. Veriyi Yükle ve Birleştir (published_paths.txt ve modified_paths.txt'den)
def load_and_merge_data():
    # Text dosyalarını oku
    with open("published_paths.txt") as f:
        published = [line.strip().split(" | ") for line in f.readlines()]
    with open("modified_paths.txt") as f:
        modified = [line.strip().split(" | ") for line in f.readlines()]

    # DataFrame oluştur
    df_pub = pd.DataFrame(published, columns=["path", "published_risk"])
    df_mod = pd.DataFrame(modified, columns=["path", "modified_risk"])

    # Risk değerlerini float'a çevir ve birleştir
    df_pub["published_risk"] = df_pub["published_risk"].str.replace("Risk: ", "").astype(float)
    df_mod["modified_risk"] = df_mod["modified_risk"].str.replace("Risk: ", "").astype(float)
    df = pd.merge(df_pub, df_mod, on="path", how="outer").fillna(0)

    return df

# 2. Risk Değişimlerini Hesapla
def calculate_risk_changes(df):
    df["risk_change"] = df["modified_risk"] - df["published_risk"]
    df["trend"] = np.where(
        df["risk_change"] > 0.1, "↑ Kötüleşen",
        np.where(df["risk_change"] < -0.1, "↓ İyileşen", "→ Sabit")
    )
    return df

# 3. Ana Analiz Fonksiyonu
def analyze_paths(df):
    # A) Trend Analizi
    slope, intercept, r_value, _, _ = stats.linregress(
        df["published_risk"], df["modified_risk"]
    )
    print(f"\n🔍 Trend Analizi (R²={r_value**2:.2f}):")
    print(f" - Modified Risk = {intercept:.2f} + {slope:.2f} * Published Risk")

    # B) İyileşen/Kötüleşen Path'ler
    trend_counts = df["trend"].value_counts()
    print("\n📊 Path Trend Dağılımı:")
    print(trend_counts.to_string())

    # C) Kritik Path'ler (CVSS ≥7.0)
    critical_pub = df[df["published_risk"] >= 7.0]
    critical_mod = df[df["modified_risk"] >= 7.0]
    print(f"\n⚠️ Kritik Path Sayısı (Published): {len(critical_pub)}")
    print(f"⚠️ Kritik Path Sayısı (Modified): {len(critical_mod)}")

    # D) Görselleştirme
    plot_risk_changes(df)

    # Sonuçları CSV'ye yaz
    df.to_csv("path_risk_changes.csv", index=False)
    df[df["trend"] == "↓ İyileşen"].to_csv("improved_paths.csv", index=False)
    df[df["trend"] == "↑ Kötüleşen"].to_csv("worsened_paths.csv", index=False)

# 4. Görselleştirme
def plot_risk_changes(df):
    plt.figure(figsize=(12, 8))

    # Scatter plot
    colors = {"↑ Kötüleşen": "red", "↓ İyileşen": "green", "→ Sabit": "gray"}
    for trend, group in df.groupby("trend"):
        plt.scatter(
            group["published_risk"], group["modified_risk"],
            color=colors[trend], label=trend, alpha=0.6
        )

    # Referans çizgileri
    plt.axline((0, 0), slope=1, color="blue", linestyle="--", label="Değişim Yok")
    plt.xlabel("Published Risk (CVSS)")
    plt.ylabel("Modified Risk (CVSS)")
    plt.title("Path Risk Değişim Analizi")
    plt.legend()
    plt.grid(True)

    # Trend çizgisi
    x = np.linspace(df["published_risk"].min(), df["published_risk"].max(), 100)
    coeffs = np.polyfit(df["published_risk"], df["modified_risk"], 1)
    plt.plot(x, np.polyval(coeffs, x), color="black", label="Genel Trend")

    plt.savefig("risk_change_plot.png", bbox_inches="tight")
    print("\n📈 Görsel kaydedildi: risk_change_plot.png")

# Ana İşlem
if __name__ == "__main__":
    print("⏳ Veri analizi başlatılıyor...")
    df = load_and_merge_data()
    df = calculate_risk_changes(df)
    analyze_paths(df)
    print("\n✅ Analiz tamamlandı! Çıktılar:")
    print(" - path_risk_changes.csv (Tüm path'ler)")
    print(" - improved_paths.csv (İyileşen path'ler)")
    print(" - worsened_paths.csv (Kötüleşen path'ler)")
    print(" - risk_change_plot.png (Görsel)")
