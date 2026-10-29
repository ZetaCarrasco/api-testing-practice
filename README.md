# API Testing Practice

![API Tests](https://github.com/ZetaCarrasco/api-testing-practice/actions/workflows/api-tests.yml/badge.svg)

A hands-on API testing project against [Restful-booker](https://restful-booker.herokuapp.com), a public practice API. I built it to practice backend testing with two tools: **pytest** (Python) and **Postman/Newman**. Both suites run automatically in **GitHub Actions**.

## What it covers

- Full CRUD flow (create, read, update, delete) with token-based authentication
- Negative cases: requests without a token, with an invalid token, with an empty body, and for a booking that does not exist
- Data-driven tests: the same test runs with several invalid booking IDs (pytest `parametrize` and a CSV file for Newman)
- pytest fixtures with setup and teardown, so each test creates and cleans up its own data
- CI pipeline: both test suites run on every push and pull request

## Project structure

```
.
├── .github/workflows/api-tests.yml   # CI: runs pytest and Newman
├── postman/
│   ├── Restful-booker.postman_collection.json
│   └── missing_ids.csv               # data for the data-driven folder
├── pytest/
│   ├── conftest.py                   # shared fixtures (base_url, token, create_booking)
│   └── test_booking_fixture.py
└── requirements.txt
```

The Postman collection has three folders: `Happy path`, `Negative cases` and `Data-driven`.

## How to run locally

**pytest** (from the project root):

```bash
pip install -r requirements.txt
pytest pytest -v
```

**Newman** (requires Node.js):

```bash
npx newman run postman/Restful-booker.postman_collection.json \
  --env-var "base_url=https://restful-booker.herokuapp.com" \
  --folder "Happy path" --folder "Negative cases"

npx newman run postman/Restful-booker.postman_collection.json \
  --env-var "base_url=https://restful-booker.herokuapp.com" \
  -d postman/missing_ids.csv --folder "Data-driven"
```

The data-driven folder is run separately because Newman repeats the selected folders once per CSV row.

## API quirks found

Some responses differ from common REST conventions. The tests assert the real behavior, and the test names document the deviation:

| Case | API returns | Standard would be |
|---|---|---|
| DELETE a booking | 201 | 200 or 204 |
| PUT or DELETE without a token | 403 | 401 |
| POST with an empty body | 500 | 400 |

## Notes

- Restful-booker is a shared public API and resets its data periodically, so each test creates its own booking instead of relying on existing data.
