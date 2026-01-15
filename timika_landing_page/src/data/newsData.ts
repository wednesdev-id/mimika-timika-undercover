import news1 from "@/assets/news-1.jpg";
import news2 from "@/assets/news-2.jpg";
import news3 from "@/assets/news-3.jpg";
import news4 from "@/assets/news-4.jpg";
import news5 from "@/assets/news-5.jpg";
import news6 from "@/assets/news-6.jpg";

export interface NewsArticle {
  id: number;
  title: string;
  date: string;
  summary: string;
  image: string;
  category: string;
}

export const newsArticles: NewsArticle[] = [
  {
    id: 1,
    title: "Pembangunan Gedung Baru di Pusat Kota Timika Rampung Akhir Tahun",
    date: "16 Januari 2025",
    summary: "Pemerintah daerah Mimika mengumumkan bahwa pembangunan gedung perkantoran modern di pusat kota Timika ditargetkan selesai pada akhir tahun ini. Proyek ini diharapkan dapat meningkatkan layanan publik.",
    image: news1,
    category: "Politik"
  },
  {
    id: 2,
    title: "Festival Budaya Papua Meriah dengan Tarian Tradisional Mimika",
    date: "15 Januari 2025",
    summary: "Acara Festival Budaya Papua yang diselenggarakan di Mimika menampilkan berbagai tarian tradisional dan upacara adat yang menarik ribuan pengunjung dari berbagai daerah.",
    image: news2,
    category: "Budaya"
  },
  {
    id: 3,
    title: "Pasar Tradisional Timika Kembali Ramai Dikunjungi Warga",
    date: "14 Januari 2025",
    summary: "Setelah renovasi, Pasar Tradisional Timika kembali dibuka dan langsung dipadati pengunjung. Para pedagang menyambut baik fasilitas baru yang lebih nyaman dan bersih.",
    image: news3,
    category: "Sosial"
  },
  {
    id: 4,
    title: "Program Pendidikan Gratis Diperluas di Seluruh Kabupaten Mimika",
    date: "13 Januari 2025",
    summary: "Pemerintah Kabupaten Mimika memperluas program pendidikan gratis hingga tingkat SMA, memberikan harapan baru bagi anak-anak Papua untuk mendapatkan pendidikan berkualitas.",
    image: news4,
    category: "Pendidikan"
  },
  {
    id: 5,
    title: "Konservasi Hutan Papua di Mimika Mendapat Apresiasi Dunia",
    date: "12 Januari 2025",
    summary: "Upaya pelestarian hutan hujan tropis di wilayah Mimika mendapat pengakuan dari organisasi lingkungan internasional. Program ini melibatkan masyarakat adat dalam menjaga kelestarian alam.",
    image: news5,
    category: "Lingkungan"
  },
  {
    id: 6,
    title: "Tim Sepak Bola Timika Raih Juara di Turnamen Regional Papua",
    date: "11 Januari 2025",
    summary: "Tim sepak bola Timika berhasil meraih juara pertama dalam turnamen regional Papua setelah mengalahkan tim dari Jayapura di pertandingan final yang berlangsung sengit.",
    image: news6,
    category: "Olahraga"
  }
];
