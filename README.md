Nama : Rahel Meilinda Aruan

NPM : 2506598513

Kelas : PBP F

### Pertanyaan Reflektif Tugas 1

1. **Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?** 
   
   Ya, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Elemen-elemen ini sangat membantu saya dalam membagi struktur kode agar menjadi lebih terorganisir, mudah dibaca (*readable*), dan mudah saat ingin melakukan perubahan pada kode tertentu secara berkala (*maintainability*). Bagi browser, struktur semantik memperjelas hierarki konten, seperti memisahkan area *Hero* (`<section class="hero">`) dan area *Projects* (`<section class="projects">`) pada website portofolio saya. Selain itu, tag `<article>` khusus dimanfaatkan pada setiap *card project* untuk menandai bahwa tiap projek merupakan satu kesatuan informasi yang independen.

2. **Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**
   
   Tantangan utama yang saya hadapi adalah menyesuaikan alur tata letak (*layout flow*) dan *spacing* saat layar mengecil. Pada tampilan desktop, elemen *hero section* menggunakan *grid layout* dua kolom yang berdampingan. Saat berpindah ke mobile, layout tersebut harus diubah menjadi satu kolom vertikal agar konten tidak bertumpuk. Saya mengevaluasi prioritas tampilan mobile berdasarkan kenyamanan membaca pengguna, dengan urutan: **Nama $\rightarrow$ Peran (Role) $\rightarrow$ Foto Profil $\rightarrow$ Bio Singkat $\rightarrow$ Tombol Aksi (CTA)**. Mungkin, di bagian inilah tantangan tersendirinya karena cukup tricky bagi saya saat mengubah-ubah kode yang bersangkutan sembari menjaga tampilan desktopnya tetap rapi. Selama proses ini, saya menghapus *margin* negatif dan menetralkan penataan kaku seperti `justify-self: end` menjadi rata tengah (*center alignment*) dengan batas jarak (*gap*) yang konsisten.

3. **Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?**
   
   Batasan utama dari *static web* murni adalah seluruh data proyek dan teks informasi masih ditulis secara langsung (*hardcoded*) di dalam berkas HTML. Hal ini membuat pembaruan konten menjadi kurang praktis karena harus mengubah markup HTML satu per satu. Selain itu, situs belum bisa memproses interaksi langsung dari pengunjung. Untuk iterasi selanjutnya, fungsionalitas dinamis yang paling ingin saya tambahkan adalah integrasi *backend* (seperti Django) untuk mengelola data portofolio melalui database, pengolahan formulir kontak (*contact form*) interaktif, serta fitur filter proyek berdasarkan kategori atau *tech stack*.

### Penggunaan AI

#### 1. Tools AI yang Digunakan
* **Claude 3.5 Sonnet (Anthropic):** Digunakan sebagai pembanding logika struktur CSS Flexbox/Grid dan optimasi keterbacaan kode (*clean code*).
* **Gemini 3.1:** Digunakan untuk brainstorming workflow ideal pengerjaan tugas 1 *debugging* CSS, penyusunan urutan komponen responsif.

#### 2. Strategi Prompting & Bagian Spesifik yang Dibantu
Sebelum menanyakan secara spesifik, saya menanyakan workflow ideal terlebih dahulu selama pengerjaan tugas 1 ini
terutama di bagian branchingnya. Setelah itu saya mendesain website portofolio di figma dan membuat versi codenya secara manual untuk struktur garis besar kode. Setelah itu, saya bertanya pada AI untuk hal yang saya ingin tambahkan tapi saya belum ketahui, seperti bagaimana membuat efek ala glassmorphism pada card, bagaimana mengatur navigation bar agar saat suatu button di click, ia akan mengarahkan langsung pada page tertentu dan mengubah state button lainnya secara otomatis, serta membantu saya dalam memperbaiki layout gambar pada device mobile (*responsivity*).

Adapun ini adalah salah satu contoh dari strategi umum yang saya pakai dalam menyelesaikan masalah diatas:
* Misalnya, saya ingin debugging layout mobile dengan gambar. Saya memberikan *screenshot* tampilan mobile yang mengalami *overlapping* (teks bertumpuk dengan gambar) beserta potongan kode CSS/HTML terkait, dengan instruksi spesifik untuk mengurutkan kembali struktur elemen secara linier.
* Lalu, saya memoles tampilan akhirnya dengan mengajukan *follow-up prompt* ketika foto profil masih bergeser ke kanan di mobile akibat properti desktop (`justify-self: end`), saya meminta solusi untuk menetralkan *alignment* foto ke tengah (*center*) dan memperlebar jarak (*gap*) antar-komponen secara proporsional.
* Setelah masalah utama (masalah responsive) terselesaikan, saya mengatur dan mengedit kembali gap dan padding yang menurut saya masih bisa diperbaiki pada tampilan mobile.
