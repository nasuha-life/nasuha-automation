# Nasuha Automation

Automasi publikasi konten inspiratif harian ke Facebook dan Instagram.

## Deskripsi

Proyek ini mengotomatisasi pembuatan dan publikasi konten harian dengan:
- Caption generator yang dinamis berdasarkan hari
- Integrasi dengan Meta APIs (Facebook & Instagram)
- GitHub Actions workflow untuk penjadwalan otomatis

## Setup

1. Clone repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export META_ACCESS_TOKEN="your_token"
   export FB_PAGE_ID="your_page_id"
   export IG_BUSINESS_ID="your_business_id"
   ```

4. Run script:
   ```bash
   python scripts/post_to_meta.py
   ```

## GitHub Actions

Workflow `daily-post.yml` berjalan setiap hari pada pukul 06:00 WIB.

Dari GitHub repository settings, tambahkan secrets:
- `META_ACCESS_TOKEN`
- `FB_PAGE_ID`
- `IG_BUSINESS_ID`

## Lisensi

MIT
