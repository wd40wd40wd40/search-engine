"use client";

import { FormEvent } from "react";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

interface ResultsSearchFormProps {
  handleSearch: (e: FormEvent) => void;
  searchQuery: string;
  setSearchQuery: (val: string) => void;
}

export function ResultsSearchForm({
  handleSearch,
  searchQuery,
  setSearchQuery,
}: ResultsSearchFormProps) {
  return (
    <form onSubmit={handleSearch} className="w-full max-w-2xl">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
        <Input
          type="text"
          placeholder="Search or type a URL"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10 pr-4 py-6 rounded-full bg-background/80 placeholder:text-muted-foreground"
        />
      </div>
    </form>
  );
}
