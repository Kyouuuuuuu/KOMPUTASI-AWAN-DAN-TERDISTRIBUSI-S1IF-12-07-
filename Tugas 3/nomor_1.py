import sys                                                   # Mengimpor modul sys untuk membaca argumen dari command line
import threading                                             # Mengimpor modul threading untuk membuat dan mengelola thread

hasil_per_thread = []                                        # Variabel global untuk menyimpan hasil penjumlahan dari setiap thread

def hitung_jumlah(thread_id, angka_awal, angka_akhir):       # Mendefinisikan fungsi yang akan dijalankan oleh setiap thread
    total = sum(range(angka_awal, angka_akhir + 1))          # Menghitung total angka dalam rentang yang ditentukan menggunakan sum()
    hasil_per_thread[thread_id] = total                      # Menyimpan hasil perhitungan ke dalam list sesuai ID thread

def jalankan_program(angka_awal, angka_akhir, jumlah_thread): # Mendefinisikan fungsi utama untuk mengatur pembagian tugas dan thread
    if angka_awal > angka_akhir:                             # Memeriksa apakah angka awal lebih besar dari angka akhir
        print("Error: Angka awal tidak boleh lebih besar dari angka akhir!") # Mencetak pesan error jika validasi gagal
        return                                               # Menghentikan fungsi jika terjadi error

    if jumlah_thread <= 0:                                   # Memeriksa apakah jumlah thread kurang dari atau sama dengan nol
        print("Error: Jumlah thread harus lebih dari 0!")    # Mencetak pesan error jika jumlah thread tidak valid
        return                                               # Menghentikan fungsi jika terjadi error

    total_angka = (angka_akhir - angka_awal) + 1             # Menghitung total jumlah angka dalam rentang (inklusif)
    ukuran_dasar = total_angka // jumlah_thread              # Menghitung ukuran dasar pembagian angka per thread (pembagian bulat)
    sisa = total_angka % jumlah_thread                       # Menghitung sisa hasil bagi untuk didistribusikan ke thread awal

    global hasil_per_thread                                  # Mendeklarasikan bahwa kita menggunakan variabel global hasil_per_thread
    hasil_per_thread = [0] * jumlah_thread                   # Menginisialisasi ulang list hasil dengan nilai 0 sebanyak jumlah thread
    
    threads = []                                             # Membuat list kosong untuk menampung objek thread
    start_sekarang = angka_awal                              # Menetapkan nilai awal untuk rentang thread pertama

    for i in range(jumlah_thread):                           # Melakukan perulangan sebanyak jumlah thread yang diminta
        ukuran_chunk = ukuran_dasar + (1 if i < sisa else 0) # Menambahkan 1 angka ke thread awal jika ada sisa pembagian
        end_sekarang = start_sekarang + ukuran_chunk - 1     # Menghitung angka akhir untuk chunk thread saat ini
        
        if end_sekarang > angka_akhir:                       # Memeriksa apakah angka akhir chunk melebihi batas angka akhir
            end_sekarang = angka_akhir                       # Membatasi angka akhir chunk agar tidak melebihi batas

        t = threading.Thread(target=hitung_jumlah, args=(i, start_sekarang, end_sekarang)) # Membuat objek thread baru
        threads.append(t)                                    # Menambahkan objek thread ke dalam list threads
        t.start()                                            # Menjalankan thread yang telah dibuat
        
        start_sekarang = end_sekarang + 1                    # Memperbarui nilai awal untuk thread berikutnya

    for t in threads:                                        # Melakukan perulangan untuk setiap thread dalam list
        t.join()                                             # Menunggu (join) sampai semua thread selesai mengeksekusi tugasnya

    total_keseluruhan = sum(hasil_per_thread)                # Menjumlahkan seluruh hasil perhitungan dari semua thread
    print(f"\nHasil penjumlahan: {total_keseluruhan}")       # Mencetak hasil akhir penjumlahan ke layar

def main():                                                  # Mendefinisikan fungsi utama program
    if len(sys.argv) == 4:                                   # Memeriksa apakah program dijalankan dengan 3 argumen tambahan
        try:                                                 # Memulai blok try untuk menangani kemungkinan error konversi tipe data
            angka_awal = int(sys.argv[1])                    # Mengambil argumen pertama dan mengonversinya menjadi integer
            angka_akhir = int(sys.argv[2])                   # Mengambil argumen kedua dan mengonversinya menjadi integer
            jumlah_thread = int(sys.argv[3])                 # Mengambil argumen ketiga dan mengonversinya menjadi integer
            print(f"Input angka awal: {angka_awal}")         # Mencetak nilai angka awal yang diterima
            print(f"Input angka akhir: {angka_akhir}")       # Mencetak nilai angka akhir yang diterima
            print(f"Thread yang digunakan: {jumlah_thread}") # Mencetak jumlah thread yang digunakan
            jalankan_program(angka_awal, angka_akhir, jumlah_thread) # Memanggil fungsi utama dengan argumen dari command line
        except ValueError:                                   # Menangkap error jika argumen bukan berupa angka
            print("Error: Pastikan argumen yang dimasukkan adalah angka!") # Mencetak pesan error
    else:                                                    # Blok else jika program dijalankan tanpa argumen command line
        try:                                                 # Memulai blok try untuk menangani error input pengguna
            print("--- Mode Input Interaktif ---")           # Mencetak informasi mode interaktif
            angka_awal = int(input("Input angka awal: "))    # Meminta pengguna memasukkan angka awal
            angka_akhir = int(input("Input angka akhir: "))  # Meminta pengguna memasukkan angka akhir
            jumlah_thread = int(input("Thread yang digunakan: ")) # Meminta pengguna memasukkan jumlah thread
            jalankan_program(angka_awal, angka_akhir, jumlah_thread) # Memanggil fungsi utama dengan input dari pengguna
        except ValueError:                                   # Menangkap error jika input pengguna bukan angka
            print("Error: Harap masukkan angka yang valid!") # Mencetak pesan error

if __name__ == "__main__":                                   # Memeriksa apakah file ini dijalankan sebagai program utama
    main()                                                   # Memanggil fungsi main() untuk memulai eksekusi program