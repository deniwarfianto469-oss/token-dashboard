
import json
import urllib.request
from datetime import datetime, timezone

TOKEN = "0x6abbaE6B3086e6502fb447D6F1D1d5Dc18d43428"
POOL = "0xa42089070f4e8078debbee9bb272cf8b4ecc5fea"

URL = (
    "https://api.dexscreener.com/latest/dex/pairs/"
    f"robinhood/{POOL}"
)

def cek_market():
    print("=== DRIFTWOOD DRFT BOT ===")
    print("Waktu UTC:", datetime.now(timezone.utc).isoformat())
    print("Token:", TOKEN)
    print("Memeriksa data market...")

    try:
        request = urllib.request.Request(
            URL,
            headers={"User-Agent": "DRFT-Market-Bot"}
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode())

        pair = data.get("pair")
        if not pair and data.get("pairs"):
            pair = data["pairs"][0]

        if not pair:
            print("Data pool belum tersedia dari API.")
            print("Cek pool:", 
                  f"https://dexscreener.com/robinhood/{POOL}")
            return

        print("Harga USD:", pair.get("priceUsd", "N/A"))
        print("Likuiditas USD:",
              pair.get("liquidity", {}).get("usd", "N/A"))
        print("Volume 24 jam:",
              pair.get("volume", {}).get("h24", "N/A"))
        print("Mode: PEMANTAUAN — tidak mengirim transaksi.")

    except Exception as error:
        print("Market belum bisa dibaca:", error)

if __name__ == "__main__":
    cek_market()
