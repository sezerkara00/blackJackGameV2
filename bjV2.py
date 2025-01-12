import time
import random

def deste_karistir(deste):
    random.shuffle(deste)
    return deste


def score_hesapla(kartlar):
    score = sum(kartlar)
    ace_count = kartlar.count(11)

    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1

    return score


def kart_al(deste):
    return deste.pop()


def blackjack_kontrol(kartlar):
    return score_hesapla(kartlar) == 21 and len(kartlar) == 2


def kazanma_durumu(oyuncu_kart, bilgisayar_kart):
    oyuncu_blackjack = blackjack_kontrol(oyuncu_kart)
    bilgisayar_blackjack = blackjack_kontrol(bilgisayar_kart)
    oyuncu_puan = score_hesapla(oyuncu_kart)
    bilgisayar_puan = score_hesapla(bilgisayar_kart)

    if oyuncu_blackjack and bilgisayar_blackjack:
        return "Berabere"
    if oyuncu_blackjack:
        return "Oyuncu Kazandı(Blackjack)"
    if bilgisayar_blackjack:
        return "Bilgisayar Kazandı(Blackjack)"
    if oyuncu_puan > 21:
        return "Bilgisayar Kazandı"
    if bilgisayar_puan > 21:
        return "Oyuncu Kazandı"
    if oyuncu_puan > bilgisayar_puan:
        return "Oyuncu Kazandı"
    if bilgisayar_puan > oyuncu_puan:
        return "Bilgisayar Kazandı"
    return "Berabere"


def kart_cekme_sureci(el, mesaj, bakiye, odenecek_tutar, deste, sayac=None):
    """Kart çekme işlemini yöneten fonksiyon"""
    while score_hesapla(el) < 21:
        if sayac is not None and sayac == 0:
            secim = input(f"{mesaj} için kart almak istiyor musunuz? (y/n): Double için 'd' giriniz: ").lower()
        else:
            secim = input(f"{mesaj} için kart almak istiyor musunuz? (y/n): ").lower()
        
        if secim in ['y', 'e']:
            el.append(kart_al(deste))
            print(f"Kartlar: {el}")
            print(f"Skor: {score_hesapla(el)}")
            if sayac is not None:
                sayac += 1
        elif secim == 'd' and sayac == 0:
            if bakiye >= odenecek_tutar:
                bakiye -= odenecek_tutar
                odenecek_tutar *= 2
                print(f"Bahis iki katına çıkarıldı. Kalan bakiye: {bakiye}")
                el.append(kart_al(deste))
                print(f"Kartlar: {el}")
                print(f"Skor: {score_hesapla(el)}")
                break
            else:
                print("Yeterli bakiyeniz yok. Bahsi iki katına çıkaramazsınız.")
        else:
            break
    return el, sayac, bakiye, odenecek_tutar


def bilgisayar_oyunu(bilgisayar_kart, deste):
    """Bilgisayarın kart çekme sürecini yöneten fonksiyon"""
    print("\nBilgisayarın kartları açılıyor...")
    print(f"Bilgisayar kartları: {bilgisayar_kart}")
    while score_hesapla(bilgisayar_kart) < 17:
        print("Bilgisayar kart alıyor...")
        time.sleep(1)
        bilgisayar_kart.append(kart_al(deste))
        print(f"Bilgisayar kartları: {bilgisayar_kart}")
        print(f"Bilgisayar skoru: {score_hesapla(bilgisayar_kart)}")
    return bilgisayar_kart


