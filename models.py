class User:
    """
    Model untuk merepresentasikan data pengguna
    """
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role


class Pasien:
    """
    Model dan logika perhitungan status gizi pasien
    """

    @staticmethod
    def hitung_status(berat, kalori):
        """
        Menentukan status gizi berdasarkan:
        Kebutuhan dasar = berat badan (kg) × 30 kkal

        - < 90% kebutuhan  → Kekurangan Kalori
        - > 110% kebutuhan → Kelebihan Kalori
        - selain itu       → Normal
        """
        kebutuhan_dasar = berat * 30

        if kalori < kebutuhan_dasar * 0.9:
            return "Kekurangan Kalori"
        elif kalori > kebutuhan_dasar * 1.1:
            return "Kelebihan Kalori"
        else:
            return "Normal"
