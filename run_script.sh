#! /bin/sh.
echo 'Running user_activity_main.py'
cd user_activity_data/ && python3 user_activity_main.py
echo 'Running scraper_main.py'
cd .. && cd github-scraper && python3 scraper_main.py
echo 'Running tests for user_activity_data'
cd .. && cd tests && python3 user_activity_main_tests.py