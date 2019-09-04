#!/usr/bin/python
# -*- coding: utf-8 -*

from bs4 import BeautifulSoup
from selenium import webdriver
import re, sys, argparse

class colors:
    # Colors
    BOLD = '\033[1m'
    FAIL = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def printMsg(msg, outcome="ok"):
    # Print based on outcome
    if outcome == "ok":
        print colors.BOLD + colors.GREEN + "[+]" + colors.END + " " + msg
    elif outcome == "neut":
        print colors.BOLD + colors.YELLOW + "[!]" + colors.END + " " + msg
    elif outcome == "fail":
        print colors.BOLD + colors.FAIL + "[!]" + colors.END + " " + msg
    elif outcome == "info":
        print colors.BOLD + colors.BLUE + "[!]" + colors.END + " " + msg
    else:
        print colors.BOLD + colors.FAIL + "[+]" + colors.END + " No color selected for printMsg"


def find_list_resources (tag, attribute,soup):
   list = []
   for x in soup.findAll(tag):
       try:
           list.append(x[attribute])
       except KeyError:
           pass
   return(list)

def unique_values(list):

    unique_list = []

    for x in list:
        if x not in unique_list:
            unique_list.append(x)
        else:
            pass
    return unique_list


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="File with URLs, one per line.", type=str)
parser.add_argument('-u', '--url', help="Single URL to check", type=str)

args = parser.parse_args()

if args.file != None and args.url == None:
    targets = args.file
    printMsg("Processing file... %s" % targets, "info")

    file = open(targets, 'r')
    for url in file:
        #Regex to catch domain
        pattern = r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[.][a-z0-9]{2,3}'

        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True    

        driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)

        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

            image_scr = find_list_resources('img',"src",soup)
            script_src = find_list_resources('script',"src",soup)
            css_link = find_list_resources("link","href",soup)
            video_src = find_list_resources("video","src",soup)
            audio_src = find_list_resources("audio","src",soup)
            iframe_src = find_list_resources("iframe","src",soup)
            embed_src = find_list_resources("embed","src",soup)
            object_data = find_list_resources("object","data",soup)
            source_src = find_list_resources("source","src",soup)

            resources = [ image_scr, script_src, css_link, video_src, audio_src, iframe_src, embed_src, object_data, source_src ]

            for res in resources:
                #printMsg("Processing %s" % repr(res), "neut") 
                for r in res:
                    domains = re.findall(pattern, r)
                    uniq_domains = unique_values(domains)
                    for d in domains:
                         print "[Resource] ", d, "| [URI] ", r

        except:
            pass

elif args.file != None and args.url != None:
    print "-f/--file and -u/--url cannot be used together"
elif args.url != None and args.file == None:
    url = args.url
    printMsg("Fetching domains from %s" % url, "info") 
    #Regex to catch domain
    pattern = r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[.][a-z0-9]{2,3}'

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True    

    driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)

    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        image_scr = find_list_resources('img',"src",soup)
        script_src = find_list_resources('script',"src",soup)
        css_link = find_list_resources("link","href",soup)
        video_src = find_list_resources("video","src",soup)
        audio_src = find_list_resources("audio","src",soup)
        iframe_src = find_list_resources("iframe","src",soup)
        embed_src = find_list_resources("embed","src",soup)
        object_data = find_list_resources("object","data",soup)
        source_src = find_list_resources("source","src",soup)

        resources = [ image_scr, script_src, css_link, video_src, audio_src, iframe_src, embed_src, object_data, source_src ]
        
        for res in resources:
            #printMsg("Processing %s" % repr(res), "neut") 
            for r in res:
                domains = re.findall(pattern, r)
                uniq_domains = unique_values(domains)
                for d in domains:
                     print "[Resource] ", d, "| [URI] ", r

    except:
        pass


