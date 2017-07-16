########################################################################################################################

__author__ = "Nimish"

to_be_added = ['GUI', 'Download Quality', 'Case Menu', 'Movie or episode',\
               'check availability of episode, etc.',\
               'Add appropriate error messages'\
               'OS functionalities and automation']

########################################################################################################################

from selenium import webdriver
import time
import os

# from selenium.webdriver.common.keys import Keys

def build_url(which_show, episode, quality):
    # print show_words
    show = which_show.replace(' ', '%20')
    # print show
    url = "https://kickass.cd/search.php?q=" + show.lower() + "+" + episode.lower() + '+' + quality + '/'
    # print url
    return url

def check_for_episode(url_after_search_query):
    driver = webdriver.Chrome()
    driver.get(url_after_search_query)
    source = driver.page_source
    driver.close()
    # Updated. [previously 'Nothing found!']
    if 'magnet' not in source:
        return False
    return True

def __main__():
    choice = 0
    while choice == 0:
        which_show = raw_input("Which show does the episode belong to? ")
        which_episode = raw_input("Which season and episode? (Eg. S06E10) ")
        what_quality = raw_input("Enter quality (Eg. 1080p, HDTV, DVDrip) ")
        url_after_search_query = build_url(which_show, which_episode, what_quality)
        # print url_after_search_query

        print ("Has the episode arrived yet?\n1 Yeah\n2 No, it\'ll be out very very soon\n3 Oops, let me re-enter the information")
        print ("[Note: Make sure you've entered the right keywords]")
        choice = input("Enter choice: ")
        if choice == 3:
            choice = 0
            continue

        while choice != 1 and choice != 2:
            print 'Easy there, you entered an invalid choice!'
            choice = input('Please enter a valid choice: ')

        if choice == 1:

            driver = webdriver.Chrome()
            # driver.get("https://kat.cr/usearch/?q=game+of+thrones+s06e10&from=opensearch")

            driver.get(url_after_search_query)
            # assert "Download" in driver.title

            source = driver.page_source
            if 'magnet' not in source:
                driver.close()
                print 'Oops, something was wrong with the search details you provided or maybe such a torrent does not exist yet!'
                print "We'll have to redirect you to the main menu..."
                __main__()

            here = source.find('magnet')

            download_link = ""
            if here != -1:
                temp = source[here + 19:here + 500]
                till_here = temp.find('class="icon16"')
                download_link = source[here + 19:here + till_here - 4]
                # print download_link
                os.startfile(download_link)

            driver.close()

            if 'thrones' in which_show.lower():
                print ('\nHope you GoT what you wanted ;)\n')
            else:
                print ('\nHope you got what you wanted :)\n')
            print ('\n0 to Download more\nAnything else to Exit: ')
            choice = input('Enter choice: ')

            if choice == 0:
                continue

            else:
                print '\nKay bye!'
                break

        elif choice == 2:
            print 'Please give a lower bound of the number of hours you think the episode will be out in'
            hours = input('Enter hours as a whole number: ')
            print 'Thank you! Now, keep the script running and rest will be taken care of :)'

            # Wait for that many hours
            time.sleep(3600 * hours)

            # Now, keep checking for the torrent in every fifteen minutes
            while not check_for_episode(url_after_search_query):
                time.sleep(9000)

            # If program control reaches here, that means the torrent has been found
            driver = webdriver.Chrome()
            driver.get(url_after_search_query)
            source = driver.page_source

            here = source.find('magnet')

            download_link = ""
            if here != -1:
                temp = source[here + 19:here + 500]
                till_here = temp.find('class="icon16"')
                download_link = source[here +19:here + till_here - 4]
                # print download_link
                os.startfile(download_link)
            driver.close()
            break



if __name__ == '__main__':
    __main__()