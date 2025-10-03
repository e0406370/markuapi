## markuapi

[![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white&label=Python)](https://www.python.org/downloads/release/python-3120/)
[![Coverage](https://img.shields.io/badge/coverage-99%25-blue?logo=python&logoColor=white&label=Coverage)](https://markuapi-coverage-report.vercel.app/)
[![license](https://img.shields.io/github/license/e0406370/markuapi)](https://github.com/e0406370/markuapi/blob/main/LICENSE)
[![Run-tests-using-Pytest](https://github.com/e0406370/markuapi/actions/workflows/test.yml/badge.svg)](https://github.com/e0406370/markuapi/actions/workflows/test.yml)

### Purpose

`markuapi` is a serverless web scraper API providing structured access to **info**, **list**, **review**, and **search** endpoints for:
- [Filmarks Animes (フィルマークス・アニメ)](https://filmarks.com/animes)
- [Filmarks Dramas (フィルマークス・ドラマ)](https://filmarks.com/dramas)
- [Filmarks Movies (フィルマークス・映画)](https://filmarks.com)

---

### API

#### Leapcell (Primary)
- Base URL:
  ```sh
  https://markuapi.apn.leapcell.app
  ```

- Redis caching of responses is implemented.

- [Swagger](https://markuapi.apn.leapcell.app/docs)

#### Vercel (Secondary)
- Base URL:
  ```sh
  https://markuapi.vercel.app
  ```

- Redis caching of responses is **NOT** implemented.

- [Swagger](https://markuapi.vercel.app/docs)

Refer to the Swagger UI for the complete API documentation.

---

### License

This project is licensed under the terms of the [MIT License](https://github.com/e0406370/markuapi/blob/main/LICENSE). 

This project is neither affiliated with nor endorsed by Filmarks.