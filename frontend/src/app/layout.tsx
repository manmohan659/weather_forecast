import '@/app/globals.css'
import { Inter } from 'next/font/google'
import { QueryProvider } from '@/lib/providers/query-provider'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Weather Forecast App',
  description: 'Advanced weather forecasting system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryProvider>
          {children}
        </QueryProvider>
      </body>
    </html>
  )
}