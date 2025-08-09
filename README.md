### Purpose

A basic web scraper API for [Filmarks Dramas (フィルマークス・ドラマ)](https://filmarks.com/dramas).

- Base URL:
```sh
https://markuapi.onrender.com/
```

---

### API Endpoints

- Search for dramas

```sh
GET /search/dramas?q={query}
```

Searches for dramas on Filmarks, by title or keyword.

Supports optional query parameters: `limit` and `page`.

<br />

- Retrieve drama information

```sh
GET /dramas/{series_id}/{season_id}
```

Retrieves details for a specific drama on Filmarks, given the Series ID and Season ID.

<br />

- Fetch trending dramas

```sh
GET /list-drama/trend
```

Fetches dramas that are currently trending on Filmarks.

Supports optional query parameters: `limit` and `page`.

<br />

- Fetch trending dramas produced in a specific country

```sh
GET /list-drama/country/{country_id}
```

Fetches dramas that are currently trending on Filmarks, produced in the specified country.

A list mapping `country_id` to countries can be found [here](./tests/___country_id.json).

Supports optional query parameters: `limit` and `page`.

<br />

- Fetch trending dramas released in a specific year

```sh
GET /list-drama/year/{year}
```

Fetches dramas that are currently trending on Filmarks, released in the specified year.

A list of all available years can be found [here](./tests/___year_id.txt).

Supports optional query parameters: `limit` and `page`.

<br />

#### Optional Query Parameters

- `limit` (default `10`, range: `1` - `1000`): 
  - Specifies the **maximum** number of results to return.

- `page` (default `1`, range: `1` - `1000`):
  - Specifies the **page number** used for pagination.
