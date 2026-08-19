import os
import json
from dotenv import load_dotenv
from services.gemini_service import classify_product

# Memuat variabel lingkungan dari file .env di root
# Sesuaikan path ke root jika file test ini berada di dalam backend/
load_dotenv(dotenv_path="../.env")

print("--- MENJALANKAN VALIDASI GEMINI SERVICE ---")

# Validasi apakah API Key terbaca
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY tidak ditemukan. Cek file .env!")
    exit(1)
else:
    print("✅ GEMINI_API_KEY berhasil dimuat.")

# Menguji Fungsi Klasifikasi
print("\n👉 Menguji Endpoint Klasifikasi (Gemini 1.5 Flash)...")
try:
    product_desc = "Gelang Macrame Custom warna warni"
    print(f"Input: '{product_desc}'")
    
    # Berikan data simulasi dari index.json agar Gemini tahu opsi kategorinya
    kategori_tersedia = """
    1. yarn_craft (Kerajinan Benang & Tali)
    2. resin_craft (Kerajinan Resin)
    3. wood_craft (Kerajinan Kayu)
    4. packaging_gift (Kemasan & Gift Box)
    5. textile_craft (Kerajinan Tekstil & Kain)
    """
    
    # Panggil fungsi dengan 2 argumen: deskripsi produk dan data kategori
    hasil_klasifikasi = classify_product(product_desc, kategori_tersedia)
    
    print("✅ Berhasil mendapatkan respons dari Gemini!")
    print("Output JSON:")
    print(json.dumps(hasil_klasifikasi, indent=2))
except Exception as e:
    print(f"❌ Terjadi kesalahan saat memanggil Gemini API: {e}")

print("\n--- VALIDASI SELESAI ---")