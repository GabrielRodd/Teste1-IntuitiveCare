import scrapy
import os   
import shutil

class GovRolSpider(scrapy.Spider):
    # Identidade
    name = 'downloadbot'

    # Request
    def start_requests(self):
        urls = ['https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Response
    def parse(self, response):
        anexo_1 = response.xpath(
            "//a[@href='https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf']/@href").get()
        
        anexo_2 = response.xpath(
            "//a[@href='https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf']/@href").get()
        
        if anexo_1:
            yield scrapy.Request(url=anexo_1, callback=self.save_pdf, meta={'file_name': 'Anexo_1.pdf'})
        if anexo_2:
            yield scrapy.Request(url=anexo_2, callback=self.save_pdf, meta={'file_name': 'Anexo_2.pdf'})
        
    
    def save_pdf(self, response):
        os.makedirs('anexos', exist_ok=True)

        file_name = os.path.join('anexos', response.meta['file_name'])
        
        with open(file_name,'wb') as arquivo:
            arquivo.write(response.body)
        self.log(f"Arquivo {file_name} salvo com sucesso!")

        if len(os.listdir('anexos')) == 2:
            self.zipar()
       
    def zipar(self):
        zip_path = 'anexos_compactados.zip'
        if os.path.exists(zip_path):
            os.remove(zip_path)

        shutil.make_archive('anexos_compactados', 'zip', 'anexos')
        self.log("Arquivos compactados em anexos_compactados.zip")


