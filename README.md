# NULL_TRACE

**NULL_TRACE** adalah sebuah game *Roguelike Hacking Simulator* berbasis terminal (CLI) yang menggabungkan elemen eksplorasi taktis dengan edukasi pemrograman Python dan konsep *Cybersecurity*. Dibangun menggunakan pustaka `tcod` (Python), game ini menghadirkan sensasi visual retro berkat efek CRT/Scanline ASCII yang khas.

## Fokus Permainan
Game ini berfokus pada **Edukasi Pemrograman dan Keamanan Siber (*Cybersecurity*)** yang dibalut dalam pengalaman bermain (*gameplay*) RPG taktis. Alih-alih merapal mantra sihir atau menembakkan peluru, pemain menggunakan sintaks dan fungsi bahasa pemrograman Python murni untuk menyerang musuh, menambal kerentanan sistem, dan mengeksploitasi server musuh. 

Kurva belajarnya dirancang progresif: dimulai dari pengenalan struktur data/sintaks dasar Python, lalu berevolusi menjadi pemahaman tentang injeksi data, sanitasi *input*, dan investigasi forensik digital.

## Ringkasan Cerita
**Tahun 2084.** Sebagian besar infrastruktur digital global kini dikendalikan oleh superkomputer otoriter misterius bernama **The Core**. 

Anda bermain sebagai **Tracer**, seorang spesialis forensik siber yang baru saja diaktifkan di sebuah Unit Rahasia. Dipandu oleh **Commander Integer** dari markas pertahanan, misi utama Anda adalah menelusuri jejak mentor Anda, **Elias Thorne**, yang hilang secara misterius di dalam sistem The Core. Namun, seiring berjalannya misi, Anda akan menemukan bahwa hilangnya Elias berkaitan erat dengan pencurian cetak biru senjata rahasia pemerintah dan konspirasi kebocoran data (*Data Breach*) berskala global. 

Apakah Elias adalah pahlawan yang mengorbankan dirinya, atau seorang pengkhianat?

## Inti Objek (Tujuan Utama)
Di setiap level (*Node*), pemain memiliki siklus misi (Gameplay Loop) yang harus diselesaikan:
1. **Survive (Bertahan Hidup):** Bergerak menembus *Fog of War* (kabut gelap) dan menjaga *System Integrity* (HP) agar tidak mencapai 0%.
2. **Data Retrieval (Pencurian Data):** Pemain wajib mengeksplorasi labirin untuk menemukan dan meretas target data yang ditandai dengan simbol **`f`**.
3. **Cyber Combat (Basmi Anomali):** Saat bertemu virus atau *System Admin*, pertarungan berlangsung secara *real-time* dan *turn-based*. Pemain harus "mengetik" sintaks Python dengan tepat untuk membasmi ancaman. (Contoh: Menulis `strip()` untuk menambal kerentanan injeksi spasi pada input).
4. **Extraction (Pelarian):** Setelah data diamankan, pemain harus mencapai terminal ekstraksi **`>`** untuk memutuskan koneksi dan melompat ke sektor selanjutnya.

***
