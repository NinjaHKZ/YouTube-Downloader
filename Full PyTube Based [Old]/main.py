from pytube import YouTube
import sys, os


class Utils:
    def GetFlagsOption(cmd):
        _newInput = []
        _inputTuple = []

        for i in cmd:
            if len(_inputTuple) == 1 and i[0] != "-":
                if i.startswith("https://www.youtube.com/watch?"):
                    i = i.split("&")[0]
                
                _inputTuple.append(i)
                _newInput.append(tuple(_inputTuple))
                _inputTuple = []

            else:
                _inputTuple.append(i)
                        

        return _newInput

    def getInputData(FlagsInput) -> dict:
        configuration = {
            "url": None,
            "resolution": "best",
            "vFormat": "video",
            "file_path": None
        }
            
        for i in FlagsInput:
            match i[0]:
                case "-u":
                    if i[1].startswith("https://www.youtube.com/watch?"):
                        configuration["url"] = i[1]
                    else:
                        print("Url inválida")
                
                case "-r":
                    configuration["resolution"] = i[1]
                
                case "-f":
                    if i[1] in ['video', 'audio']:
                        configuration["vFormat"] = i[1]
                case "-p":
                    configuration["file_path"] = i[1]

        return configuration

    def checkUrl(url):
        try:
            return YouTube(url)

        except Exception:
            exit()

    def bestResolution(cfg, videos):
        vid = videos.streams.filter(progressive=True).get_highest_resolution()
        vid_title = vid.title
        vid_size = vid.filesize_mb
        vid_extension = vid.mime_type.split("/")[1] if vid.mime_type.split("/")[1] != "3gpp" else "mp4"
        vid_resolution = vid.resolution

        vid_name = "{}_|++|_[ {} ].{}".format(vid_title, vid_resolution, vid_extension) 

        print("\nbaixando o vídeo...\nNome: {}\nTamanho: {}\n".format(vid_title, vid_size))
     
        vid.download(output_path=cfg.get("file_path"), filename=vid_name)

    def getByResolution(cfg, videos_B):
        videos = videos_B.streams.filter(res=cfg.get("resolution"), progressive=True)
        
        if len(videos) != 0:
            vid = videos.get_highest_resolution()
            vid_title = vid.title
            vid_size = vid.filesize_mb
            vid_extension = vid.mime_type.split("/")[1] if vid.mime_type.split("/")[1] != "3gpp" else "mp4"
            vid_resolution = vid.resolution

            vid_name = "{}_|++|_[ {} ].{}".format(vid_title, vid_resolution, vid_extension) 

            print("\nbaixando o vídeo...\nNome: {}\nTamanho: {}\n".format(vid_title, vid_size))    
            
            vid.download(output_path=cfg.get("file_path"), filename=vid_name)

        else:           
            videos = videos_B.streams.filter(progressive=True).order_by("resolution")

            vid_list = {}

            for i in enumerate(videos):
                vid_list.update({i[0]: i[1]})
            
            del videos

            vid_list = vid_list[round(len(vid_list)/2)]

            vid_title = vid_list.title
            vid_size = vid_list.filesize_mb
            vid_extension = vid_list.mime_type.split("/")[1] if vid_list.mime_type.split("/")[1] != "3gpp" else "mp4"
            vid_resolution = vid_list.resolution

            vid_name = "{}_|++|_[ {} ].{}".format(vid_title, vid_resolution, vid_extension) 

            print("\nbaixando o vídeo...\nNome: {}\nTamanho: {}\n".format(vid_title, vid_size))

            vid_list.download(output_path=cfg.get('file_path'), filename=vid_name)

    def GetAudio(config, vid):
            vid = vid.streams.get_audio_only()

            vid_title = vid.title
            vid_size = vid.filesize_mb
            vid_extension = vid.mime_type.split("/")[1] if vid.mime_type.split("/")[1] != "3gpp" else "mp4"
            vid_resolution = vid.resolution

            vid_name = "{}_|++|_[ {} ].{}".format(vid_title, vid_resolution, vid_extension) 

            print("\nbaixando o vídeo...\nNome: {}\nTamanho: {}\n".format(vid_title, vid_size))

            vid.download(output_path=config.get("file_path"), filename=vid_name)
    
def Download(config: dict) -> None:
    
    vid = Utils.checkUrl(config.get('url'))

    match config.get('vFormat'):
        case "video":
            if config.get('resolution') == "best":
                Utils.bestResolution(config, vid)
            
            else:
                Utils.getByResolution(config, vid)

        case "audio":
            Utils.GetAudio(config, vid)


    print("Download finalizado.")
    sys.exit()

if __name__ == "__main__":
    try:
        print("caso esteja usando no linux, é recomendável passar os argumentos que contenha '&' em aspas(\"https://www.youtube.com/watch?v=XXXXXX&List=XXXXXXX\") ")
        cmd = sys.argv[1:]
        
        FlagsInput = Utils.GetFlagsOption(cmd)

        if len(FlagsInput[0]) == 0:
            print("python "+sys.argv[0]+" -u <URL> -r <RESOLUÇÃO> -f <VIDEO/AUDIO> -p <CAMINHO PARA SALVAR>")
            exit()

        Download(Utils.getInputData(FlagsInput))

    except KeyboardInterrupt:
        print("\ndownload cancelado.")