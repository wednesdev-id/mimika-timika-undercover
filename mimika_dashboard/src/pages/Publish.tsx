import { AdminLayout } from "@/components/AdminLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Upload, CheckCircle } from "lucide-react";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

const publishableArticles = [
  {
    id: 2,
    title: "Festival Budaya Mimika Menyambut Tahun 2024",
    verifiedDate: "2024-01-15",
  },
  {
    id: 6,
    title: "Peningkatan Kualitas Pendidikan di Papua",
    verifiedDate: "2024-01-13",
  },
  {
    id: 7,
    title: "Pariwisata Mimika Terus Berkembang",
    verifiedDate: "2024-01-12",
  },
];

export default function Publish() {
  const [selectedArticles, setSelectedArticles] = useState<number[]>([]);
  const { toast } = useToast();

  const handleSelectAll = () => {
    if (selectedArticles.length === publishableArticles.length) {
      setSelectedArticles([]);
    } else {
      setSelectedArticles(publishableArticles.map((a) => a.id));
    }
  };

  const handleToggleArticle = (id: number) => {
    setSelectedArticles((prev) =>
      prev.includes(id) ? prev.filter((a) => a !== id) : [...prev, id]
    );
  };

  const handlePublish = () => {
    toast({
      title: "Articles Published",
      description: `${selectedArticles.length} article(s) have been published to the main portal.`,
    });
    setSelectedArticles([]);
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Publish to Portal</h1>
          <p className="text-muted-foreground mt-1">
            Select verified articles to publish to the main news portal
          </p>
        </div>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Ready to Publish</CardTitle>
              <div className="flex gap-2">
                <Button variant="outline" onClick={handleSelectAll}>
                  {selectedArticles.length === publishableArticles.length
                    ? "Deselect All"
                    : "Select All"}
                </Button>
                <Button
                  onClick={handlePublish}
                  disabled={selectedArticles.length === 0}
                >
                  <Upload className="mr-2 h-4 w-4" />
                  Publish {selectedArticles.length > 0 && `(${selectedArticles.length})`}
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {publishableArticles.map((article) => (
                <div
                  key={article.id}
                  className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <Checkbox
                      checked={selectedArticles.includes(article.id)}
                      onCheckedChange={() => handleToggleArticle(article.id)}
                    />
                    <div>
                      <p className="font-medium">{article.title}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <CheckCircle className="h-4 w-4 text-status-verified" />
                        <p className="text-sm text-muted-foreground">
                          Verified on {article.verifiedDate}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
}
