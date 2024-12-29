"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import { useTheme } from "next-themes";

import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";

export default function resultsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchedQuery, setSearchedQuery] = useState("");
  const [sourceURL, setSourceURL] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const { theme } = useTheme();

  const resetSearch = () => {
    setSearchQuery("");
    setSearchedQuery("");
    setSourceURL("");
    setHasSearched(false);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault;
    if (searchQuery.trim()) {
      setSearchedQuery(searchQuery);
    }
  };

  return (
    <div className='py-4 pl-0.5'>
      <div className='flex items-center gap-4'>
        <button onClick={resetSearch} className='h-12 relative shrink-0'>
          <Image
            src={
              theme === "light"
                ? "/images/NOVA-Logo-Black-Big.png"
                : "/images/NOVA-Logo-White-Big.png"
            }
            alt='Nova'
            width={96}
            height={48}
            className='object-contain transition-opacity duration-700'
            priority
          />
        </button>

        <form onSubmit={handleSearch} className='w-full max-w-2xl'>
          <div className='relative'>
            <Search className='absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4' />
            <Input
              type='text'
              placeholder='Search or type a URL'
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className='pl-10 pr-4 py-6 rounded-full bg-background/80 placeholder:text-muted-foreground'
            />
          </div>
        </form>
      </div>
    </div>

    // {hasSearched && <SearchResults query={searchedQuery} />}
  );
}
