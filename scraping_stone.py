import requests
import argparse
from bs4 import BeautifulSoup

def get_url_text(url):
    '''
    Dada uma url retorna o texto do site
    
    params: url -> link do site
    
    return: retorna o texto do site
    '''
    return requests.get(url).text

def get_vagas_disponiveis(site_text, header : str, classe : str):
    '''
    Recebe o texto do site e retorna os textos dentro dos headerss e classes desejado
    
    params: site_text -> texto do site
            header:str -> header onde a classe do texto se encontra
            classe:str -> classe onde o textp se encontra
    
    return: retorna lista com items com header e classe desejado
    '''
    site_soup = BeautifulSoup(site_text, features = 'lxml')
    return site_soup.find_all(header, {'class':classe})

def get_vagas(url, header, classe, keywords_desejadas : list[str]) -> list[str]: 
    '''
    Recebe o texto do site, header, classe e keywords desejadas e retorna vagas que
    se encaixam as vagas desejadas
    
    params: site_text -> texto do site
            header:str -> header onde a classe do texto se encontra
            classe:str -> classe onde o textp se encontra
    
    return: retorna lista com items com header e classe desejado
    '''
    stone_site_text = get_url_text(url)
    header_vagas = get_vagas_disponiveis(stone_site_text, header, classe)
    vagas = [vaga.text.lower() for vaga in header_vagas]
    
    vagas_desejadas = []
    for vaga in vagas:
        for nome in keywords_desejadas:
            if nome in vaga:
                vagas_desejadas.append(vaga)
    
    return vagas_desejadas

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vagas', action = 'append', help = 'vagas desejadas')
    args = vars(parser.parse_args())
    vagas_desejadas = args['vagas'][0].split(',')

    print(get_vagas('https://jornada.stone.com.br/times/tecnologia/dados?city=', 'h2', 'text-[#45505E] font-semibold mb-4',
                            vagas_desejadas))
    
    vagas_desejadas.append('pcd')

    print(get_vagas('https://jornada.stone.com.br/times/tecnologia/vagas-pcd?city=', 'h2', 'text-[#45505E] font-semibold mb-4',
                            vagas_desejadas))