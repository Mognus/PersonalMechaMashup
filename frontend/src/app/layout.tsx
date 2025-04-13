// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import { Inter as FontSans } from "next/font/google"; // Or choose a more "techy" font if you like
import "./globals.css"; // Tailwind styles
import { cn } from "@/lib/utils";
import Sidebar from "@/components/layout/Sidebar";

// Load the font with specific settings
const fontSans = FontSans({
  subsets: ["latin"],
  variable: "--font-sans", // CSS variable for Tailwind
});

// Basic metadata for the site
export const metadata: Metadata = {
  title: "Mech Mashup", // Change to your desired title
  description: "Personal Mashup Site - Mech Cockpit Style", // Change description
};

export default function RootLayout({
  children, // This will be the content of the specific page being rendered
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning> {/* suppressHydrationWarning often needed with themes/dark mode */}
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased flex", // Basic styling, flex container
          fontSans.variable // Apply the font variable
        )}
      >
        {/* Static Sidebar - Adjust width (w-64) as needed */}
        <aside className="w-64 border-r border-border bg-muted/40 hidden md:block"> {/* Hide on small screens */}
          <Sidebar /> {/* Render the Sidebar component */}
        </aside>

        {/* Main content area */}
        <main className="flex-1 flex flex-col"> {/* Takes remaining space, allows vertical flex */}
          {/* Optional: Header component could go here */}
          {/* <header className="p-4 border-b border-border">Header Content</header> */}

          {/* Page content */}
          <div className="flex-1 p-6"> {/* Padding around the page content */}
            {children} {/* Render the actual page content */}
          </div>

          {/* Optional: Footer or other layout elements */}
        </main>

        {/* Optional: Mobile Navigation (e.g., using ShadCN Sheet) */}
        {/* Could be triggered by a button in a mobile header */}

      </body>
    </html>
  );
}