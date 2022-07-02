
from bs4 import BeautifulSoup
from selenium import webdriver
import discord


driver = webdriver.Firefox()


def get_url(search_term):
    """Generates a url from search term"""
    template = 'https://myanimelist.net/search/all?q={}&cat=all'
    search_term = search_term.replace(' ',"+")
    return template.format(search_term)


async def get_results(searchTerm):

    url = get_url(searchTerm)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Stores the results for the anime search
    results = soup.find_all('div', {'class', 'information di-tc va-t pt4 pl8'})
    theResults = []

    # Gathers info for each anime
    for item in results:
        myAni = item.find_all('div')
        aniName = myAni[0].a
        aniName = aniName.text.strip()
        aniUrl = myAni[0].a.get('href')
        toSend = ''
        aniInfo = myAni[-1].text.strip().split("\n")
        for i in aniInfo:
            toSend += i.lstrip() + '\n'
        embed = discord.Embed(title=aniName,url=aniUrl,description=toSend)
        theResults.append(embed)
    return theResults


async def get_embed(myEmbed,message):

    # Creates the Embedded message with picture and watch links 
    driver.get(myEmbed.url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    locations = soup.find_all('div', {'class', 'broadcast'})
    imgUrl = ((soup.find('div', {'class', 'leftside'})).div.a.img).get('data-src')
    myEmbed.set_thumbnail(url=imgUrl)
    for location in locations:
        myEmbed.add_field(name=location.a.get('title'), value=location.a.get('href'))
    await message.channel.send(embed=myEmbed)



    