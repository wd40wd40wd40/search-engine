"use client";

import { FormEvent } from "react";
import { Search, Globe } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface PrimarySearchFormProps {
  handleSearch: (e: FormEvent) => void;
  searchQuery: string;
  setSearchQuery: (val: string) => void;
  sourceURL: string;
  setSourceURL: (val: string) => void;
}

export function PrimarySearchForm({
  handleSearch,
  searchQuery,
  setSearchQuery,
  sourceURL,
  setSourceURL,
}: PrimarySearchFormProps) {
  return (
    <form onSubmit={handleSearch} className='space-y-8'>
      <div className='flex flex-row justify-center space-x-10'>
        <div className='relative w-1/2'>
          <Search className='absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4' />
          <Input
            type='text'
            placeholder='Search'
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className='pl-10 pr-4 py-6 rounded-full bg-background/80 placeholder:text-muted-foreground'
          />
        </div>

        <div className='relative w-1/2'>
          <Globe className='absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4' />
          <Input
            type='text'
            placeholder='Enter source URL'
            value={sourceURL}
            onChange={(e) => setSourceURL(e.target.value)}
            className='pl-10 pr-4 py-6 rounded-full bg-background/80 placeholder:text-muted-foreground'
          />
        </div>
      </div>

      <div className='flex flex-row justify-center w-full max-w-xs space-x-10 mx-auto'>
        <Button variant='outline' type='submit' className='w-1/2'>
          Search
        </Button>
        <Button variant='outline' className='w-1/2'>
          Feeling Lucky?
        </Button>
      </div>
    </form>
  );
}
