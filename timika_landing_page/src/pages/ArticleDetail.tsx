import { useState, useRef } from "react";
import { AdminLayout } from "@/components/AdminLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@undercover/ui-react";
import { Input } from "@undercover/ui-react";
import { Textarea } from "@undercover/ui-react";
import { Button } from "@undercover/ui-react";
import { Label } from "@undercover/ui-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@undercover/ui-react";
import { StatusBadge } from "@/components/StatusBadge";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, CheckCircle, AlertTriangle, Upload, Save, Image as ImageIcon } from "lucide-react";
import { toast } from "@undercover/ui-react";

type ArticleStatus = "pending" | "verified" | "hoax" | "published";

import { fetchNewsById } from "../services/api";
import { useEffect } from "react";

export default function ArticleDetail() {
    const { id } = useParams();
    const navigate = useNavigate();

    const fileInputRef = useRef<HTMLInputElement>(null);

    const [isLoading, setIsLoading] = useState(true);
    const [article, setArticle] = useState<{
        title: string;
        source: string;
        date: string;
        status: ArticleStatus;
        content: string;
        imageUrl: string;
        category: string;
    }>({
        title: "",
        source: "",
        date: "",
        status: "pending",
        content: "",
        imageUrl: "",
        category: "",
    });

    useEffect(() => {
        const loadArticle = async () => {
            if (!id) return;
            setIsLoading(true);
            try {
                const data = await fetchNewsById(id);
                if (data) {
                    setArticle({
                        title: data.title,
                        source: data.url || "Unknown Source",
                        date: data.date,
                        status: "pending",
                        content: data.summary,
                        imageUrl: data.image,
                        category: data.category,
                    });
                } else {
                    toast.error("Article not found");
                    navigate("/scraped-news");
                }
            } catch (error) {
                console.error(error);
                toast.error("Failed to load article");
            } finally {
                setIsLoading(false);
            }
        };
        loadArticle();
    }, [id, navigate]);

    const relatedNews = [
        { id: "2", title: "Proyek Infrastruktur Papua Tengah Berlanjut", source: "Papua Today", date: "2024-01-14" },
        { id: "3", title: "Pembangunan Jembatan di Timika Dimulai", source: "Timika Express", date: "2024-01-13" },
        { id: "4", title: "Akses Jalan ke Pedalaman Papua Diperbaiki", source: "Papua News", date: "2024-01-12" },
    ];

    const handleSave = () => {
        toast("Article Saved", {
            description: "Your changes have been saved as draft.",
        });
    };

    const handleVerify = () => {
        setArticle({ ...article, status: "verified" });
        toast.success("Article Verified", {
            description: "Article has been marked as verified.",
        });
    };

    const handleMarkAsHoax = () => {
        setArticle({ ...article, status: "hoax" });
        toast.error("Article Marked as Hoax", {
            description: "Article has been marked as hoax.",
        });
    };

    const handlePublish = () => {
        setArticle({ ...article, status: "published" });
        toast.success("Article Published", {
            description: "Article has been published to the main portal.",
        });
    };

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setArticle({ ...article, imageUrl: reader.result as string });
            };
            reader.readAsDataURL(file);
            toast("Image Updated", {
                description: "Featured image has been changed.",
            });
        }
    };

    return (
        <AdminLayout>
            <div className="space-y-6">
                <div className="flex items-center gap-4">
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => navigate("/scraped-news")}
                    >
                        <ArrowLeft className="h-5 w-5" />
                    </Button>
                    <div>
                        <h1 className="text-3xl font-bold text-foreground">Article Details</h1>
                        <p className="text-muted-foreground mt-1">Review and edit article (Timika)</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    <div className="lg:col-span-3 space-y-6">
                        <Card>
                            <CardHeader>
                                <div className="flex items-center justify-between">
                                    <CardTitle>Article Content</CardTitle>
                                    <StatusBadge status={article.status} />
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div>
                                    <Label htmlFor="title">Title</Label>
                                    <Input
                                        id="title"
                                        value={article.title}
                                        onChange={(e) =>
                                            setArticle({ ...article, title: e.target.value })
                                        }
                                        className="mt-1"
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="source">Source</Label>
                                        <Input
                                            id="source"
                                            value={article.source}
                                            onChange={(e) =>
                                                setArticle({ ...article, source: e.target.value })
                                            }
                                            className="mt-1"
                                        />
                                    </div>
                                    <div>
                                        <Label htmlFor="category">Category</Label>
                                        <Select
                                            value={article.category}
                                            onValueChange={(value) =>
                                                setArticle({ ...article, category: value })
                                            }
                                        >
                                            <SelectTrigger className="mt-1">
                                                <SelectValue placeholder="Select category" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="Infrastructure">Infrastructure</SelectItem>
                                                <SelectItem value="Economy">Economy</SelectItem>
                                                <SelectItem value="Education">Education</SelectItem>
                                                <SelectItem value="Health">Health</SelectItem>
                                                <SelectItem value="Environment">Environment</SelectItem>
                                                <SelectItem value="Politics">Politics</SelectItem>
                                                <SelectItem value="Culture">Culture</SelectItem>
                                                <SelectItem value="Sports">Sports</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </div>

                                <div>
                                    <Label htmlFor="content">Content</Label>
                                    <Textarea
                                        id="content"
                                        value={article.content}
                                        onChange={(e) =>
                                            setArticle({ ...article, content: e.target.value })
                                        }
                                        className="mt-1 min-h-[300px]"
                                    />
                                </div>

                                <div>
                                    <Label>Featured Image</Label>
                                    <div className="mt-2 rounded-lg overflow-hidden border border-border relative group">
                                        <img
                                            src={article.imageUrl}
                                            alt={article.title}
                                            className="w-full h-64 object-cover"
                                        />
                                        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                            <Button
                                                variant="secondary"
                                                size="sm"
                                                onClick={() => fileInputRef.current?.click()}
                                            >
                                                <ImageIcon className="mr-2 h-4 w-4" />
                                                Change Image
                                            </Button>
                                        </div>
                                    </div>
                                    <input
                                        ref={fileInputRef}
                                        type="file"
                                        accept="image/*"
                                        className="hidden"
                                        onChange={handleImageUpload}
                                    />
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    <div className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>Article Info</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div>
                                    <Label className="text-muted-foreground">Date Scraped</Label>
                                    <p className="font-medium mt-1">{article.date}</p>
                                </div>
                                <div>
                                    <Label className="text-muted-foreground">Status</Label>
                                    <div className="mt-1">
                                        <StatusBadge status={article.status} />
                                    </div>
                                </div>
                                <div>
                                    <Label className="text-muted-foreground">Category</Label>
                                    <p className="font-medium mt-1">{article.category}</p>
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Actions</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-3">
                                <Button
                                    className="w-full"
                                    variant="outline"
                                    onClick={handleSave}
                                >
                                    <Save className="mr-2 h-4 w-4" />
                                    Save Draft
                                </Button>
                                <Button
                                    className="w-full"
                                    variant="outline"
                                    onClick={handleVerify}
                                    disabled={article.status === "verified" || article.status === "published"}
                                >
                                    <CheckCircle className="mr-2 h-4 w-4" />
                                    Verify Article
                                </Button>
                                <Button
                                    className="w-full"
                                    variant="outline"
                                    onClick={handleMarkAsHoax}
                                    disabled={article.status === "hoax"}
                                >
                                    <AlertTriangle className="mr-2 h-4 w-4" />
                                    Mark as Hoax
                                </Button>
                                <Button
                                    className="w-full"
                                    onClick={handlePublish}
                                    disabled={article.status !== "verified"}
                                >
                                    <Upload className="mr-2 h-4 w-4" />
                                    Publish to Portal
                                </Button>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Related News</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-3">
                                {relatedNews.map((news) => (
                                    <div
                                        key={news.id}
                                        className="p-3 rounded-lg border border-border hover:bg-accent/50 cursor-pointer transition-colors"
                                        onClick={() => navigate(`/article/${news.id}`)}
                                    >
                                        <h4 className="font-medium text-sm line-clamp-2 mb-1">
                                            {news.title}
                                        </h4>
                                        <p className="text-xs text-muted-foreground">
                                            {news.source} • {news.date}
                                        </p>
                                    </div>
                                ))}
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </AdminLayout>
    );
}
