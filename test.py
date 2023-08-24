import requests, time, os




class DownloadEngine:
    def __init__(self, url):
        os.remove("video.mp4")
        self.url = url
        self.last_run = False
                
        
       


    def start(self):
        video_size = int(requests.post(self.url, headers=self._compile_header(0, 0)).headers["Content-Range"].split('/')[1])
        byte_init = 0
        byte_final = 29999999
        last_run = False

        while True:
            data = requests.post(self.url, headers=self._compile_header(byte_init, byte_final))
 
            if byte_final > video_size:
                    if last_run == False:
                        byte_init += 3000000
                        byte_final = byte_final - video_size
                        last_run = True
                        
                    else:
                         break
           
            else:

                byte_init += 3000000
                byte_final += 3000000

           
            self._compile_header(byte_init, byte_final)        

            with open("video.mp4", 'ab') as r:
                r.write(data.content)
    
    def _compile_header(self, init_range, final_range):
        return  {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Range": f"bytes={init_range}-{final_range}"}
    
DownloadEngine('https://rr1---sn-qc0b-jfcs.googlevideo.com/videoplayback?expire=1692938002&ei=strnZNKgMYbzwAT17qfYDw&ip=201.130.84.253&id=o-AGIMZzgzDeyR91bNkqZuNlMSufD-5fVEzGe35dKcCnqq&itag=18&source=youtube&requiressl=yes&mh=ul&mm=31%2C29&mn=sn-qc0b-jfcs%2Csn-bg07dn6r&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=24&initcwndbps=615000&vprv=1&mime=video%2Fmp4&gir=yes&clen=29112407&ratebypass=yes&dur=436.395&lmt=1669660609570250&mt=1692916141&fvip=2&fexp=24007246%2C51000023&c=ANDROID_MUSIC&txp=5538434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRAIgSbYOjICsVFX6ukJMRWA_IElanmZ7EfcpWfdWhmTeHksCIBN3NRFeybtUWpV7E6QdwSfp-omPVMOjiBDMW9ETRFdE&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhANz_LHGihWqqdB2V6pbxZAvBiCSSm3MXJIApkuJQWTeiAiAPBd2mFFpp-lKqVO4OPD1VfdNDgQjaN6jNpt-wy9XIbA%3D%3D').start()