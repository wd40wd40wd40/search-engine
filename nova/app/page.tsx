"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/toaster";
import { useToast } from "@/hooks/use-toast";
import { UserCircle, Paintbrush } from "lucide-react";
import { HeroLogo } from "@/components/HeroLogo";
import { PrimarySearchForm } from "@/components/PrimarySearchForm";
import { CustomizeSidebar } from "@/components/customize-sidebar";
import SettingsHomePage from "@/components/SettingsHomePage";

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
  const [maxPages, setMaxPages] = useState(1000);
  const [maxDepth, setMaxDepth] = useState(3);
  const [currentGradient, setCurrentGradient] = useState(-1);
  const [customizeOpen, setCustomizeOpen] = useState(false);
  const [customModeEnabled, setCustomModeEnabled] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [status, setStatus] = useState("");

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

  async function handleCrawl(e: React.FormEvent) {
    e.preventDefault();
    setStatus("Crawling...");

    try {
      const response = await fetch("http://127.0.0.1:8000/crawl", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: sourceURL,
          max_pages: maxPages,
          max_depth: maxDepth,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to crawl: ${response.status}`);
      }

      const data = await response.json();
      setStatus(
        `Success! ${data.message}. Indexed ${data.total_tokens} tokens.`
      );
    } catch (error: any) {
      console.error(error);
      setStatus(error.message);
    }
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();

    const trimmedSearch = searchQuery.trim();
    const trimmedSourceURL = sourceURL.trim();

    if (trimmedSearch && trimmedSourceURL) {
      try {
        // 1) Call your FastAPI crawler endpoint:
        const crawlRes = await fetch("http://127.0.0.1:8000/crawl", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            url: trimmedSourceURL,
            max_pages: maxPages, // or whatever defaults you want
            max_depth: maxDepth,
          }),
        });

        if (!crawlRes.ok) {
          // If the crawl fails, throw an error
          throw new Error(
            `Crawling failed with status code: ${crawlRes.status}`
          );
        }

        // 2) Crawl succeeded, continue with your existing flow
        const data = await crawlRes.json();
        console.log("Crawl success:", data);

        setSearchedQuery(trimmedSearch);
        const query = new URLSearchParams({
          searchedQuery: trimmedSearch,
          sourceURL: trimmedSourceURL,
        }).toString();
        router.push(`/results?${query}`);
      } catch (error: any) {
        console.error(error);
        toast({
          variant: "destructive",
          title: "Uh oh! Something went wrong.",
          description: error.message,
        });
      }
    }
    // If only the source URL is provided, no search query
    else if (trimmedSourceURL) {
      toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: "Search is empty.",
      });
    }
    // If only the search query is provided, no source URL
    else if (trimmedSearch) {
      toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: "No Source URL provided.",
      });
    }
    // If neither is provided
    else {
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
          <div className='container mx-auto px-4'>
            <div className='flex flex-col items-center space-y-10 py-16'>
              <div className='flex flex-row'>
                <HeroLogo />
                <SettingsHomePage
                  maxPages={maxPages}
                  setMaxPages={setMaxPages}
                  maxDepth={maxDepth}
                  setMaxDepth={setMaxDepth}
                />
              </div>
              <div className='w-full max-w-5xl flex flex-col'>
                <PrimarySearchForm
                  searchQuery={searchQuery}
                  setSearchQuery={setSearchQuery}
                  sourceURL={sourceURL}
                  setSourceURL={setSourceURL}
                  handleSearch={handleSearch}
                />
              </div>
            </div>
          </div>
        </div>
        <div className='fixed top-4 right-4'>
          <Button
            variant='ghost'
            size='icon'
            className='rounded-full bg-background/80 backdrop-blur-sm'
          >
            <UserCircle className='h-5 w-5' />
            <span className='sr-only'>Sign in</span>
          </Button>
        </div>

        <div className='fixed bottom-4 right-4'>
          <Button
            variant='ghost'
            size='icon'
            onClick={() => setCustomizeOpen(true)}
            className='rounded-full bg-background/80 backdrop-blur-sm'
          >
            <Paintbrush className='h-5 w-5' />
            <span className='sr-only'>Customize</span>
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
