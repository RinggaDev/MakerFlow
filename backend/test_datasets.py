from services.dataset_service import get_filtered_materials

print("--- MENJALANKAN VALIDASI DATASET SERVICE ---")

try:
    # Simulasi parameter pencarian untuk kategori 'yarn_craft'
    category_id = "resin_craft"
    keywords = ["rumbai", "bingkai"]
    mandatory_ids = ["RC001"] # ID material wajib

    results = get_filtered_materials(category_id, keywords, mandatory_ids)
    
    print(f"✅ Berhasil memuat dataset! Total material terpilih: {len(results)}")
    for item in results:
        print(f" - [{item['id']}] {item['name']} (Unit: {item['unit']})")

except Exception as e:
    print(f"❌ Gagal menguji dataset service: {e}")

print("--- VALIDASI SELESAI ---")