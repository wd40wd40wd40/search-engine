'use client'

import Image from 'next/image'
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet"

interface CustomizeSidebarProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onGradientSelect: (index: number) => void
  currentGradient: number
  customModeEnabled: boolean
  onCustomModeChange: (enabled: boolean) => void
}

const gradientIcons = [
  "/images/Gradient-Icon-1.png",
  "/images/Gradient-Icon-2.png",
  "/images/Gradient-Icon-3.png",
  "/images/Gradient-Icon-4.png",
  "/images/Gradient-Icon-5.png",
  "/images/Gradient-Icon-6.png",
  "/images/Gradient-Icon-7.png",
  "/images/Gradient-Icon-8.png",
]

export function CustomizeSidebar({ 
  open, 
  onOpenChange, 
  onGradientSelect,
  currentGradient,
  customModeEnabled,
  onCustomModeChange
}: CustomizeSidebarProps) {
  const { theme, setTheme } = useTheme()

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="w-[200px] sm:w-[250px] border-l">
        <SheetHeader>
          <SheetTitle>Customize</SheetTitle>
        </SheetHeader>
        
        <div className="py-6">
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4">Default</h3>
            <div className="flex items-center space-x-2">
              <Switch
                id="theme-mode"
                checked={theme === 'dark'}
                onCheckedChange={(checked) => setTheme(checked ? 'dark' : 'light')}
              />
              <Label htmlFor="theme-mode">Light/Dark Mode</Label>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Custom</h3>
            <div className="flex items-center space-x-2 mb-4">
              <Switch
                id="custom-mode"
                checked={customModeEnabled}
                onCheckedChange={onCustomModeChange}
              />
              <Label htmlFor="custom-mode">Gradients</Label>
            </div>
            <div className={`grid grid-cols-2 gap-2 ${customModeEnabled ? '' : 'opacity-50 pointer-events-none'}`}>
              {gradientIcons.map((icon, index) => (
                <button
                  key={index}
                  onClick={() => onGradientSelect(index)}
                  className={`relative aspect-square rounded-xl overflow-hidden border-2 transition-all ${
                    currentGradient === index 
                      ? 'border-primary scale-95' 
                      : 'border-transparent hover:scale-95'
                  }`}
                  disabled={!customModeEnabled}
                >
                  <Image
                    src={icon}
                    alt={`Gradient ${index + 1}`}
                    fill
                    className="object-cover"
                  />
                </button>
              ))}
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  )
}

