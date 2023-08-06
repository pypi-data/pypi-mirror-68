import requests
import json

# the base url
url = 'https://covidtracking.com/api/v1'

# filename for output file to append to
filename = "CovidDailyUpdate.txt"  # Change to your filename


def main():
    # adding the sub urls
    JSON_state_current = requests.get(url + '/states/MS/current.json').json()
    JSON_state_info = requests.get(url + '/states/info.json').json()
    JSON_daily_info = requests.get(url + '/states/MS/daily.json').json()
    JSON_us_daily = requests.get(url + '/us/daily.json').json()

    # importing the json as a string
    state = JSON_state_info[28]["name"]
    total_cases_ms = JSON_state_current["positive"]
    deaths_ms = JSON_state_current["death"]
    dateChecked = JSON_daily_info[0]["dateChecked"]
    new_cases_ms = JSON_daily_info[0]["positiveIncrease"]
    new_deaths_ms = JSON_daily_info[0]["deathIncrease"]
    new_cases_us = JSON_us_daily[0]["positiveIncrease"]
    new_deaths_us = JSON_us_daily[0]["deathIncrease"]
    total_cases_us = JSON_us_daily[0]["positive"]
    total_deaths_us = JSON_us_daily[0]["death"]
    output_line = f"{dateChecked}: Today in {state} there are {new_cases_ms} new COVID-19 cases being reported by the MSDH and {new_deaths_ms} new deaths. This brings the total number of cases in {state} to {total_cases_ms} and {deaths_ms} deaths. \r\n Today in the US the CDC is reporting {new_cases_us} new cases and {new_deaths_us} deaths. This brings the total number of positive cases to {total_cases_us} and a total of {total_deaths_us} deaths.\r"

    # Adding functionality to append to document.
    # Open file in append & read mode ('a+').
    with open(filename, 'a+') as document:
        document.seek(0)

        # If document not empty, insert blank line for formatting / spacing.
        if len(document.read(100)) > 0:
            document.write('\n')
        document.write(output_line)


if __name__ == '__main__':
    main()
