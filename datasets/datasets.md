## Kategori Dataset yang Spesifik

Berdasarkan konteks **UMKM hingga manufaktur menengah Indonesia**, ini kategori yang paling relevan:

```
/datasets
  ├── index.json
  ├── food_beverage/
  │   ├── grain_flour.json          ← Serelia & Tepung
  │   ├── sweetener_dairy.json      ← Pemanis & Susu
  │   ├── oil_fat.json              ← Minyak & Lemak
  │   ├── spice_flavoring.json      ← Bumbu & Perisa
  │   └── packaging_food.json       ← Kemasan khusus pangan
  │
  ├── textile_fashion/
  │   ├── fabric_base.json          ← Kain dasar (katun, polyester, dll)
  │   ├── thread_accessory.json     ← Benang, kancing, resleting
  │   └── dye_finishing.json        ← Pewarna & bahan finishing
  │
  ├── decoration_craft/
  │   ├── wood_material.json        ← Kayu, MDF, triplek
  │   ├── resin_adhesive.json       ← Resin, lem, epoxy
  │   └── paint_coating.json        ← Cat, vernis, coating
  │
  ├── packaging_general/
  │   ├── paper_cardboard.json      ← Kertas, karton, kraft
  │   ├── plastic_wrap.json         ← Plastik, stretch film, bubble wrap
  │   └── label_print.json          ← Label, stiker, sablon
  │
  ├── chemical_cosmetic/
  │   ├── base_ingredient.json      ← Bahan aktif (SLS, AHA, dll)
  │   ├── preservative.json         ← Pengawet & stabilizer
  │   └── fragrance_color.json      ← Parfum & pewarna kosmetik
  │
  ├── metal_fabrication/
  │   ├── steel_aluminum.json       ← Besi, baja, aluminium
  │   ├── fastener.json             ← Baut, mur, paku
  │   └── welding_material.json     ← Kawat las, elektroda
  │
  └── agro_processing/
      ├── seed_fertilizer.json      ← Benih & pupuk
      └── pesticide_organic.json    ← Pestisida & bahan organik
```

Total: **~21 file JSON**, masing-masing berisi 10–15 item → total sekitar **200–300 bahan baku**.

---

## Soal Nama Toko / Link Supplier — Ini Jawabannya

Gue harus jujur di sini, ada **trade-off yang perlu dipertimbangkan**:

### ✅ Efektif JIKA datanya dikurasi manual & statis

```json
{
  "id": "RM001",
  "name": "Tepung Terigu Cakra Kembar",
  "suppliers": [
    {
      "name": "Bogasari Official Store",
      "platform": "Tokopedia",
      "url": "https://tokopedia.com/bogasari",
      "price_per_kg": 13500,
      "min_order": "25kg",
      "location": "Jakarta",
      "last_verified": "2025-06-01"
    }
  ]
}
```

**Keuntungan:**
- Output AI lebih actionable — user langsung bisa beli
- Di mata juri terlihat **sangat production-ready**
- Narrative proposal kuat: *"MakerFlow tidak hanya estimasi, tapi langsung connect ke supplier"*

### ❌ Masalah Utamanya: Data Basi

| Risiko | Dampak |
|---|---|
| Harga berubah setiap minggu | Output AI jadi tidak akurat |
| Link toko bisa mati / berubah | User klik → 404 |
| Tidak ada API publik Tokopedia/Shopee gratis | Tidak bisa auto-update |

---

## Rekomendasi untuk MVP Kompetisi

Pakai pendekatan **"Supplier Category"** bukan link spesifik:

```json
{
  "id": "RM001",
  "name": "Tepung Terigu",
  "supplier_info": {
    "recommended_platforms": ["Tokopedia", "Indotrading", "Ralali"],
    "supplier_type": ["distributor resmi", "agen lokal"],
    "price_range": { "min": 12000, "max": 15000, "currency": "IDR", "unit": "kg" },
    "notes": "Harga fluktuatif mengikuti harga gandum internasional"
  }
}
```

Lalu di output AI, tampilannya:

```
💡 Rekomendasi Supplier:
Cari "Tepung Terigu Protein Tinggi" di Tokopedia / Indotrading
Estimasi harga: Rp 12.000 – 15.000/kg
Tipe supplier: Distributor resmi atau agen lokal
```

