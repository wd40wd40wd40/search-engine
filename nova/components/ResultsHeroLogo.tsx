"use client";

import { useTheme } from "next-themes";
import Image from "next/image";

interface ResultsHeroLogoProps {
  className?: string;
  resetSearch: () => void;
}

export function ResultsHeroLogo({
  className,
  resetSearch,
}: ResultsHeroLogoProps) {
  const { theme } = useTheme();

  return (
    <button onClick={resetSearch} className="h-12 relative shrink-0">
      <Image
        src={
          theme === "light"
            ? "/images/NOVA-Logo-Black-Big.png"
            : "/images/NOVA-Logo-White-Big.png"
        }
        alt="Nova"
        width={96}
        height={48}
        className="object-contain transition-opacity duration-700"
        priority
      />
    </button>
  );
}
