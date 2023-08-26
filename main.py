from pytube import YouTube
import asyncio, json
from itertools import zip_longest
from DownloadCore import DownloadEngine
from ArgsCore import ArgEngine
# sync youtube account to get playlists from channel 

class DownloadManager:
    def __init__(self):
            
        arguments = ArgEngine.Start()
        arguments.url = set(arguments.url)
        
        self.urls = [res.replace(',', '') for res in arguments.url]
        try:
            self.resolution = [int(res.replace(',', '')) for res in arguments.resolution]
        except ValueError:
            print('resolutions must be int.')
            exit()

        self.format = arguments.mediatype
        self.path = arguments.path
        self.simultaneous_task = arguments.url_per_tasks

        self.tasks_queue = [] 
        self.content_filtered = {}

        self.itag_identifier = {
            18: (360, "mp4"),
            22: (720, "mp4"),
            37: (1080, "mp4"),
            38: (3072, "mp4"),
            160: (144, "mp4")
            }

        sup_resolutions = [res[0] for res in list(self.itag_identifier.values())]
        remove_resolutions = []
        
        for res in enumerate(self.resolution):
            if res[1] not in sup_resolutions:
                remove_resolutions.append(res[1])
                
        
        if len(self.resolution) == len(remove_resolutions):
            self.resolution = [360]

        elif len(remove_resolutions) != 0:
            for index in remove_resolutions:
                self.resolution.remove(index)
        
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
            
            separate_content_filtered = list(zip_longest(*[iter(tuple(self.content_filtered.items()))]* self.simultaneous_task, fillvalue=None))
            
            self.tasks_queue.clear()
            
            for content in separate_content_filtered:
                self.tasks_queue.append(asyncio.create_task(self._start_download(content)))
            
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
                "name": request_results.title,
                "creator_name": request_results.author,
                "itag": data['itag'],
                "mimeType": data['mimeType'],
                "media_url": data['url'],
                "vide_quality": data["quality"],
                "audio_quality": data['audioQuality'],
                "midia_fps": data['fps'],
                "height_resolution": data["qualityLabel"]

            }
            await asyncio.sleep(0.015)

            self.content_filtered[request_results.title][dict_filter_type['itag']].update(dict_filter_type)

    async def _start_download(self, content):
        content_for_downlaod = []
        
        for content_dict in content:
            if content_dict != None:
                for itags in content_dict[1].items():
                    await asyncio.sleep(0.015)
                    
                    if itags[0] in list(self.itag_identifier.keys()):
                            if self.itag_identifier[itags[0]][0] in self.resolution:
                                title = "{}{} {} {}.{}".format(self.path, itags[1]["height_resolution"], itags[1]['name'], itags[1]['creator_name'], self.itag_identifier[itags[0]][1])
                                content_for_downlaod.append((itags[1].get('media_url'), title.replace(' ', '+'), self.path))

                    else:
                        pass
                       # print("processo não suportado", itags[1], itags[0])
            else:
                pass
        await DownloadEngine(content_for_downlaod).start()
        


    def _url_processing(self, url):
        if url.startswith("https://") == True:
            return url, 1

        elif len(url) == 11:
            return "https://www.youtube.com/watch?v="+url, 1

        else:
            return {'error': 'Use only LINK or ID from video.'}, 0, "\ninvalid Option: "+url
            



if __name__ == "__main__":
    DownloadManager().start()