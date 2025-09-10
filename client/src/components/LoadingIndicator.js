export default function LoadingIndicator() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-amber-500">
      <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-amber-600 border-solid"></div>
      <p className="mt-4 text-gray-900 font-semibold">Processing...</p>
    </div>
  );
}
