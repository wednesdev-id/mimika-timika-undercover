import {
    LayoutDashboard,
    FileText,
    CheckCircle,
    Upload,
    BarChart3,
    Settings
} from "lucide-react";
import { NavLink } from "./NavLink";
import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    useSidebar,
} from "@undercover/ui-react";

const menuItems = [
    { title: "Dashboard", url: "/dashboard", icon: LayoutDashboard },
    { title: "Scraped News", url: "/scraped-news", icon: FileText },
    { title: "Verified News", url: "/verified-news", icon: CheckCircle },
    { title: "Publish", url: "/publish", icon: Upload },
    { title: "Analytics", url: "/analytics", icon: BarChart3 },
    { title: "Settings", url: "/settings", icon: Settings },
];

export function AdminSidebar() {
    const { state } = useSidebar();
    const collapsed = state === "collapsed";

    return (
        <Sidebar className={collapsed ? "w-16" : "w-64"}>
            <div className="px-6 py-4 border-b border-sidebar-border">
                {!collapsed && (
                    <h1 className="text-xl font-bold text-sidebar-foreground">
                        Timika Undercover
                    </h1>
                )}
                {collapsed && (
                    <div className="text-xl font-bold text-sidebar-foreground text-center">
                        TU
                    </div>
                )}
            </div>

            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {menuItems.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton asChild>
                                        <NavLink
                                            to={item.url}
                                            className="flex items-center gap-3 px-3 py-2 rounded-md transition-colors hover:bg-sidebar-accent"
                                            activeClassName="bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                                        >
                                            <item.icon className="h-5 w-5 flex-shrink-0" />
                                            {!collapsed && <span>{item.title}</span>}
                                        </NavLink>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
        </Sidebar>
    );
}
