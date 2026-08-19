from models.request import EstimateRequest
from models.response import EstimateResponse
from pydantic import ValidationError

print("--- MENJALANKAN VALIDASI SCHEMA ---")

# 1. Uji Data Request yang VALID (Sesuai Frontend)
try:
    valid_data = {
    "product_description": "Gelang Macrame Custom",
    "target_qty": 100,       # <-- Sebelumnya tertulis 'qty'
    "max_budget": 300000,    # <-- Sebelumnya tertulis 'budget'
    "mandatory_materials": ["Tali Macrame 4mm (Grade: A, Substitusi: Tidak)"]
    }
    req = EstimateRequest(**valid_data)
    print("✅ EstimateRequest VALID berhasil diparsing:", req.model_dump())
except ValidationError as e:
    print("❌ Gagal memvalidasi request valid:", e)

# 2. Uji Data Request yang TIDAK VALID (Misal: budget diisi huruf, wajib angka)
try:
    invalid_data = {
        "product_description": "Gelang Macrame",
        "target_qty": 100,
        "max_budget": "tiga ratus ribu", # Seharusnya integer!
        "mandatory_materials": []
    }
    req = EstimateRequest(**invalid_data)
except ValidationError as e:
    print("✅ Pydantic BERHASIL MENOLAK data salah (Expected Error):")
    print(e.errors()[0]["msg"])

print("--- VALIDASI SELESAI ---")