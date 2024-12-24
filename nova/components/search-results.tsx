interface SearchResultsProps {
  query: string
}

export function SearchResults({ query }: SearchResultsProps) {
  // Placeholder results - now using the passed query that only updates on form submit
  const results = [
    {
      title: `Example Search Result for "${query}"`,
      url: "https://example.com/1",
      description: `This is a placeholder result that matches your search for "${query}". It demonstrates how search results will appear once the web crawler is implemented.`
    },
    {
      title: "Related Search Result",
      url: "https://example.com/2",
      description: "Another placeholder result showing how multiple search results will be displayed in a list format."
    },
    {
      title: "Additional Search Result",
      url: "https://example.com/3",
      description: "A third placeholder result to demonstrate the layout and styling of search results in the Nova search engine."
    }
  ]

  return (
    <div className="container mx-auto px-4 py-6">
      <p className="text-sm text-muted-foreground mb-4">
        About {results.length} results
      </p>
      <div className="space-y-6">
        {results.map((result, index) => (
          <div key={index} className="max-w-2xl">
            <a 
              href={result.url}
              className="group block"
            >
              <div className="text-xs text-muted-foreground mb-1">
                {result.url}
              </div>
              <h2 className="text-lg font-medium text-primary group-hover:underline mb-1">
                {result.title}
              </h2>
              <p className="text-sm text-muted-foreground">
                {result.description}
              </p>
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}

