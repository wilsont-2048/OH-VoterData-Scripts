import os
import sys
import cloudscraper


def get_sos_data():
    # Get current working DIR and create DATA folder to store data files.
    cwd = os.getcwd()
    os.mkdir(cwd + '/DATA')

    # Base URL to access data from OH SOS site.
    base_url = "https://www6.ohiosos.gov/ords/f?p=VOTERFTP:DOWNLOAD::FILE:NO:2:P2_PRODUCT_NUMBER:"

    # Create instance of web scrapper capable of bypassing Cloudflare anti-bot defense.
    scrapper = cloudscraper.create_scraper(delay=10, browser='chrome')

    print("Obtaining data from site...")

    # Set range to obtain individual data from 88 Ohio counties.
    for i in range(1, 89):
        url = base_url + str(i)

        data = scrapper.get(url).content

        # Write file to 'DATA' folder.
        with open(f'./DATA/data{i}.txt', 'wb') as file:
            file.write(data)

    print("Process Complete.")


def main():
    get_sos_data()

    sys.exit()


if __name__ == '__main__':
    main()
