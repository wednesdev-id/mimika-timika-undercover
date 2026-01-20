import { AdminLayout } from "@/components/AdminLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui";
import { Label } from "@/shared/ui";
import { Input } from "@/shared/ui";
import { Button } from "@/shared/ui";
import { Switch } from "@/shared/ui";
import { toast } from "@/shared/ui";

export default function Settings() {

  const handleSave = () => {
    toast.success("Settings Saved", {
      description: "Your settings have been updated successfully.",
    });
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Settings</h1>
          <p className="text-muted-foreground mt-1">
            Configure your dashboard preferences
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>General Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="portal-name">Portal Name</Label>
                <Input
                  id="portal-name"
                  defaultValue="Timika News Portal"
                  placeholder="Enter portal name"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="portal-url">Portal URL</Label>
                <Input
                  id="portal-url"
                  defaultValue="https://timikanews.com"
                  placeholder="Enter portal URL"
                />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Auto-publish verified articles</Label>
                  <p className="text-sm text-muted-foreground">
                    Automatically publish articles after verification
                  </p>
                </div>
                <Switch />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Notification Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Email notifications</Label>
                  <p className="text-sm text-muted-foreground">
                    Receive email for new scraped articles
                  </p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Hoax detection alerts</Label>
                  <p className="text-sm text-muted-foreground">
                    Get notified when potential hoax is detected
                  </p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Daily summary</Label>
                  <p className="text-sm text-muted-foreground">
                    Receive daily summary of articles
                  </p>
                </div>
                <Switch />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Scraper Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="scrape-interval">Scraping Interval (minutes)</Label>
                <Input
                  id="scrape-interval"
                  type="number"
                  defaultValue="30"
                  placeholder="Enter interval"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="max-articles">Max Articles per Run</Label>
                <Input
                  id="max-articles"
                  type="number"
                  defaultValue="50"
                  placeholder="Enter max articles"
                />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Enable scraper</Label>
                  <p className="text-sm text-muted-foreground">
                    Turn on/off automatic scraping
                  </p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Account Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="user-name">Full Name</Label>
                <Input
                  id="user-name"
                  defaultValue="Admin User"
                  placeholder="Enter your name"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="user-email">Email</Label>
                <Input
                  id="user-email"
                  type="email"
                  defaultValue="admin@timikanews.com"
                  placeholder="Enter your email"
                />
              </div>
              <Button variant="outline" className="w-full">
                Change Password
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="flex justify-end">
          <Button onClick={handleSave} size="lg">
            Save All Settings
          </Button>
        </div>
      </div>
    </AdminLayout>
  );
}
