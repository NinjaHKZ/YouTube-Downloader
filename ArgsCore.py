import argparse


class ArgEngine:
    def Start():
        args = argparse.ArgumentParser(
            prog="YoutubeDownloader - Baixador e conversor de vídeos".title(),
            description="Um baixador de vídeos, músicas e tudo mais!\n\
            Possuí um poderoso sistema de download múltiplos e uma ferramente de conversão inbutido(em desenvolvimento) para facilitar a vida do usuário!\n",
            usage="python main.py -u URL/ID -m VIDEO/AUDIO -r [RESOLUTIONS]\t--help to see all commands",
            epilog="Powered With Python Power - NinjaHKZ [Devloped By Dev.Marcos H. Albach]"
        )


        args.add_argument('-u', '--url', required=True, nargs="+", type=str,
                        help='Define a url, pode ser separada por vírgulas para multiplos downloads, deve ser link ou id.')
        args.add_argument('-r', '--resolution', default="144", nargs="+", type=str,
                        help='define a qualidade(deve ser inteiro: 144 e não 144p), separar por vírgula para multiplas resoluções.')
        args.add_argument('-m', '--mediatype', choices=['video', 'audio'], default='video', type=str,
                        help='define um tipo de mídia desejada, sendo vídeo ou áudio.')
        args.add_argument('-p', '--path', type=str, default='download/',
                        help='Define o caminho onde deseja salvar os items.')
        args.add_argument('-utasks', '--url_per_tasks', type=int, default=2,
                        help='Define a queue de download ao mesmo tempo(1 para 1 url por task, 2 para 2 para cada tasks e etc...).')

        

        args = args.parse_args()

        for url in args.url:
            if url.endswith('.txt') == True:
                args.url.remove(url)

                with open(url, 'r') as r:
                    for lines in r.readlines():
                        args.url.append(lines)
        
        return args

