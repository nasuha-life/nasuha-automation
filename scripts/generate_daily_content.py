from pathlib import Path
from datetime import datetime
import json

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

CONTENTS = [
    {
        "title": "Pintu Taubat Selalu Terbuka",
        "verse_reference": "QS. Az-Zumar: 53",
        "verse": "Janganlah kamu berputus asa dari rahmat Allah. Sesungguhnya Allah mengampuni dosa-dosa semuanya.",
        "reflection": "Tidak ada dosa yang lebih besar daripada rahmat Allah. Mulailah kembali hari ini.",
        "caption": "Kadang kita merasa sudah terlalu jauh dari Allah. Padahal Allah sendiri yang memanggil kita untuk kembali. Jangan menunggu menjadi sempurna untuk bertaubat, karena taubatlah yang membuat kita semakin dekat kepada-Nya. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Taubat #Muhasabah"
    },
    {
        "title": "Istighfar Menghapus Dosa",
        "verse_reference": "QS. Nuh: 10",
        "verse": "Mohonlah ampun kepada Tuhanmu, sungguh Dia Maha Pengampun.",
        "reflection": "Istighfar yang tulus adalah awal perubahan hati.",
        "caption": "Lisan yang terbiasa beristighfar akan membawa hati menjadi lebih lembut. Ucapkan Astaghfirullah dengan penuh penyesalan dan harapan. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Istighfar #Taubat"
    },
    {
        "title": "Jangan Menunda Taubat",
        "verse_reference": "QS. At-Tahrim: 8",
        "verse": "Wahai orang-orang yang beriman, bertaubatlah kepada Allah dengan taubat yang sebenar-benarnya.",
        "reflection": "Hari ini adalah kesempatan yang belum tentu datang lagi esok.",
        "caption": "Banyak orang berniat berubah, tetapi menundanya terus-menerus. Padahal tidak ada yang tahu kapan kesempatan itu berakhir. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Taubat #Hijrah"
    },
    {
        "title": "Allah Mencintai Orang yang Bertaubat",
        "verse_reference": "QS. Al-Baqarah: 222",
        "verse": "Sesungguhnya Allah mencintai orang-orang yang bertaubat.",
        "reflection": "Taubat bukan hanya diterima, tetapi juga dicintai oleh Allah.",
        "caption": "Betapa indahnya ketika Allah bukan hanya mengampuni, tetapi juga mencintai hamba yang kembali kepada-Nya. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Taubat #RahmatAllah"
    },
    {
        "title": "Sabar dalam Ujian",
        "verse_reference": "QS. Al-Baqarah: 153",
        "verse": "Sesungguhnya Allah bersama orang-orang yang sabar.",
        "reflection": "Kesabaran adalah jalan menuju pertolongan Allah.",
        "caption": "Tidak semua ujian harus segera selesai. Kadang Allah sedang membentuk hati yang lebih kuat dan lebih dekat kepada-Nya. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Sabar #Muhasabah"
    },
    {
        "title": "Syukur Menambah Nikmat",
        "verse_reference": "QS. Ibrahim: 7",
        "verse": "Jika kamu bersyukur, niscaya Aku akan menambah nikmat kepadamu.",
        "reflection": "Hati yang bersyukur akan melihat nikmat di setiap keadaan.",
        "caption": "Sering kali kita fokus pada yang belum dimiliki, hingga lupa pada nikmat yang sudah Allah berikan setiap hari. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Syukur #Muhasabah"
    },
    {
        "title": "Kekuatan Doa",
        "verse_reference": "QS. Ghafir: 60",
        "verse": "Berdoalah kepada-Ku, niscaya Aku perkenankan bagimu.",
        "reflection": "Doa adalah tanda bahwa hati masih bergantung kepada Allah.",
        "caption": "Jangan lelah berdoa meskipun belum melihat jawaban. Allah mendengar setiap bisikan hati yang tulus. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Doa #Tawakal"
    },
    {
        "title": "Dzikir Menenangkan Hati",
        "verse_reference": "QS. Ar-Ra'd: 28",
        "verse": "Ingatlah, hanya dengan mengingat Allah hati menjadi tenteram.",
        "reflection": "Ketenangan sejati tidak datang dari dunia, tetapi dari mengingat Allah.",
        "caption": "Saat hati gelisah, perbanyaklah dzikir. Di sanalah Allah menurunkan ketenangan yang tidak bisa diberikan oleh dunia. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Dzikir #Muhasabah"
    },
    {
        "title": "Tawakal Setelah Ikhtiar",
        "verse_reference": "QS. Ali 'Imran: 159",
        "verse": "Apabila engkau telah membulatkan tekad, maka bertawakallah kepada Allah.",
        "reflection": "Ikhtiar adalah tugas kita, hasil adalah urusan Allah.",
        "caption": "Lakukan yang terbaik, lalu serahkan hasilnya kepada Allah. Tawakal bukan menyerah, tetapi percaya kepada keputusan-Nya. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Tawakal #Iman"
    },
    {
        "title": "Keikhlasan Membebaskan Hati",
        "verse_reference": "QS. Al-Bayyinah: 5",
        "verse": "Mereka diperintah agar menyembah Allah dengan memurnikan ketaatan kepada-Nya.",
        "reflection": "Ikhlas adalah ketika Allah menjadi tujuan utama.",
        "caption": "Banyak beban hati berkurang ketika kita berhenti mencari penilaian manusia dan mulai mencari ridha Allah. Mulailah perjalanan taubatmu hari ini bersama https://nasuha.life\\n\\n#NasuhaLife #Ikhlas #Muhasabah"
    }
]

# Duplicate to make 30 daily variations
while len(CONTENTS) < 30:
    CONTENTS.extend(CONTENTS[: min(len(CONTENTS), 30 - len(CONTENTS))])

today = datetime.utcnow().day
content = CONTENTS[(today - 1) % 30]

with open(OUTPUT_DIR / "output.json", "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=2)

with open(OUTPUT_DIR / "caption.txt", "w", encoding="utf-8") as f:
    f.write(content["caption"])

print("Offline daily content generated successfully.")
