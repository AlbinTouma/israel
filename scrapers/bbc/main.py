

class AljazeeraScraper():
    def __init__(self, skip_titles, driver):
        self.skip_titles = skip_titles
        self.driver  = driver

    def collect_titles(self):
        print("Collect")
        x = WebPage(website='bbc', link="https://www.bbc.com/news/topics/c2vdnvdg6xxt")
        scraper = HomePage(x, 'bbc_links')
        scraper.run()
        print("DONE")

    def full_run(self):

        file = 'bbc_data'
        js = Database.read_jsonl(filename='bbc_links')
        if self.skip_titles == "Yes":
            self.collect_titles()

        js = js[586:]

        count = 0
        for i in js:
            page = WebPage(link=i['link'])
            opts = {
                "news": News(page, file, self.driver) ,
                "news/liveblog": LiveBlog(page, file, self.driver),
                "program/newsfeed": ProgramNews(page, file, self.driver)
            }

            for key, scraper in opts.items():
                if i['media_type'] == key:
                    scraper.run()
                    count += 1
                    time.sleep(randint(1, 3))
