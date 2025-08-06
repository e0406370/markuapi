### Purpose

A basic web scraper API for [Filmarks Dramas (フィルマークス・ドラマ)](https://filmarks.com/dramas).

Note:
This API is currently under development.
Only two endpoints have been implemented thus far.

---

### API Base URL

```sh
https://markuapi.onrender.com/
```

---

### API Endpoints

- Retrieve drama information

```sh
GET /dramas/{series_id}/{season_id}
```

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
