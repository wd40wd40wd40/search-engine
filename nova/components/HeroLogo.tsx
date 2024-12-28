"use client";

import { useTheme } from "next-themes";
import Image from "next/image";

interface HeroLogoProps {
  className?: string;
}

export function HeroLogo({ className }: HeroLogoProps) {
  const { theme } = useTheme();

  return (
    <div className='w-80 h-20 relative'>
      <Image
        src={
          theme === "light"
            ? "/images/NOVA-Logo-Black-Big.png"
            : "/images/NOVA-Logo-White-Big.png"
        }
        alt='Nova'
        fill
        className='object-contain transition-opacity duration-700'
        priority
      />
    </div>
  );
}
