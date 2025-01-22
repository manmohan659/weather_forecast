import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="flex flex-col items-center gap-8">
        <h1 className="text-4xl font-bold">Weather Forecast Dashboard</h1>
        <Link 
          href="/dashboard" 
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
        >
          Go to Dashboard
        </Link>
      </div>
    </main>
  )
}