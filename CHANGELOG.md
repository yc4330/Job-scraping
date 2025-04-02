# Changelog

## Ver. 2025-04-02

### Added

- **crawler.py**

  - to run crawlers for 5 platforms at once
  - and merge all new csv files

- **new_data** folder where latest scraped data automatically goes to

- **script_log\_{MMDD}.txt**: automatically record outputs and errors after running crawler.py

- **primitive deduplicate**: before writing new data, deduplicate by comparing with old data

- **target_num parameter**: added as target number of new data entries to be scraped.
  - Can be customized in main() of each crawler .py file.
    e.g. scrape_jobs_51job(2000) means we want 2000 new entries from 51 jobs.

### Changed

- rename outputs: automatically store data with "job\_{platform}\_{MMDD}.csv"

### TODO

- dianzhang cannot be scraped: job list not loaded -- see log

- CAPTCHA: still requires manual verification
