'use client'

import { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { MoonIcon, SunIcon } from "@radix-ui/react-icons"
import { useTheme } from "next-themes"

function SearchResults({ results }: { results: string[] }) {
  return (
    <div className="mt-8 space-y-4">
      {results.map((result, index) => (
        <Card key={index}>
          <CardHeader>
            <CardTitle>Result {index + 1}</CardTitle>
            <CardDescription>{result}</CardDescription>
          </CardHeader>
        </Card>
      ))}
    </div>
  )
}

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<string[]>([])
  const { theme, setTheme } = useTheme()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // Simulating search results
    setSearchResults([
      `Result for "${searchQuery}" 1`,
      `Result for "${searchQuery}" 2`,
      `Result for "${searchQuery}" 3`,
    ])
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <main className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold">Nova Search</h1>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
          >
            {theme === 'light' ? <MoonIcon className="h-6 w-6" /> : <SunIcon className="h-6 w-6" />}
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
        <form onSubmit={handleSearch} className="flex gap-2">
          <Input
            type="text"
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-grow"
          />
          <Button type="submit">Search</Button>
        </form>
        <SearchResults results={searchResults} />
      </main>
    </div>
  )
}

