import aiohttp, asyncio

class DownloadEngine:
    def __init__(self, url: list):
        self.url = url
        self.last_run = False

      

    async def start(self):
        for url_tuples in self.url:
            print(url_tuples)
            url = url_tuples[0]
            name = url_tuples[1]
            extension = url_tuples[2]

            async with aiohttp.ClientSession() as requests:
                video_size = await requests.post(url, headers=self._compile_header(0, 0))
                video_size = int(video_size.headers["Content-Range"].split('/')[1])
                byte_init = 0
                byte_final = 299999
                last_run = False


                while True:
                    data = await requests.post(url, headers=self._compile_header(byte_init, byte_final))
                    await asyncio.sleep(0.015)

                    if byte_final > video_size:
                            if last_run == False:
                                byte_init += 300000
                                byte_final = byte_final - video_size
                                last_run = True
                            
                            else:
                                break
                
                    else:

                        byte_init += 300000
                        byte_final += 300000
                        
                    with open(f"{name}.{extension}", 'ab') as r:
                        r.write(await data.content.read())

        return {"succes": "finish process"}, 1            
    
    def _compile_header(self, init_range, final_range):
        return  {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Range": f"bytes={init_range}-{final_range}"}
    


asyncio.run(DownloadEngine(
    [('https://rr1---sn-qc0b-jfcs.googlevideo.com/videoplayback?expire=1692938002&ei=strnZNKgMYbzwAT17qfYDw&ip=201.130.84.253&id=o-AGIMZzgzDeyR91bNkqZuNlMSufD-5fVEzGe35dKcCnqq&itag=18&source=youtube&requiressl=yes&mh=ul&mm=31%2C29&mn=sn-qc0b-jfcs%2Csn-bg07dn6r&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=24&initcwndbps=615000&vprv=1&mime=video%2Fmp4&gir=yes&clen=29112407&ratebypass=yes&dur=436.395&lmt=1669660609570250&mt=1692916141&fvip=2&fexp=24007246%2C51000023&c=ANDROID_MUSIC&txp=5538434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRAIgSbYOjICsVFX6ukJMRWA_IElanmZ7EfcpWfdWhmTeHksCIBN3NRFeybtUWpV7E6QdwSfp-omPVMOjiBDMW9ETRFdE&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhANz_LHGihWqqdB2V6pbxZAvBiCSSm3MXJIApkuJQWTeiAiAPBd2mFFpp-lKqVO4OPD1VfdNDgQjaN6jNpt-wy9XIbA%3D%3D', 'zin', 'mp4'),
      ('https://rr3---sn-qc0b-jfcz.googlevideo.com/videoplayback?expire=1692950618&ei=-gvoZL2FJMWbobIPl5mVoAs&ip=201.130.84.253&id=o-ABKhLYTngzGTbBO0riVkdg7RzFMhFVbe2R7RjM2x2JLN&itag=22&source=youtube&requiressl=yes&mh=TD&mm=31%2C29&mn=sn-qc0b-jfcz%2Csn-bg07dn6d&ms=au%2Crdu&mv=m&mvi=3&pl=24&initcwndbps=1346250&vprv=1&mime=video%2Fmp4&cnr=14&ratebypass=yes&dur=202.431&lmt=1656127564579613&mt=1692928619&fvip=1&fexp=24007246%2C24363393&beids=24350018&c=ANDROID_MUSIC&txp=5432434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRAIgaSaNxG_aZiIJ4OFUk0tPJ6eQU44kHZJrnD6XrPTriKMCIF5ixOWs7MUJwpcN7D9xvc7KD0GrYexh4cVs49XWOsEQ&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRAIgZnOY2FFMIstFZv1MPSRoZOhEsmWJY4v6cUhQp5AXNXQCICsmCAX4fNh9yruokintKjduOdKO0j8T7INifXiR37OC', "ayakashi", 'mp4')]).start())