import requests
import json

# Pastikan URL ini sesuai dengan alamat server FastAPI kamu berjalan
API_URL = "http://localhost:8000/estimate"

# Payload JSON sama persis dengan yang ada di Swagger UI
payload = {
    "product_name": "Totebag Canvas (Custom Draw)",
    "target_qty": 100,
    "budget_max": 3500000,
    "has_mandatory_material": True,
    "mandatory_material_name": "Kanvas 12oz",
    "allow_substitution": False
}

headers = {
    "Content-Type": "application/json"
}

print(f"Mengirim request ke {API_URL}...")

try:
    response = requests.post(API_URL, json=payload, headers=headers)
    
    # Cek apakah request sukses (HTTP 200 OK)
    if response.status_code == 200:
        print("\n✅ BERHASIL! Respons dari server:")
        # Menampilkan respons dalam format JSON yang cantik
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\n❌ GAGAL (Status Code: {response.status_code})")
        print("Detail Error:", response.text)
        
except requests.exceptions.ConnectionError:
    print("\n❌ GAGAL KONEKSI: Pastikan server FastAPI sudah berjalan (uvicorn main:app --reload)!")