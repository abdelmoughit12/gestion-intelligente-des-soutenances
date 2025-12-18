import Link from 'next/link'
import { Button } from '@/components/ui/button'
import Image from 'next/image'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <Image
          src="/images/logov2.svg"
          alt="Logo"
          width={200}
          height={200}
          className="mx-auto mb-8"
        />
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Thesis Defense Management System
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Manage thesis defenses, jury assignments, and evaluations
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/student">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
              Student Portal
            </Button>
          </Link>
          <Link href="/professor/dashboard">
            <Button size="lg" variant="outline">
              Professor Space
            </Button>
          </Link>
          <Link href="/dashboard">
            <Button size="lg" variant="outline">
              Manager Dashboard
            </Button>
          </Link>
        </div>
        <p className="mt-8 text-sm text-gray-500">
          Authentication system coming soon...
        </p>
      </div>
    </div>
  )
}


