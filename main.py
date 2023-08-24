from pytube import YouTube
import asyncio


class DownloadManager:
    def __init__(self, urls: list, resolution: tuple, format="video", path=None):
        self.urls = urls
        self.resolution = resolution
        self.format = format
        self.path = path
        self.tasks_queue = [] 
        self.content_filtered = {}

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._sync_manager())

    async def _sync_manager(self):

        for url in self.urls:
            url_clean = self._url_processing(url)

            if url_clean[1] != 0:
                self.tasks_queue.append(asyncio.create_task(self._get_stream_data(url_clean[0])))
            else:
                print(url_clean[0].get('error'), url_clean[2])

        if len(self.tasks_queue) != 0:
            await asyncio.gather(*self.tasks_queue)
        
        else:
            return {"error": "All URLs passed are invalid."}, 0, self.urls

    async def _get_stream_data(self, url):
        request_results = YouTube(url)
        self.content_filtered.update({request_results.title: {}})
        
        for data in request_results.streaming_data['formats']:
            self.content_filtered[request_results.title].update({data["itag"]: {}})
            await asyncio.sleep(0.015)
            dict_filter_type = {
                "itag": data['itag'],
                "mimeType": data['mimeType'],
                "media_url": data['url'],
                "vide_quality": data["quality"],
                "audio_quality": data['audioQuality'],
                "midia_fps": data['fps'],
                "height_resolution": data["qualityLabel"]

            }

            self.content_filtered[request_results.title][dict_filter_type['itag']].update(dict_filter_type)

            
    def _url_processing(self, url):
        if url.startswith("https://") == True:
            return url, 1

        elif len(url) == 11:
            return "https://www.youtube.com/watch?v="+url, 1

        else:
            return {'error': 'Use only LINK or ID from video.'}, 0, "\ninvalid Option: "+url

            



if __name__ == "__main__":
    url = ["A2HCiEX7hyc1", "https://www.youtube.com/watch?v=-QBuXSGQ9fM&list=RDMM&index=11&ab_channel=RodrigoZin", "https://www.youtube.com/watch?v=vjKEFyzR9EQ&ab_channel=CanaldoSchwarza"]
    resolution = "144p"
    format = "video"
    path = "baixados/"

    DownloadManager(url, resolution, format, path).start()