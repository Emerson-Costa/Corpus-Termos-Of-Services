import scrapy


import scrapy

class CorpusExtract(scrapy.Spider):
    # deve ser o mesmo nome dado a classe
    name = 'termsExtract'
    
    start_urls = ['https://play.google.com/store/apps?&hl=pt_BR']

    def parse(self, response):
        links = response.css('li.KZnDLd a::attr(href)').getall()
        for link in links:
            yield scrapy.Request(
               response.urljoin(link), callback=self.appsCategoria
            )
    
    def appsCategoria(self, response):
        links = response.css('a.poRVub::attr(href)').getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link), callback=self.nomeApp_CatApp
            )     

    def nomeApp_CatApp(self, response):
        politica_privacidade = response.xpath('//div//a[re:test(@href,"privacy")]/@href').get()
        yield scrapy.Request(
                   politica_privacidade, callback=self.appsPrivacity
        )
    
    def appsPrivacity(self, response):
        # Gravar com o nome do app contido no arquivo.csv
        nome = response.css('title::text').get()
        with open(nome+'.html', 'wb') as f:
            f.write(response.body)   