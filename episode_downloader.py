########################################################################################################################

__author__ = "Nimish"

to_be_added = ['GUI']

########################################################################################################################

from selenium import webdriver
import time
import os
import sys

# from selenium.webdriver.common.keys import Keys

def build_url(which_show, episode, quality):
    # show_words = which_show.split()
    # show_word_count = show_words.__len__()
    # print show_words
    show = which_show.replace(' ', '%20')
    # print show
    # return "https://kat.cr/usearch/" + show.lower() + "%20" + episode.lower() + '%20' + quality + '/'
    # return "https://kickass.cd/search.php?q=" + show.lower() + "%20" + episode.lower() + '%20' + quality + '/'
    return "https://kickass.cd/search.php?q=" + show.lower() + "+" + episode.lower() + '+' + quality + '/'

def check_for_episode(url_after_search_query):
    driver = webdriver.Chrome()
    driver.get(url_after_search_query)
    source = driver.page_source
    if 'Nothing found!' in source:
        driver.close()
        return False
    return True

def open_downloaded_torrent_file(which_show, which_episode, what_quality):
    # print os.getcwd()
    path_to_file = 'C:/Users/Nimish/Downloads/'

    right_torrent_found = 0

    this_file = ''
    for files in os.walk(path_to_file):
        # print files
        for sub_files in files[2]:
            # Search for all torrent files
            if '.torrent' in sub_files:
                # Search for the torrent file associated with the script
                torrent_file_split_by_dots = sub_files[8:].split('.')
                show_split_by_spaces = which_show.lower().split()
                show_number_of_words = show_split_by_spaces.__len__()
                # print torrent_file_split_by_dots
                # print show_split_by_spaces
                # print which_episode.lower()
                # print what_quality.lower()
                if which_episode.upper() in torrent_file_split_by_dots:
                    right_torrent_found = 1
                    this_file = sub_files
                '''
                for i in range(show_number_of_words):
                     if show_split_by_spaces[i] in torrent_file_split_by_dots:
                        if which_episode.lower() in torrent_file_split_by_dots:
                            if what_quality.lower() in torrent_file_split_by_dots:
                                right_torrent_found = 1
                                this_file = sub_files
                '''
    if right_torrent_found == 1:
        os.startfile(path_to_file + this_file)

    else:
        print 'File not found!'
        __main__()

    return


def __main__():
    choice = 0
    while choice == 0:
        which_show = raw_input("Which show does the episode belong to? ")
        which_episode = raw_input("Which season and episode? (Eg. S06E10) ")
        what_quality = raw_input("Enter quality (Eg. 1080p, HDTV, DVDrip) ")
        url_after_search_query = build_url(which_show, which_episode, what_quality)
        print url_after_search_query

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
            # choice = 0
            # while choice == 0:

            driver = webdriver.Chrome()
            # driver.get("https://kat.cr/usearch/?q=game+of+thrones+s06e10&from=opensearch")

            driver.get(url_after_search_query)
            # assert "Download" in driver.title

            source = driver.page_source
            if 'Nothing found!' in source:
                driver.close()
                print 'Oops, something was wrong with the search details you provided or maybe such a torrent does not exist yet!'
                print "We'll have to redirect you to the main menu..."
                __main__()

            # here = source.find('torcache')
            here = source.find('itorrents')
            download_link = ""
            if here != -1:
                # print 'hula'
                temp = source[here - 2:here + 300]
                till_here = temp.find('class="icon16"')
                download_link = source[here - 2:here + till_here - 4]
                # print download_link
            driver.close()

            driver = webdriver.Chrome()
            driver.get('https:' + download_link)
            time.sleep(3)
            driver.close()

            open_downloaded_torrent_file(which_show, which_episode, what_quality)

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

            here = source.find('torcache')
            download_link = ""
            if here != -1:
                temp = source[here - 2:here + 300]
                till_here = temp.find('class="icon16"')
                download_link = source[here - 2:here + till_here - 4]

            driver.close()

            driver = webdriver.Chrome()
            driver.get('https:' + download_link)
            time.sleep(3)
            driver.close()

            open_downloaded_torrent_file(which_show, which_episode, what_quality)

            break



if __name__ == '__main__':
    __main__()

    # open_downloaded_torrent_file()
