import type { Metadata } from 'next'
import { DM_Sans } from 'next/font/google'
import { Toaster } from "@/components/ui/sonner"
import './globals.css'

const dmSans = DM_Sans({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Soutenance Manager - Student Dashboard',
  description: 'Manage your soutenance requests and track their status',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={dmSans.className}>
        {children}
        <Toaster />
      </body>
    </html>
  )
}

