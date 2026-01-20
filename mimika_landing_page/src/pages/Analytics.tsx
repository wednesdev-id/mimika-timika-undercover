import { AdminLayout } from "@/components/AdminLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const monthlyData = [
  { month: "Jul", pending: 15, verified: 45, hoax: 3, published: 40 },
  { month: "Aug", pending: 22, verified: 52, hoax: 5, published: 48 },
  { month: "Sep", pending: 18, verified: 48, hoax: 2, published: 45 },
  { month: "Oct", pending: 25, verified: 55, hoax: 4, published: 52 },
  { month: "Nov", pending: 20, verified: 60, hoax: 6, published: 55 },
  { month: "Dec", pending: 28, verified: 58, hoax: 3, published: 54 },
  { month: "Jan", pending: 24, verified: 56, hoax: 8, published: 42 },
];

const weeklyPublished = [
  { week: "Week 1", articles: 12 },
  { week: "Week 2", articles: 15 },
  { week: "Week 3", articles: 10 },
  { week: "Week 4", articles: 18 },
];

export default function Analytics() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Analytics</h1>
          <p className="text-muted-foreground mt-1">
            Track article trends and performance metrics
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Articles by Status (Monthly)</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="pending"
                    stroke="hsl(var(--status-pending))"
                    name="Pending"
                  />
                  <Line
                    type="monotone"
                    dataKey="verified"
                    stroke="hsl(var(--status-verified))"
                    name="Verified"
                  />
                  <Line
                    type="monotone"
                    dataKey="hoax"
                    stroke="hsl(var(--status-hoax))"
                    name="Hoax"
                  />
                  <Line
                    type="monotone"
                    dataKey="published"
                    stroke="hsl(var(--status-published))"
                    name="Published"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Published Articles (This Month)</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={weeklyPublished}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar
                    dataKey="articles"
                    fill="hsl(var(--primary))"
                    name="Published Articles"
                  />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Source Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-medium">Portal Berita Timika</span>
                <div className="flex items-center gap-4">
                  <div className="w-64 bg-muted rounded-full h-2">
                    <div
                      className="bg-primary h-2 rounded-full"
                      style={{ width: "65%" }}
                    />
                  </div>
                  <span className="text-sm text-muted-foreground w-12 text-right">
                    65%
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-medium">Mimika News</span>
                <div className="flex items-center gap-4">
                  <div className="w-64 bg-muted rounded-full h-2">
                    <div
                      className="bg-secondary h-2 rounded-full"
                      style={{ width: "20%" }}
                    />
                  </div>
                  <span className="text-sm text-muted-foreground w-12 text-right">
                    20%
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-medium">Kompas Papua</span>
                <div className="flex items-center gap-4">
                  <div className="w-64 bg-muted rounded-full h-2">
                    <div
                      className="bg-accent h-2 rounded-full"
                      style={{ width: "10%" }}
                    />
                  </div>
                  <span className="text-sm text-muted-foreground w-12 text-right">
                    10%
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-medium">Other Sources</span>
                <div className="flex items-center gap-4">
                  <div className="w-64 bg-muted rounded-full h-2">
                    <div
                      className="bg-muted-foreground h-2 rounded-full"
                      style={{ width: "5%" }}
                    />
                  </div>
                  <span className="text-sm text-muted-foreground w-12 text-right">
                    5%
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
}
