from datetime import datetime

OPENERS = [
    "Bismillah, semoga hari ini membawa keberkahan.",
    "Assalamu'alaikum, semoga Allah memudahkan urusan kita semua.",
    "Mari luangkan sejenak untuk mengingat Allah.",
    "Semoga hati kita semakin dekat kepada Allah hari ini."
]

CTAS = [
    "Bagikan kepada orang yang Anda sayangi.",
    "Semoga bermanfaat dan menjadi amal jariyah.",
    "Aamiin ya Rabbal 'alamin.",
    "Semoga Allah memberi kita kekuatan untuk mengamalkannya."
]

HASHTAGS = [
    "#NasuhaLife #Taubat #Muhasabah",
    "#NasuhaLife #Islam #Quran",
    "#NasuhaLife #DoaHarian #Hijrah",
    "#NasuhaLife #Istighfar #Tadabbur"
]

def generate_caption():
    day = datetime.utcnow().day
    opener = OPENERS[day % len(OPENERS)]
    cta = CTAS[(day * 2) % len(CTAS)]
    tags = HASHTAGS[(day * 3) % len(HASHTAGS)]

    body = (
        "Allah tidak pernah menutup pintu taubat bagi hamba-Nya. "
        "Sekecil apa pun langkah kita untuk kembali kepada-Nya, "
        "rahmat-Nya selalu lebih luas daripada dosa-dosa kita."
    )

    return f"{opener}\n\n{body}\n\n{cta}\n\n{tags}"
