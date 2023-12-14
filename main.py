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
        
        self.media_type = arguments.mediatype
        self.path = arguments.path
        self.simultaneous_task = arguments.url_per_tasks
        self.item_get_info_queue = len(self.urls)
        self.item_queue_run = 0  

        if self.media_type == "audio":
            self.itag_identifier = {
                140: (None, "mp3")
                }

        else:
            try:
                self.resolution = [int(res.replace(',', '')) for res in arguments.resolution]
                        
                self.itag_identifier = {
                    17: (144, "mp4"),
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
            
            except ValueError:
                print('resolutions must be int.')
                exit()


        self.tasks_queue = [] 
        self.content_filtered = {}

        
    def start(self):
        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._sync_manager())
        except KeyboardInterrupt:
            print("finalizado por interrupção manual...\n")
            exit()
            
    async def _sync_manager(self):

        for url in self.urls:
            url_clean = self._url_processing(url)

            if url_clean[1] != 0:
                self.tasks_queue.append(asyncio.create_task(self._get_stream_data(url_clean[0])))
            else:
                print(url_clean[0].get('error'), url_clean[2])

        if len(self.tasks_queue) != 0:
            print(f"{self.item_get_info_queue} item for collect information...")
            await asyncio.gather(*self.tasks_queue)
            
            separate_content_filtered = list(zip_longest(*[iter(tuple(self.content_filtered.items()))]* self.simultaneous_task, fillvalue=None))
            
            self.tasks_queue.clear()
        
            for content in separate_content_filtered:
                self.tasks_queue.append(asyncio.create_task(self._start_download(content)))
            
            print('succes, starting download...', end='\n\n')            
            await asyncio.gather(*self.tasks_queue)
        
        else:
            return {"error": "All URLs passed are invalid."}, 0, self.urls

    async def _get_stream_data(self, url):
        request_results = YouTube(url)
        author = request_results.author
        title = request_results.title
        request_results = request_results.streaming_data['formats'] if self.media_type == "video" else request_results.streams.get_audio_only()

        for item_for_repalce in [(' ', '+'), ('|', ''), ('/', '')]:
            title = title.replace(item_for_repalce[0], item_for_repalce[1])

        self.content_filtered.update({title: {}})

        print(f"collected itens: {self.item_queue_run}", end='\r')

        self.item_queue_run += 1

        if self.media_type == "video":
            for data in request_results:

                self.content_filtered[title].update({data["itag"]: {}}) 

                dict_filter_type = {
                    "name": title,
                    "creator_name": author,
                    "itag": data['itag'],
                    "mimeType": data['mimeType'],
                    "media_url": data['url'],
                    "height_resolution": data['height']
                }
                await asyncio.sleep(0.015)
                self.content_filtered[title][dict_filter_type['itag']].update(dict_filter_type)       
        
        else:
            self.content_filtered[title].update({request_results.itag: {}})
            
            dict_filter_type = {
                "name": title,
                "creator_name": author,
                "itag": request_results.itag,
                "mimeType": request_results.mime_type,
                "media_url": request_results.url
            }
            await asyncio.sleep(0.015)

            self.content_filtered[title][dict_filter_type['itag']].update(dict_filter_type)        

    async def _start_download(self, content):
        content_for_downlaod = []
        
        for content_dict in content:
            if content_dict != None:
                for itags in content_dict[1].items():
                    await asyncio.sleep(0.015)

                    if itags[0] in list(self.itag_identifier.keys()):

                        if self.media_type == "video":
                            if self.itag_identifier[itags[0]][0] in self.resolution:

                                title = "{}{}+{}+{}.{}".format(self.path, itags[1]["height_resolution"], itags[1]['name'].replace("\"", ""), itags[1]['creator_name'], self.itag_identifier[itags[0]][1])
                                content_for_downlaod.append((itags[1].get('media_url'), title, self.path))
                            else:
                                continue
                        
                        else:
                            title = "{}{} {}.{}".format(self.path, itags[1]['name'], itags[1]['creator_name'], self.itag_identifier[itags[0]][1])                            
                            content_for_downlaod.append((itags[1].get('media_url'), title, self.path))

                    else:
                        pass
                       #print("processo não suportado", itags[1], itags[0])
                    
        await DownloadEngine(content_for_downlaod).start()
        


    def _url_processing(self, url):
        if url.startswith("https://") == True:
            return url.split("&")[0], 1

        elif len(url) == 11:
            return "https://www.youtube.com/watch?v="+url, 1

        else:
            return {'error': 'Use only LINK or ID from video.'}, 0, "\ninvalid Option: "+url
            


if __name__ == "__main__":
    DownloadManager().start()