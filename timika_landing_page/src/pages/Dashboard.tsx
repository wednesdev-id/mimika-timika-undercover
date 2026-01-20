import { AdminLayout } from "@/components/AdminLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@undercover/ui-react";
import { FileText, CheckCircle, AlertTriangle, Newspaper } from "lucide-react";

const stats = [
    {
        title: "Pending Review",
        value: "24",
        icon: FileText,
        color: "text-status-pending",
        bgColor: "bg-status-pending/10",
    },
    {
        title: "Verified",
        value: "156",
        icon: CheckCircle,
        color: "text-status-verified",
        bgColor: "bg-status-verified/10",
    },
    {
        title: "Hoax",
        value: "8",
        icon: AlertTriangle,
        color: "text-status-hoax",
        bgColor: "bg-status-hoax/10",
    },
    {
        title: "Published",
        value: "142",
        icon: Newspaper,
        color: "text-status-published",
        bgColor: "bg-status-published/10",
    },
];

export default function Dashboard() {
    return (
        <AdminLayout>
            <div className="space-y-6">
                <div>
                    <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
                    <p className="text-muted-foreground mt-1">
                        Overview of news articles management
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {stats.map((stat) => (
                        <Card key={stat.title}>
                            <CardHeader className="flex flex-row items-center justify-between pb-2">
                                <CardTitle className="text-sm font-medium text-muted-foreground">
                                    {stat.title}
                                </CardTitle>
                                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                                    <stat.icon className={`h-5 w-5 ${stat.color}`} />
                                </div>
                            </CardHeader>
                            <CardContent>
                                <div className="text-3xl font-bold">{stat.value}</div>
                            </CardContent>
                        </Card>
                    ))}
                </div>

                <Card>
                    <CardHeader>
                        <CardTitle>Recent Activity</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div className="flex items-center justify-between py-3 border-b border-border">
                                <div>
                                    <p className="font-medium">New article scraped from Portal Berita Timika</p>
                                    <p className="text-sm text-muted-foreground">2 minutes ago</p>
                                </div>
                                <span className="text-status-pending text-sm font-medium">Pending</span>
                            </div>
                            <div className="flex items-center justify-between py-3 border-b border-border">
                                <div>
                                    <p className="font-medium">Article verified: "Pembangunan Jalan Trans Papua"</p>
                                    <p className="text-sm text-muted-foreground">15 minutes ago</p>
                                </div>
                                <span className="text-status-verified text-sm font-medium">Verified</span>
                            </div>
                            <div className="flex items-center justify-between py-3 border-b border-border">
                                <div>
                                    <p className="font-medium">Article published: "Festival Budaya Timika 2024"</p>
                                    <p className="text-sm text-muted-foreground">1 hour ago</p>
                                </div>
                                <span className="text-status-published text-sm font-medium">Published</span>
                            </div>
                            <div className="flex items-center justify-between py-3">
                                <div>
                                    <p className="font-medium">Article marked as hoax: False claim about mining</p>
                                    <p className="text-sm text-muted-foreground">2 hours ago</p>
                                </div>
                                <span className="text-status-hoax text-sm font-medium">Hoax</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </AdminLayout>
    );
}
