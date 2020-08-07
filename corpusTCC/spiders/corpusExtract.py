import scrapy

class CorpusExtract(scrapy.Spider):
    # deve ser o mesmo nome dado a classe
    name = 'corpusExtract'

    start_urls = ['https://play.google.com/store/apps']

    def parse(self, response):
        links = response.css('li.KZnDLd a::attr(href)').getall()
        for link in links:
            yield scrapy.Request(
            # o método urljoin concatena a url extaída com a url raíz da página 
               response.urljoin(link), callback=self.parse_category
            )
    
    # métodos para as chamadas de call backs
    def parse_category(self, response):
        news = response.css('a.poRVub::attr(href)').getall()
        for new_url in news:
            
            yield scrapy.Request(
                response.urljoin(new_url), callback=self.parse_termosUsers
            )
    
    def parse_termosUsers(self, response):
        news = response.xpath('//div//a[re:test(@href,"privacy-policy")]/@href').getall()
        for new_url in news:
            
            yield scrapy.Request(
                response.urljoin(new_url), callback=self.parse_termsPage
            )
            
    # retornando um discionário com os dados das URLS
    def parse_termsPage(self, response):
        nome_da_categoria = response.css('.TwyJFf::text').get()
        nome_do_app = response.css('.AHFaub span::text').get()
        link_da_politica_de_privacidade = response.xpath('//div//a[re:test(@href,"privacy-policy")]/@href').get()
        yield{
            'nomeCategoryApp': nome_da_categoria,
            'nomeApp': nome_do_app,
            'PoliticaPrivacy': link_da_politica_de_privacidade
        }

    '''
        Atributos:

            - nome da categoria = response.css('.TwyJFf::text').get()
            - nome do app = response.css('.AHFaub span::text').get()
            - link da politica de privacidade = response.xpath('//div//a[re:test(@href,"privacy-policy")]/@href').get()

    '''
    