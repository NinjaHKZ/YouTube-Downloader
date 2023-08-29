import aiohttp, asyncio, os

class DownloadEngine:
    def __init__(self, url: list):
        self.url = url
        self.last_run = False
    

    async def start(self):
        for url_tuples in self.url:
            url = url_tuples[0]
            name = url_tuples[1]         
            path = url_tuples[2]
            
            self._file_exists(url, name, path)         
            
            async with aiohttp.ClientSession() as requests:
                video_size = await requests.post(url, headers=self._compile_header(0, 0))
                video_size = int(video_size.headers["Content-Range"].split('/')[1])
                byte_init = 0
                byte_final = 699999
                last_run = False


                while True:
                    data = await requests.post(url, headers=self._compile_header(byte_init, byte_final))
                    await asyncio.sleep(0.015)

                    if byte_final > video_size:
                            if last_run == False:
                                byte_init += 700000
                                byte_final = byte_final - video_size
                                last_run = True
                            
                            else:
                                break
                
                    else:

                        byte_init += 700000
                        byte_final += 700000
                    
                
                    with open(name, 'ab') as r:
                        r.write(await data.content.read())
                    
        
                print("finish process on \"%s\" file"%(name))
        return {"succes": "finish process"}, 1            
    
    def _compile_header(self, init_range, final_range):
        return  {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Range": f"bytes={init_range}-{final_range}"}
    
    def _file_exists(self, url, name, path):
        if os.path.exists(path) == False:
            os.mkdir(path)

        if os.path.exists(name) == True:
            os.remove(name)



