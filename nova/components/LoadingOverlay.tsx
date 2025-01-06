export function LoadingOverlay() {
  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm'>
      {/* Spinner */}
      <div className='h-12 w-12 border-4 border-t-transparent border-white rounded-full animate-spin' />
    </div>
  );
}
