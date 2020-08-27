import scrapy

class CorpusExtract(scrapy.Spider):
    # deve ser o mesmo nome dado a classe
    name = 'corpusExtract'
    
    nome_da_categoria = ''
    

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
        itens = response.css('.R8zArc::text').getall()

        nomeApp =  itens[0]
        categoriaApp = ''
        for item in itens:
            if(nomeApp != item):
                categoriaApp += ' '+item
            

        informacoes = response.css('span.htlgb::text').getall()
        
        atualizada = informacoes[0]
        tamanho = informacoes[1]
        instalacoes = informacoes[2]
        versao_atual = informacoes[3]
        requer_android = informacoes[4]
        classificacao = informacoes[5]

        politica_privacidade = response.xpath('//div//a[re:test(@href,"privacy")]/@href').get()

        yield{
            'Nome': nomeApp,
            'Categoria': categoriaApp,
            'Atualizada': atualizada ,
            'Tamanho': tamanho,
            'Instalacoes': instalacoes,
            'Versao Atual': versao_atual,
            'Requer Android': requer_android,
            'Classificacao': classificacao,
            'Politica de Privacidade': politica_privacidade
        }

        
