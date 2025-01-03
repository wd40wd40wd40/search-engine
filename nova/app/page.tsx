"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { CustomizeSidebar } from "@/components/customize-sidebar";
import { SearchResults } from "@/components/search-results";
import { Toaster } from "@/components/ui/toaster";

import { useToast } from "@/hooks/use-toast";

import { UserCircle, Paintbrush } from "lucide-react";
import { Search } from "lucide-react";

import { useTheme } from "next-themes";
import Image from "next/image";

import { HeroLogo } from "@/components/HeroLogo";
import { PrimarySearchForm } from "@/components/PrimarySearchForm";

const gradients = [
  "/images/Gradient-1.png",
  "/images/Gradient-2.png",
  "/images/Gradient-3.png",
  "/images/Gradient-4.png",
  "/images/Gradient-5.png",
];

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchedQuery, setSearchedQuery] = useState("");
  const [sourceURL, setSourceURL] = useState("");
  const [currentGradient, setCurrentGradient] = useState(-1);
  const [customizeOpen, setCustomizeOpen] = useState(false);
  const [customModeEnabled, setCustomModeEnabled] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  const { toast } = useToast();

  const router = useRouter();

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (hasSearched) {
      setCurrentGradient(-1);
      setCustomModeEnabled(false);
    }
  }, [hasSearched]);

  useEffect(() => {
    if (mounted) {
      if (hasSearched) {
        setCurrentGradient(-1);
        setCustomModeEnabled(false);
      }
    }
  }, [hasSearched, mounted]);

  if (!mounted) return null;

  const logoSrc =
    theme === "light"
      ? "/images/NOVA-Logo-Black-Big.png"
      : "/images/NOVA-Logo-White-Big.png";

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedSearch = searchQuery.trim();
    const trimmedSourceURL = sourceURL.trim();
    if (searchQuery.trim() && sourceURL.trim()) {
      setSearchedQuery(searchQuery);
      const query = new URLSearchParams({
        searchedQuery: trimmedSearch,
        sourceURL: trimmedSourceURL,
      }).toString();
      router.push(`/results?${query}`);
    } else if (sourceURL.trim()) {
      //no search query
      toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: "Search is empty.",
      });
    } else if (searchQuery.trim()) {
      //no sourceURL
      toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: "No Source URL provided.",
      });
    } else {
      toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: "No Search or Source URL provided.",
      });
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

  const resetSearch = () => {
    setSearchQuery("");
    setSearchedQuery("");
    setSourceURL("");
    setHasSearched(false);
  };

  return (
    <div
      className={`min-h-screen bg-cover bg-center transition-all duration-700`}
      style={{
        backgroundImage:
          currentGradient >= 0 && customModeEnabled && !hasSearched
            ? `url(/images/gradient-${currentGradient + 1}.png)`
            : "none",
      }}
    >
      <div
        className={`min-h-screen backdrop-blur-[2px] flex flex-col transition-all duration-500 ${
          customizeOpen ? "mr-[250px]" : ""
        }`}
      >
        <div
          className={`w-full transition-all duration-500 ${
            hasSearched ? "bg-background/80 backdrop-blur-sm" : ""
          }`}
        >
          <div className="container mx-auto px-4">
            {!hasSearched ? (
              <div className="flex flex-col items-center space-y-10 py-16">
                <HeroLogo />
                <div className="w-full max-w-5xl flex flex-col">
                  <PrimarySearchForm
                    searchQuery={searchQuery}
                    setSearchQuery={setSearchQuery}
                    sourceURL={sourceURL}
                    setSourceURL={setSourceURL}
                    handleSearch={handleSearch}
                  />
                </div>
              </div>
            ) : (
              <div className="py-4 pl-0.5">
                <div className="flex items-center gap-4">
                  <button
                    onClick={resetSearch}
                    className="h-12 relative shrink-0"
                  >
                    <Image
                      src={logoSrc}
                      alt="Nova"
                      width={96}
                      height={48}
                      className="object-contain transition-opacity duration-700"
                      priority
                    />
                  </button>

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
            )}
          </div>
        </div>

        {hasSearched && <SearchResults query={searchedQuery} />}

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
