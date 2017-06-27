import scrapy


# from w3lib.html import remove_tags

class PlayerHittingHeadingsSpider(scrapy.Spider):
    name = "player_hitting_headings"

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "BOT_NAME": 'inv',
        "ROBOTSTXT_OBEY": False}

    #base_url = 'http://www.fangraphs.com/'

    def start_requests(self):
        start_url = 'http://www.fangraphs.com/statss.aspx?playerid=1177&position=1B'
        yield scrapy.Request(url=start_url, callback=self.get_headings)

    def get_headings(self, response):

        base_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason1_")]/thead/tr//th//text()').extract()]

        adv_hitting_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason2_")]/thead/tr//th//text()').extract()]

        bb_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason3_")]/thead/tr//th//text()').extract()]

        plate_disc_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason7_")]/thead/tr//th//text()').extract()]

        fielding_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason8_")]/thead/tr//th//text()').extract()]

        adv_fielding_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason12_")]/thead/tr//th//text()').extract()]

        scouting_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason14_")]/thead/tr//th//text()').extract()]

        value_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason9_")]/thead/tr//th//text()').extract()]

        win_prob_stats = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason5_")]/thead/tr//th//text()').extract()]

        yield {'base_stats': base_stats,
               'adv_hitting_stats': adv_hitting_stats,
               'bb_stats': bb_stats,
               'plate_disc_stats': plate_disc_stats,
               'fielding_stats': fielding_stats,
               'adv_fielding_stats': adv_fielding_stats,
               'scouting_stats': scouting_stats,
               'value_stats': value_stats,
               'win_prob_stats': win_prob_stats}
