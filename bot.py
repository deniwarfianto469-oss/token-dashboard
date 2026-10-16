import json
import os
import sys
import urllib.request
import urllib.error

RPC = os.environ.get("ROBINHOOD_RPC_URL", "").strip()

TOKEN = "0x6abbaE6B3086e6502fb447D6F1D1d5Dc18d43428"
POOL = "0xa42089070f4e8078debbee9bb272cf8b4ecc5fea"


def rpc(method, params):
    if not RPC:
        raise RuntimeError(
            "Secret ROBINHOOD_RPC_URL kosong atau belum diteruskan ke workflow."
        )

    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }).encode()

    req = urllib.request.Request(
        RPC,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        # Jangan cetak URL karena bisa mengandung API key.
        detail = e.read().decode(errors="replace")[:500]
        raise RuntimeError(
            f"RPC HTTP {e.code}: {detail or e.reason}"
        ) from None
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Koneksi RPC gagal: {e.reason}"
        ) from None

    if result.get("error"):
        raise RuntimeError(f"RPC mengembalikan error: {result['error']}")

    if "result" not in result:
        raise RuntimeError("Respons RPC tidak memiliki field result.")

    return result["result"]


def main():
    print("=== DRFT ON-CHAIN MONITOR ===", flush=True)

    if not RPC:
        raise RuntimeError(
            "Secret ROBINHOOD_RPC_URL belum tersedia di workflow."
        )

    print("Menguji koneksi RPC...", flush=True)

    chain_id = int(rpc("eth_chainId", []), 16)
    print(f"Chain ID: {chain_id}", flush=True)

    if chain_id != 4663:
        raise RuntimeError(
            f"Chain ID salah: {chain_id}; diharapkan 4663."
        )

    block = int(rpc("eth_blockNumber", []), 16)
    print(f"Blok terbaru: {block}", flush=True)

    pool_code = rpc("eth_getCode", [POOL, "latest"])
    token_code = rpc("eth_getCode", [TOKEN, "latest"])

    print(f"Kode kontrak pool ditemukan: {pool_code != '0x'}", flush=True)
    print(f"Kode kontrak token ditemukan: {token_code != '0x'}", flush=True)

    if pool_code == "0x":
        raise RuntimeError(
            "Alamat pool tidak memiliki kode kontrak pada chain ini."
        )

    if token_code == "0x":
        raise RuntimeError(
            "Alamat token tidak memiliki kode kontrak pada chain ini."
        )

    print("Tes koneksi dan pemeriksaan kontrak berhasil.", flush=True)
    print("Belum ada transaksi trading.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR BOT: {e}", file=sys.stderr, flush=True)
        raise
