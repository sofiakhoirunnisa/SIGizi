def hitung_status_kalori(kalori):
    if kalori is None:
        return "Normal"

    if kalori < 1800:
        return "Kekurangan Kalori"
    elif 1800 <= kalori <= 2500:
        return "Normal"
    else:
        return "Kelebihan Kalori"


def get_panduan(status_bb, status_kalori, kalori=None):
    """
    status_bb      : Kurus | Normal | Berlebih
    status_kalori  : bisa None
    kalori         : opsional (dipakai jika status_kalori None)
    """

    if not status_kalori:
        status_kalori = hitung_status_kalori(kalori)

    if status_bb == "Kurus" and status_kalori == "Kekurangan Kalori":
        return (
            "Makan 5–6 kali sehari, tambahkan karbohidrat kompleks "
            "(nasi, kentang), protein tinggi (telur, ayam, tempe), "
            "dan lemak sehat (alpukat, kacang)."
        )

    if status_bb == "Kurus" and status_kalori == "Normal":
        return (
            "Pertahankan asupan kalori, fokus peningkatan massa otot "
            "dengan latihan ringan dan protein cukup."
        )

    if status_bb == "Kurus" and status_kalori == "Kelebihan Kalori":
        return (
            "Perbaiki kualitas makanan, hindari junk food, dan atur "
            "pola makan agar kenaikan berat badan tetap sehat."
        )

    if status_bb == "Normal" and status_kalori == "Kekurangan Kalori":
        return (
            "Tambahkan porsi makan utama dan snack sehat seperti buah, "
            "yoghurt, atau kacang."
        )

    if status_bb == "Normal" and status_kalori == "Normal":
        return (
            "Pertahankan pola makan seimbang, konsumsi sayur dan buah "
            "setiap hari, serta olahraga rutin."
        )

    if status_bb == "Normal" and status_kalori == "Kelebihan Kalori":
        return (
            "Kurangi gula dan makanan berlemak, perbanyak sayur dan "
            "tingkatkan aktivitas fisik."
        )

    if status_bb == "Berlebih" and status_kalori == "Kekurangan Kalori":
        return (
            "Evaluasi pola makan, pastikan nutrisi tetap terpenuhi "
            "tanpa menambah kalori berlebih."
        )

    if status_bb == "Berlebih" and status_kalori == "Normal":
        return (
            "Jaga pola makan terkontrol, kurangi cemilan tinggi kalori, "
            "dan olahraga teratur."
        )

    if status_bb == "Berlebih" and status_kalori == "Kelebihan Kalori":
        return (
            "Kurangi porsi makan, hindari gorengan dan makanan manis, "
            "ganti nasi putih dengan nasi merah, dan lakukan olahraga kardio."
        )

    return "Atur pola makan sesuai kebutuhan dan aktivitas harian."


if __name__ == "__main__":
    print(get_panduan("Normal", None, 2100))
    print(get_panduan("Kurus", "Kekurangan Kalori"))
    print(get_panduan("Berlebih", None, 2800))
