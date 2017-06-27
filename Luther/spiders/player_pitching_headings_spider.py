import scrapy
#from w3lib.html import remove_tags

class PlayerPitchingHeadingsSpider(scrapy.Spider):
    name = "player_pitching_headings"

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "BOT_NAME": 'inv',
        "ROBOTSTXT_OBEY": False}

    #base_url = 'http://www.fangraphs.com/'

    def start_requests(self):
        start_url = 'http://www.fangraphs.com/statss.aspx?playerid=1303&position=P'
        yield scrapy.Request(url=start_url, callback=self.get_player_headings)

    def get_player_headings(self, response):

        standard = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason1_")]/thead/tr//th//text()').extract()]

        advanced = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason2_")]/thead/tr//th//text()').extract()]

        batted_ball = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason3_")]/thead/tr//th//text()').extract()]

        more_batted_ball = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason4_")]/thead/tr//th//text()').extract()]

        win_probability = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason5_")]/thead/tr//th//text()').extract()]

        pitch_values_per_100 = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason20_")]/thead/tr//th//text()').extract()]

        value = [row for row in response.xpath('//table[contains(@id, "SeasonStats1_dgSeason9_")]/thead/tr//th//text()').extract()]

        yield {'standard': standard,
               'advanced': advanced,
               'batted_ball': batted_ball,
               'more_batted_ball': more_batted_ball,
               'win_probability': win_probability,
               'pitch_values_per_100': pitch_values_per_100,
               'value': value}
