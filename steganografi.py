from PIL import Image

def sembunyikan_teks(jalur_gambar, teks_rahasia, jalur_keluaran):
    # Buka gambar
    gambar = Image.open(jalur_gambar)

    # Ubah teks rahasia ke biner
    biner_teks_rahasia = ''.join(format(ord(char), '08b') for char in teks_rahasia)
    
    # Tambahkan pembatas null character (karakter null)
    biner_teks_rahasia += '00000000'

    # Periksa apakah gambar dapat menampung teks rahasia
    kapasitas_gambar = gambar.width * gambar.height * 3
    if len(biner_teks_rahasia) > kapasitas_gambar:
        raise ValueError("Gambar tidak memiliki kapasitas yang cukup untuk menyembunyikan teks rahasia.")

    # Sembunyikan teks rahasia dalam gambar 
    piksel = gambar.load()
    indeks = 0
    for i in range(gambar.width):
        for j in range(gambar.height):
            if indeks < len(biner_teks_rahasia):
                r, g, b = piksel[i, j]

                # Modifikasi bit paling tidak signifikan dari setiap saluran warna
                if indeks < len(biner_teks_rahasia):
                    r = (r & 0xFE) | int(biner_teks_rahasia[indeks])
                    indeks += 1
                if indeks < len(biner_teks_rahasia):
                    g = (g & 0xFE) | int(biner_teks_rahasia[indeks])
                    indeks += 1
                if indeks < len(biner_teks_rahasia):
                    b = (b & 0xFE) | int(biner_teks_rahasia[indeks])
                    indeks += 1

                piksel[i, j] = (r, g, b)

    # Simpan gambar dengan teks yang disembunyikan
    gambar.save(jalur_keluaran)

def ekstrak_teks(jalur_gambar):
    # Buka gambar
    gambar = Image.open(jalur_gambar)

    # Tampilkan teks rahasia dari gambar
    piksel = gambar.load()
    biner_teks_rahasia = ""
    for i in range(gambar.width):
        for j in range(gambar.height):
            r, g, b = piksel[i, j]

            # Ekstrak bit paling tidak signifikan dari setiap saluran warna
            biner_teks_rahasia += str(r & 1)
            biner_teks_rahasia += str(g & 1)
            biner_teks_rahasia += str(b & 1)

    # Ubah teks biner menjadi ASCII
    teks_rahasia = ""
    for i in range(0, len(biner_teks_rahasia), 8):
        char = chr(int(biner_teks_rahasia[i:i+8], 2))
        if char == '\x00':  # Karakter null sebagai pembatas
            break
        teks_rahasia += char

    return teks_rahasia

# Menyembunyikan teks rahasia dalam gambar
jalur_gambar = 'image.jpg'
teks_rahasia = 'Ini adalah pesan rahasia.'
jalur_keluaran = 'output_image.jpg'
sembunyikan_teks(jalur_gambar, teks_rahasia, jalur_keluaran)

# Ekstrak Teks rahasia dari gambar
teks_diekstrak = ekstrak_teks(jalur_keluaran)
print("Teks diekstrak:", teks_diekstrak)
