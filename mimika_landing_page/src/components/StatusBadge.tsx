import { Badge } from "@/shared/ui";
import { cn } from "@/lib/utils";

type Status = "pending" | "verified" | "hoax" | "published";

interface StatusBadgeProps {
  status: Status;
}

const statusConfig = {
  pending: {
    label: "Pending Review",
    className: "bg-status-pending/20 text-status-pending border-status-pending/30",
  },
  verified: {
    label: "Verified",
    className: "bg-status-verified/20 text-status-verified border-status-verified/30",
  },
  hoax: {
    label: "Hoax",
    className: "bg-status-hoax/20 text-status-hoax border-status-hoax/30",
  },
  published: {
    label: "Published",
    className: "bg-status-published/20 text-status-published border-status-published/30",
  },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];
  
  return (
    <Badge variant="outline" className={cn("font-medium", config.className)}>
      {config.label}
    </Badge>
  );
}
