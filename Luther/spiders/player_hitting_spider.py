import scrapy
# from w3lib.html import remove_tags


class PlayerHittingSpider(scrapy.Spider):
    name = "player_hitting"

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "BOT_NAME": 'inv',
        "ROBOTSTXT_OBEY": False}

    base_url = 'http://www.fangraphs.com/'

    def start_requests(self):
        start_url = 'http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=8&season=2016&month=0&season1=2000&ind=0&team=0&rost=0&age=0&filter=&players=0&sort=21,d'
        yield scrapy.Request(url=start_url, callback=self.get_player_link)

    def get_player_link(self, response):
        for player in response.xpath('//tr[contains(@id, "LeaderBoard1")]//td[2]'):
            name = player.xpath('.//text()').extract()[0]
            for link in player.xpath('.//a/@href').extract():

                url = self.base_url + link
                request = scrapy.Request(url=url, callback=self.get_player_stats)
                request.meta['player'] = name
                yield request

        #follow pagination links
        next_page = response.xpath('//a[contains(@class, "rgPageNext")]/@href').extract_first()
        if next_page is not None:
            next_page = self.base_url + next_page[1:]
            print(next_page)
            yield scrapy.Request(url=next_page, callback=self.get_player_link)

    def get_player_stats(self, response):
        base_stats = []
        adv_hitting_stats = []
        bb_stats = []
        plate_disc_stats = []
        fielding_stats = []
        adv_fielding_stats = []
        scouting_stats = []
        value_stats = []
        win_prob_stats = []

        for i in response.xpath('//form[@id="form1"]/@action').extract():
            first = i.partition('playerid=')
            second = first[2].partition('&')    # get partition after player id
            player_id = second[0]   # get partition after 'playerid' and before '&'

            birthdate = (response.xpath('//strong[contains(., "Birthdate:")]//following-sibling::text()')
                         .extract()[0]
                         .strip()
                         .split()[0])

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason1_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            base_stats.append(row_stats)

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason2_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            adv_hitting_stats.append(row_stats)

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason3_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            bb_stats.append(row_stats)

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason7_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            plate_disc_stats.append(row_stats)

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason8_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            fielding_stats.append(row_stats)

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason12_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            adv_fielding_stats.append(row_stats)

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason14_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            scouting_stats.append(row_stats)

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason9_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            value_stats.append(row_stats)

        for row in response.xpath('//tr[contains(@id, "SeasonStats1_dgSeason5_")]'):
            row_stats = []
            for cell in row.xpath('.//td//text()').extract():
                row_stats.append(cell)
            win_prob_stats.append(row_stats)

        yield {'player_id': player_id,
               'name': response.meta['player'],
               'birthdate': birthdate,
               'base_stats': base_stats,
               'adv_hitting_stats': adv_hitting_stats,
               'bb_stats': bb_stats,
               'plate_disc_stats': plate_disc_stats,
               'fielding_stats': fielding_stats,
               'adv_fielding_stats': adv_fielding_stats,
               'scouting_stats': scouting_stats,
               'value_stats': value_stats,
               'win_prob_stats': win_prob_stats}
