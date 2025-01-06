"use client";

import { Popover, PopoverTrigger, PopoverContent } from "./ui/popover";
import { Button } from "./ui/button";
import { Settings } from "lucide-react";
import { Label } from "./ui/label";
import { Input } from "./ui/input";

interface SettingsHomePageProps {
  maxPages: number;
  setMaxPages: (val: number) => void;
  maxDepth: number;
  setMaxDepth: (val: number) => void;
}

export default function SettingsHomePage({
  maxPages,
  setMaxPages,
  maxDepth,
  setMaxDepth,
}: SettingsHomePageProps) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant='outline' size='icon'>
          <Settings></Settings>
        </Button>
      </PopoverTrigger>
      <PopoverContent className='w-80'>
        <div className='grid gap-4'>
          <div className='space-y-2'>
            <h4 className='font-medium leading-none'>Configuration</h4>
          </div>
          <div className='grid gap-2'>
            <div className='grid grid-cols-3 items-center gap-4'>
              <Label htmlFor='max_pages'>Max Pages</Label>
              <Input
                type='number'
                value={maxPages}
                onChange={(e) => setMaxPages(e.target.valueAsNumber)}
              />
            </div>
          </div>
          <div className='grid gap-2'>
            <div className='grid grid-cols-3 items-center gap-4'>
              <Label htmlFor='max_depth'>Max Depth</Label>
              <Input
                type='number'
                value={maxDepth}
                onChange={(e) => setMaxDepth(e.target.valueAsNumber)}
              />
            </div>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
