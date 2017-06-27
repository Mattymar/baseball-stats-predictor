import scrapy
from w3lib.html import remove_tags

class TeamBattingSpider(scrapy.Spider):
    name = "team_batting"

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "BOT_NAME": 'inv',
        "ROBOTSTXT_OBEY": False}

    def start_requests(self):
        start_url = 'http://www.baseball-reference.com/teams/'
        yield scrapy.Request(url=start_url, callback=self.get_teams)

    def get_teams(self, response):
        for link in response.xpath('//*[@id="div_teams_active"]//a/@href').extract():
            team = link[7:10]
            url = response.urljoin(link)
            request = scrapy.Request(url=url, callback=self.get_years)
            request.meta['team'] = team
            yield request

    def get_years(self, response):
        team = response.meta['team']
        for link in response.xpath('//*[@id="franchise_years"]//a[starts-with(text(), "20")]/@href').extract():
            year = link[11:15]
            url = response.urljoin(link)
            request = scrapy.Request(url=url, callback=self.get_batting_stats)
            request.meta['year'] = year
            request.meta['team'] = team
            yield request

    def get_batting_stats(self, response):
        team = response.meta['team']
        year = response.meta['year']
        heads = []
        players = []
        for i in response.xpath('//*[@id="team_batting"]/thead/tr'):
            head = i.xpath('.//text()').extract()
            for j in head:
                heads.append(j.strip())
        for i in response.xpath('//*[@id="team_batting"]/tbody/tr'):
            player = []
            row = map(remove_tags, i.xpath('.//*').extract())
            for j in row:
                player.append(j)
            if player[2] == player[1]:
                del player[2]
            players.append(player)
        yield {'team': team, 'year': year, 'headings': list(filter(None, heads)), 'players': players}
