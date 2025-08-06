### Purpose

A basic web scraper API for [Filmarks Dramas](https://filmarks.com/dramas).

Note:
This API is currently under development. 
Only one endpoint has been implemented thus far.

---

### API

- Search for dramas

```sh
GET /search/dramas?q={query}
```

Optional parameters:
- `limit`
  - Default: `10`
  - Range: `1` to `1000`
  - Limits the number of results returned.
    - If the specified limit exceeds the number of available results, only the available results are returned.

- `page`
  - Default: `1`
  - Range: `1` to `1000`
  - Fetches results from the corresponding page of search results.
    - If the specified page has no results, an empty list will be returned.