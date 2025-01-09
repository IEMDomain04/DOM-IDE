import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// TITLE OF THE WEB APP
export const metadata: Metadata = {
  title: "DOM Compiler",
  description: "The DOM language IDE allows programming with a Jujutsu Kaisen-inspired theme (DOMAIN EXPANSION).",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <meta property="og:title" content="DOM Compiler" />
        <meta property="og:description" content="The DOM language IDE allows programming with a Jujutsu Kaisen-inspired theme (DOMAIN EXPANSION)." />
        <meta property="og:image" content="https://p325k7wa.twic.pics/high/jujutsu-kaisen/jujutsu-kaisen-cursed-clash/00-page-setup/JJK-header-mobile2.jpg?twic=v1/resize=760/step=10/quality=80" />
        <meta property="og:url" content="https://dom-ide.vercel.app/" />
        <link rel="icon" href="/dom-logo.ico" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}