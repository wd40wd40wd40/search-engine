import Link from "next/link";
import { useEffect, useState } from "react";

interface SearchResultsProps {
  query: string;
}

interface APISearchResult {
  doc_id: string;
  score: number;
  title: string;
  snippet: string;
}

export function SearchResults({ query }: SearchResultsProps) {
  const [results, setResults] = useState<APISearchResult[]>([]);

  // For loading, will update later
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!query) return;

    setLoading(true);
    setError(null);

    fetch(`http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error. status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (data && Array.isArray(data.results)) {
          setResults(data.results);
        } else {
          setResults([]);
        }
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [query]);

  if (loading) {
    return (
      <div>
        <h1>Results loading</h1>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h1>Error: {error}</h1>
      </div>
    );
  }

  return (
    <div className='container mx-40 py-6 display-flex transition-all duration-300'>
      <p className='text-sm text-muted-foreground mb-4'>
        Found {results.length} results for &quot;{query}&quot;:
      </p>
      <div className='space-y-6'>
        {results.map((res, index) => (
          <div key={index} className='max-w-2xl'>
            <h2 className='text-lg font-medium text-primary mb-1 hover:underline'>
              <Link
                href={res.doc_id}
                className='visited:text-violet-900'
                target='_blank'
              >
                {res.title}
              </Link>
            </h2>
            <h4 className='text-lg font-medium text-primary mb-1'>
              Score: {res.score}
            </h4>
            <div
              className='text-xs text-muted-foreground mb-1'
              dangerouslySetInnerHTML={{ __html: res.snippet }}
            />
            <div className='text-xs text-muted-foreground mb-1'>
              {res.score}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
