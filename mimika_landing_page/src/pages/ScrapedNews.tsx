import { useState } from "react";
import { AdminLayout } from "@/components/AdminLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui";
import { Input } from "@/shared/ui";
import { Button } from "@/shared/ui";
import { Badge } from "@/shared/ui";
import { Tabs, TabsList, TabsTrigger } from "@/shared/ui";
import { Search, RefreshCw, Edit, Trash2, Calendar, FileText } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "@/shared/ui";

const mockArticles = [
  {
    id: 1,
    title: "Pembangunan Jalan Trans Papua Segera Dilanjutkan",
    source: "Portal Berita Timika",
    date: "2024-01-15",
    status: "pending" as const,
    preview: "Pemerintah mengumumkan kelanjutan proyek pembangunan jalan Trans Papua yang akan menghubungkan berbagai wilayah di Papua.",
    thumbnail: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400",
    isNew: true,
  },
  {
    id: 2,
    title: "Festival Budaya Mimika Menyambut Tahun 2024",
    source: "Mimika News",
    date: "2024-01-14",
    status: "verified" as const,
    preview: "Festival budaya tahunan Mimika akan digelar dengan menampilkan tarian tradisional dan pameran kerajinan lokal.",
    thumbnail: "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400",
    isNew: true,
  },
  {
    id: 3,
    title: "Hoaks: Klaim Palsu tentang Pertambangan",
    source: "Social Media",
    date: "2024-01-14",
    status: "hoax" as const,
    preview: "Informasi yang beredar di media sosial tentang penutupan tambang ternyata tidak benar dan telah diklarifikasi oleh pihak berwenang.",
    thumbnail: "https://images.unsplash.com/photo-1504192010706-dd7f569ee2be?w=400",
    isNew: false,
  },
  {
    id: 4,
    title: "Program Kesehatan Gratis untuk Warga Timika",
    source: "Kompas Papua",
    date: "2024-01-13",
    status: "published" as const,
    preview: "Dinas Kesehatan Mimika meluncurkan program pemeriksaan kesehatan gratis untuk seluruh warga Timika sepanjang bulan Januari.",
    thumbnail: "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=400",
    isNew: false,
  },
  {
    id: 5,
    title: "Peningkatan Infrastruktur Pendidikan di Mimika",
    source: "Portal Berita Timika",
    date: "2024-01-13",
    status: "pending" as const,
    preview: "Pemerintah daerah mengalokasikan anggaran untuk renovasi dan pembangunan gedung sekolah baru di berbagai kecamatan.",
    thumbnail: "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400",
    isNew: false,
  },
  {
    id: 6,
    title: "Pasar Tradisional Timika Ramai Jelang Tahun Baru",
    source: "Timika Today",
    date: "2024-01-12",
    status: "pending" as const,
    preview: "Aktivitas perdagangan di pasar tradisional Timika meningkat signifikan menjelang perayaan tahun baru.",
    thumbnail: "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400",
    isNew: false,
  },
];

const statusLabels = {
  pending: "Belum Disunting",
  verified: "Sudah Diverifikasi",
  hoax: "Hoax",
  published: "Sudah Dipublikasikan",
};

const statusColors = {
  pending: "bg-status-pending/20 text-status-pending border-status-pending/30",
  verified: "bg-status-verified/20 text-status-verified border-status-verified/30",
  hoax: "bg-status-hoax/20 text-status-hoax border-status-hoax/30",
  published: "bg-status-published/20 text-status-published border-status-published/30",
};

export default function ScrapedNews() {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [isRefreshing, setIsRefreshing] = useState(false);
  const navigate = useNavigate();

  const filteredArticles = mockArticles.filter((article) => {
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.preview.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterStatus === "all" || article.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
      toast.success("Berhasil", {
        description: "Berita baru berhasil dimuat dari scraper.",
      });
    }, 1000);
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Katalog Berita Scraper</h1>
            <p className="text-muted-foreground mt-1">
              Kelola semua berita yang diambil dari scraper
            </p>
          </div>
          <Button
            onClick={handleRefresh}
            disabled={isRefreshing}
            variant="outline"
            className="gap-2"
          >
            <RefreshCw className={`h-4 w-4 ${isRefreshing ? "animate-spin" : ""}`} />
            Refresh Data Scraper
          </Button>
        </div>

        <Card>
          <CardHeader>
            <div className="space-y-4">
              <Tabs value={filterStatus} onValueChange={setFilterStatus}>
                <TabsList className="grid w-full grid-cols-5">
                  <TabsTrigger value="all">Semua Berita</TabsTrigger>
                  <TabsTrigger value="pending">Belum Disunting</TabsTrigger>
                  <TabsTrigger value="verified">Sudah Diverifikasi</TabsTrigger>
                  <TabsTrigger value="published">Sudah Dipublikasikan</TabsTrigger>
                  <TabsTrigger value="hoax">Hoax</TabsTrigger>
                </TabsList>
              </Tabs>

              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Cari berita berdasarkan judul atau isi..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
          </CardHeader>

          <CardContent>
            <div className="grid gap-4">
              {filteredArticles.map((article) => (
                <Card key={article.id} className="overflow-hidden hover:shadow-md transition-shadow">
                  <div className="flex gap-4 p-4">
                    {/* Thumbnail */}
                    <div className="relative flex-shrink-0 w-32 h-32 rounded-lg overflow-hidden bg-muted">
                      <img
                        src={article.thumbnail}
                        alt={article.title}
                        className="w-full h-full object-cover"
                      />
                      {article.isNew && (
                        <Badge className="absolute top-2 left-2 bg-primary text-primary-foreground">
                          Baru
                        </Badge>
                      )}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg text-foreground mb-2 line-clamp-2">
                            {article.title}
                          </h3>
                          <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                            {article.preview}
                          </p>

                          <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <div className="flex items-center gap-1">
                              <FileText className="h-4 w-4" />
                              <span>{article.source}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Calendar className="h-4 w-4" />
                              <span>{article.date}</span>
                            </div>
                          </div>
                        </div>

                        <div className="flex flex-col items-end gap-3">
                          <Badge
                            variant="outline"
                            className={statusColors[article.status]}
                          >
                            {statusLabels[article.status]}
                          </Badge>

                          <div className="flex gap-2">
                            <Button
                              variant="default"
                              size="sm"
                              onClick={() => navigate(`/article/${article.id}`)}
                              className="gap-2"
                            >
                              <Edit className="h-4 w-4" />
                              Sunting Berita
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              className="text-destructive hover:text-destructive"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}

              {filteredArticles.length === 0 && (
                <div className="text-center py-12 text-muted-foreground">
                  <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Tidak ada berita ditemukan</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
}