**Kenapa ini lebih baik untuk MVP:**
- Tidak ada link yang bisa mati
- Tetap actionable untuk user
- Data tidak basi karena tidak ada harga spesifik per toko
- Bisa di-pitch sebagai *"Phase 2: Direct Supplier Integration via API"* — ini justru menambah nilai roadmap di proposal

---

## Struktur `index.json` Final

```json
{
  "version": "1.0.0",
  "last_updated": "2025-07-01",
  "categories": [
    {
      "id": "food_beverage",
      "label": "Makanan & Minuman",
      "subcategories": [
        { "id": "grain_flour", "label": "Serelia & Tepung", "file": "food_beverage/grain_flour.json" },
        { "id": "sweetener_dairy", "label": "Pemanis & Susu", "file": "food_beverage/sweetener_dairy.json" },
        { "id": "oil_fat", "label": "Minyak & Lemak", "file": "food_beverage/oil_fat.json" },
        { "id": "spice_flavoring", "label": "Bumbu & Perisa", "file": "food_beverage/spice_flavoring.json" },
        { "id": "packaging_food", "label": "Kemasan Pangan", "file": "food_beverage/packaging_food.json" }
      ]
    },
    {
      "id": "textile_fashion",
      "label": "Tekstil & Fashion",
      "subcategories": [
        { "id": "fabric_base", "label": "Kain Dasar", "file": "textile_fashion/fabric_base.json" },
        { "id": "thread_accessory", "label": "Benang & Aksesori", "file": "textile_fashion/thread_accessory.json" },
        { "id": "dye_finishing", "label": "Pewarna & Finishing", "file": "textile_fashion/dye_finishing.json" }
      ]
    },
    {
      "id": "decoration_craft",
      "label": "Dekorasi & Kerajinan",
      "subcategories": [
        { "id": "wood_material", "label": "Material Kayu", "file": "decoration_craft/wood_material.json" },
        { "id": "resin_adhesive", "label": "Resin & Perekat", "file": "decoration_craft/resin_adhesive.json" },
        { "id": "paint_coating", "label": "Cat & Coating", "file": "decoration_craft/paint_coating.json" }
      ]
    },
    {
      "id": "packaging_general",
      "label": "Kemasan Umum",
      "subcategories": [
        { "id": "paper_cardboard", "label": "Kertas & Karton", "file": "packaging_general/paper_cardboard.json" },
        { "id": "plastic_wrap", "label": "Plastik & Wrap", "file": "packaging_general/plastic_wrap.json" },
        { "id": "label_print", "label": "Label & Print", "file": "packaging_general/label_print.json" }
      ]
    },
    {
      "id": "chemical_cosmetic",
      "label": "Kimia & Kosmetik",
      "subcategories": [
        { "id": "base_ingredient", "label": "Bahan Aktif", "file": "chemical_cosmetic/base_ingredient.json" },
        { "id": "preservative", "label": "Pengawet & Stabilizer", "file": "chemical_cosmetic/preservative.json" },
        { "id": "fragrance_color", "label": "Parfum & Pewarna", "file": "chemical_cosmetic/fragrance_color.json" }
      ]
    },
    {
      "id": "metal_fabrication",
      "label": "Fabrikasi Logam",
      "subcategories": [
        { "id": "steel_aluminum", "label": "Besi & Aluminium", "file": "metal_fabrication/steel_aluminum.json" },
        { "id": "fastener", "label": "Baut & Fastener", "file": "metal_fabrication/fastener.json" },
        { "id": "welding_material", "label": "Material Las", "file": "metal_fabrication/welding_material.json" }
      ]
    },
    {
      "id": "agro_processing",
      "label": "Agro & Pengolahan",
      "subcategories": [
        { "id": "seed_fertilizer", "label": "Benih & Pupuk", "file": "agro_processing/seed_fertilizer.json" },
        { "id": "pesticide_organic", "label": "Pestisida & Organik", "file": "agro_processing/pesticide_organic.json" }
      ]
    }
  ]
}
```

---

Lanjut ke mana sekarang?

1. **Generate sample dataset lengkap** untuk 2-3 kategori (siap pakai)
2. **Struktur folder full project** MakerFlow
3. **Template prompt engineering** final dengan dataset injection
4. **Draft outline proposal** AIC