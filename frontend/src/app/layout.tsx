import React from "react";
import { Montserrat, Karla } from "next/font/google";
import "../components/globals.css";
import {Header} from "@/components";

const montserrat = Montserrat({
  subsets: ["latin"],
  display: 'swap',
  variable: '--font-montserrat'
});

const karla = Karla({
  subsets: ["latin"],
  display: 'swap',
  variable: '--font-karla'
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning={true} className={`${montserrat.variable} ${karla.variable}`}>
      <body suppressHydrationWarning={true}>
        <Header />
        {children}
      </body>
    </html>
  );
}
