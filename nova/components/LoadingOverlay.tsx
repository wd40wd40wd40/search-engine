export function LoadingOverlay() {
  return (
    <div className='fixed inset-0 z-50 flex flex-col items-center justify-center bg-black/60 backdrop-blur-sm'>
      {/* Spinner */}
      <div className='h-12 w-12 border-4 border-t-transparent border-white rounded-full animate-spin' />
      <h2 className='mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0'>
        Crawling...
      </h2>
    </div>
  );
}
