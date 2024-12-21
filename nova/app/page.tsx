"use client";

import React, { useState, Component } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { MoonIcon, SunIcon, UserCircle } from "lucide-react";
import { useTheme } from "next-themes";
import { Search } from "lucide-react";
import Image from "next/image";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const { theme, setTheme } = useTheme();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      console.log(`Searching for: ${searchQuery}`);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col items-center">
      <main className="container mx-auto px-4 py-16 flex flex-col items-center">
        <div className="w-64 h-16 relative mb-8">
          <Image
            src={
              theme === "light"
                ? "/images/nova-logo-black.png"
                : "/images/nova-logo-white.png"
            }
            alt="Nova"
            fill
            className="object-contain"
            priority
          />
        </div>
        <form onSubmit={handleSearch} className="w-full max-w-2xl">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              type="text"
              placeholder="Search or type a URL"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-6 rounded-full"
            />
          </div>
        </form>
      </main>
      <div className="fixed top-4 right-4 flex items-center space-x-2">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === "light" ? "dark" : "light")}
          className="rounded-full"
        >
          {theme === "light" ? (
            <MoonIcon className="h-5 w-5" />
          ) : (
            <SunIcon className="h-5 w-5" />
          )}
          <span className="sr-only">Toggle theme</span>
        </Button>
        <Button variant="ghost" size="icon" className="rounded-full">
          <UserCircle className="h-5 w-5" />
          <span className="sr-only">Sign in</span>
        </Button>
      </div>
    </div>
  );
}
