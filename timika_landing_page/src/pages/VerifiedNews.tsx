import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search, Eye, Upload } from "lucide-react";
import { AdminLayout } from "@/components/AdminLayout";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Input,
    Button,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from "@/shared/ui";
const mockVerifiedArticles = [
    {
        id: 2,
        title: "Festival Budaya Timika Menyambut Tahun 2024",
        source: "Timika News",
        date: "2024-01-14",
        verifiedDate: "2024-01-15",
    },
    {
        id: 6,
        title: "Peningkatan Kualitas Pendidikan di Papua",
        source: "Portal Berita Timika",
        date: "2024-01-12",
        verifiedDate: "2024-01-13",
    },
    {
        id: 7,
        title: "Pariwisata Timika Terus Berkembang",
        source: "Travel Papua",
        date: "2024-01-11",
        verifiedDate: "2024-01-12",
    },
];

export default function VerifiedNews() {
    const [searchQuery, setSearchQuery] = useState("");
    const navigate = useNavigate();

    const filteredArticles = mockVerifiedArticles.filter((article) =>
        article.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <AdminLayout>
            <div className="space-y-6">
                <div>
                    <h1 className="text-3xl font-bold text-foreground">Verified News</h1>
                    <p className="text-muted-foreground mt-1">
                        Articles that have been verified and ready for publishing (Timika)
                    </p>
                </div>

                <Card>
                    <CardHeader>
                        <CardTitle>Verified Articles</CardTitle>
                        <div className="relative mt-4">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search verified articles..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-10"
                            />
                        </div>
                    </CardHeader>
                    <CardContent>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Title</TableHead>
                                    <TableHead>Source</TableHead>
                                    <TableHead>Scraped Date</TableHead>
                                    <TableHead>Verified Date</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredArticles.map((article) => (
                                    <TableRow key={article.id}>
                                        <TableCell className="font-medium">{article.title}</TableCell>
                                        <TableCell>{article.source}</TableCell>
                                        <TableCell>{article.date}</TableCell>
                                        <TableCell>{article.verifiedDate}</TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => navigate(`/article/${article.id}`)}
                                                >
                                                    <Eye className="h-4 w-4" />
                                                </Button>
                                                <Button variant="outline" size="sm">
                                                    <Upload className="mr-2 h-4 w-4" />
                                                    Publish
                                                </Button>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>
            </div>
        </AdminLayout>
    );
}