def split_oyunu(oyuncu_kart, bilgisayar_kart, bakiye, odenecek_tutar, deste):
    """Split oyununu yöneten fonksiyon"""
    if bakiye >= odenecek_tutar:
        bakiye -= odenecek_tutar
        deste1 = [oyuncu_kart[0]]
        deste2 = [oyuncu_kart[1]]
        
        # Deste1 için oyun
        print("\nDeste 1 için oyun:")
        deste1.append(kart_al(deste))
        print(f"Deste 1 kartları: {deste1}")
        print(f"Deste 1 skoru: {score_hesapla(deste1)}")
        deste1, _, bakiye, odenecek_tutar = kart_cekme_sureci(deste1, "Deste 1", bakiye, odenecek_tutar, deste)
        
        # Deste2 için oyun
        print("\nDeste 2 için oyun:")
        deste2.append(kart_al(deste))
        print(f"Deste 2 kartları: {deste2}")
        print(f"Deste 2 skoru: {score_hesapla(deste2)}")
        deste2, _, bakiye, odenecek_tutar = kart_cekme_sureci(deste2, "Deste 2", bakiye, odenecek_tutar, deste)
        
        # Bilgisayar oyunu
        bilgisayar_kart = bilgisayar_oyunu(bilgisayar_kart, deste)
        
        # Sonuçları hesapla
        sonuclar = []
        for i, el in enumerate([deste1, deste2], 1):
            print(f"\nDeste {i} Sonucu:")
            sonuc = kazanma_durumu(el, bilgisayar_kart)
            print(f"Deste {i}: {el}, Skor: {score_hesapla(el)}")
            print(f"Sonuç: {sonuc}")
            sonuclar.append(sonuc)
        
        # Kazançları hesapla
        for sonuc in sonuclar:
            if sonuc == "Oyuncu Kazandı":
                bakiye += odenecek_tutar * 2
            elif sonuc == "Oyuncu Kazandı(Blackjack)":
                bakiye += int(odenecek_tutar * 2.5)
            elif sonuc == "Berabere":
                bakiye += odenecek_tutar
        
        print(f"\nGüncel bakiye: {bakiye}")
        return True, bakiye
    else:
        print("Split için yeterli bakiyeniz yok!")
        return False, bakiye


def oyun():
    bakiye = 1000
    while True:
        print("OYUN BAŞLIYOR........... \n\n\n ")
        oyuncu_kart = []
        bilgisayar_kart = []
        deste = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 3
        deste = deste_karistir(deste)

        # Bahis alma
        while bakiye > 0:
            try:
                odenecek_tutar = int(input(f"Ödeyeceğiniz tutarı giriniz: {bakiye} TL: "))
                if bakiye >= odenecek_tutar:
                    bakiye -= odenecek_tutar
                    print(f"Kalan bakiye: {bakiye}")
                    break
                else:
                    print("Bakiye yetersiz")
            except ValueError:
                print("Lütfen geçerli bir sayı giriniz.")

        # İlk kartları dağıt
        for _ in range(2):
            time.sleep(0.5)
            oyuncu_kart.append(kart_al(deste))
            time.sleep(0.5)
            bilgisayar_kart.append(kart_al(deste))

        print(f"Oyuncu kartları: {oyuncu_kart}")
        print(f"Oyuncu skoru: {score_hesapla(oyuncu_kart)}")
        print(f"Bilgisayar kartları: [{bilgisayar_kart[0]}, 'Gizli kart']")

        # Split kontrolü
        if oyuncu_kart[0] == oyuncu_kart[1]:
            secim = input("Kartlarınız eşit. Kart almak istiyor musunuz? (y/n): Double için 'd', Split için 's' giriniz: ").lower()
            if secim == 's':
                split_yapildi, bakiye = split_oyunu(oyuncu_kart, bilgisayar_kart, bakiye, odenecek_tutar, deste)
                if split_yapildi:
                    print("\nOYUN BİTTİ...........")
                    print("OYUNA DEVAM ETMEK İSTİYOR MUSUNUZ? (y/n)")
                    devam = input().lower()
                    if devam in ["n", "h"]:
                        break
                    continue

        # Normal oyun akışı
        sayac = 0
        oyuncu_kart, sayac, bakiye, odenecek_tutar = kart_cekme_sureci(oyuncu_kart, "Oyuncu", bakiye, odenecek_tutar, deste, sayac)
        
        # Bilgisayar oyunu
        bilgisayar_kart = bilgisayar_oyunu(bilgisayar_kart, deste)

        # Sonuç değerlendirme
        sonuc = kazanma_durumu(oyuncu_kart, bilgisayar_kart)
        print("\nSonuç:", sonuc)

        if sonuc == "Oyuncu Kazandı":
            bakiye += odenecek_tutar * 2
        elif sonuc == "Oyuncu Kazandı(Blackjack)":
            bakiye += int(odenecek_tutar * 2.5)
        elif sonuc == "Berabere":
            bakiye += odenecek_tutar

        print(f"Kalan bakiye: {bakiye}")

        print("\nOYUN BİTTİ...........")
        if bakiye <= 0:
            print("Bakiyeniz bitmiştir!")
            break
            
        devam = input("OYUNA DEVAM ETMEK İSTİYOR MUSUNUZ? (y/n): ").lower()
        if devam in ["n", "h"]:
            break


if __name__ == "__main__":
    oyun()
