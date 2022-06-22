# Scraping IPCA time series

Basically the project consists of 5 stages

The main function will loop with 10 attempts being started through a cron.

1. Get the date of the last update from the local file
2. Get the date of the last update available on the site
3. Compares if the dates are different and if so, get the new value on the site.
4. If not, a time counter set to 30 minutes starts
5. Finally the local file is updated with new data.