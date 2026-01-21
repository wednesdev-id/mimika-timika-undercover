import { Badge } from "@/shared/ui";

type ArticleStatus = "pending" | "verified" | "hoax" | "published";

const statusLabels: Record<ArticleStatus, string> = {
    pending: "Belum Disunting",
    verified: "Sudah Diverifikasi",
    hoax: "Hoax",
    published: "Sudah Dipublikasikan",
};

const statusColors: Record<ArticleStatus, string> = {
    pending: "bg-status-pending/20 text-status-pending border-status-pending/30 hover:bg-status-pending/30",
    verified: "bg-status-verified/20 text-status-verified border-status-verified/30 hover:bg-status-verified/30",
    hoax: "bg-status-hoax/20 text-status-hoax border-status-hoax/30 hover:bg-status-hoax/30",
    published: "bg-status-published/20 text-status-published border-status-published/30 hover:bg-status-published/30",
};

interface StatusBadgeProps {
    status: ArticleStatus | string;
    className?: string;
}

export const StatusBadge = ({ status, className }: StatusBadgeProps) => {
    const normalizedStatus = (status as ArticleStatus) || "pending";
    return (
        <Badge
            variant="outline"
            className={`${statusColors[normalizedStatus]} ${className}`}
        >
            {statusLabels[normalizedStatus] || status}
        </Badge>
    );
};
