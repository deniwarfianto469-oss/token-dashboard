
import json
import urllib.request

import os

RPC = os.environ["ROBINHOOD_RPC_URL"]
TOKEN = "0x6abbaE6B3086e6502fb447D6F1D1d5Dc18d43428"
POOL = "0xa42089070f4e8078debbee9bb272cf8b4ecc5fea"

def rpc(method, params):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }).encode()

    req = urllib.request.Request(
        RPC,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=20) as response:
        result = json.loads(response.read().decode())

    if "error" in result:
        raise RuntimeError(result["error"])

    return result["result"]

def main():
    print("=== DRFT ON-CHAIN BOT ===")

    chain_id = int(rpc("eth_chainId", []), 16)
    print("Chain ID:", chain_id)

    if chain_id != 4663:
        raise RuntimeError("RPC bukan Robinhood Chain mainnet!")

    block = int(rpc("eth_blockNumber", []), 16)
    print("Blok terbaru:", block)

    code = rpc("eth_getCode", [POOL, "latest"])
    print("Kode kontrak pool ditemukan:", code != "0x")

    token_code = rpc("eth_getCode", [TOKEN, "latest"])
    print("Kode kontrak token ditemukan:", token_code != "0x")

    if code == "0x" or token_code == "0x":
        print("PERINGATAN: periksa kembali alamat kontrak.")

    print("Tes koneksi selesai. Belum ada transaksi trading.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR BOT:", repr(e))
        raise
