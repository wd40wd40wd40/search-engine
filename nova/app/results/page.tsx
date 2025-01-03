"use client";

import { useState, useEffect } from "react";

import Image from "next/image";
import { useTheme } from "next-themes";
import { useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";

import { Search } from "lucide-react";
import { UserCircle, Paintbrush } from "lucide-react";

import { SearchResults } from "@/components/search-results";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { CustomizeSidebar } from "@/components/customize-sidebar";
import { Toaster } from "@/components/ui/toaster";
import { ResultsHeroLogo } from "../ResultsHeroLogo";

export default function ResultsPage() {
  const searchParams = useSearchParams(); // for extracting search and url from home page

  const searchedQuery = searchParams.get("searchedQuery") || "";
  const sourceURL = searchParams.get("sourceURL") || "";

  const [searchQuery, setSearchQuery] = useState("");
  const [currentGradient, setCurrentGradient] = useState(-1);
  const [customModeEnabled, setCustomModeEnabled] = useState(false);
  const [customizeOpen, setCustomizeOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  const { theme } = useTheme();

  const router = useRouter();

  const resetSearch = () => {
    router.push("/");
  };

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedSearch = searchQuery.trim();
    if (searchQuery.trim()) {
      const query = new URLSearchParams({
        searchedQuery: trimmedSearch,
        sourceURL: sourceURL,
      }).toString();
      router.push(`/results?${query}`);
    }
  };

  const handleGradientSelect = (index: number) => {
    if (customModeEnabled) {
      setCurrentGradient(index);
    }
  };

  const handleCustomModeChange = (enabled: boolean) => {
    setCustomModeEnabled(enabled);
    if (!enabled) {
      setCurrentGradient(-1);
    }
  };

  return (
    <div
      className={`min-h-screen bg-cover bg-center transition-all duration-700`}
      style={{
        backgroundImage:
          currentGradient >= 0 && customModeEnabled
            ? `url(/images/gradient-${currentGradient + 1}.png)`
            : "none",
      }}
    >
      <div
        className={`min-h-screen backdrop-blur-[2px] flex flex-col transition-all duration-500 ${
          customizeOpen ? "mr-[250px]" : ""
        }`}
      >
        <div className="py-4 pl-5">
          <div className="flex items-center gap-4">
            <ResultsHeroLogo resetSearch={resetSearch} />
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
          </div>
        </div>
        <SearchResults query={searchedQuery} />

        <div className="fixed top-4 right-4">
          <Button
            variant="ghost"
            size="icon"
            className="rounded-full bg-background/80 backdrop-blur-sm"
          >
            <UserCircle className="h-5 w-5" />
            <span className="sr-only">Sign in</span>
          </Button>
        </div>

        <div className="fixed bottom-4 right-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCustomizeOpen(true)}
            className="rounded-full bg-background/80 backdrop-blur-sm"
          >
            <Paintbrush className="h-5 w-5" />
            <span className="sr-only">Customize</span>
          </Button>
        </div>

        <CustomizeSidebar
          open={customizeOpen}
          onOpenChange={setCustomizeOpen}
          onGradientSelect={handleGradientSelect}
          currentGradient={currentGradient}
          customModeEnabled={customModeEnabled}
          onCustomModeChange={handleCustomModeChange}
        />
      </div>
      <Toaster />
    </div>
  );
}
