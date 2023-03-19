import cv2
import os
import glob

from pytube import YouTube

class MakeImagesFromVideos():

    def __init__(self, root_dir_vids, root_dir_imgs):
        self.root_dir_vids = root_dir_vids
        self.root_dir_imgs = root_dir_imgs

        self.mp4_files = glob.glob(os.path.join(root_dir_vids, '*.mp4'))

    def download_video(self, url, max_duration=10):
        try:
            yt = YouTube(url)
            duration = int(yt.player_config_args['player_response']['streamingData']['formats'][0]['approxDurationMs'])

            if duration < max_duration * 60:
                yt = yt.streams.filter(file_extension='mp4', res='2160p60').first()
                out_file = yt.download(self.root_dir_vids)

                file_name = out_file.split("\\")[-1]

                print(f"Downloaded {file_name} correctly!")
            else:
                print(f"Video {url} too long")
        
        except Exception as exc:
            print(f"Download of {url} did not work because of {exc}...")

    def max_label(self, name, folder):
        for fl in os.listdir(folder):
            if name in fl:
                label = int(fl.split("_")[-1].split(".")[0])
                
                return label
        
        return 0

    def extract_images_from_video(self, video, folder=None, delay=30, name="file", max_images=20, silent=False):    
        vidcap = cv2.VideoCapture(video)
        count = 0
        num_images = 0
        if not folder:
            folder = os.getcwd()
        
        label = self.max_label(name, folder)
        success = True
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        
        while success and num_images < max_images:
            success, image = vidcap.read()
            num_images += 1
            label += 1

            file_name = name + "_" + str(label) + ".png"
            path = os.path.join(folder, file_name)
            cv2.imwrite(path, image)

            if cv2.imread(path) is None:
                os.remove(path)
            else:
                if not silent:
                    print(f'Image successfully written at {path}')

            count += delay * fps
            vidcap.set(1, count)

    def extract_images(self, url, delete_video=False, image_delay=30, max_images=20, name="file", max_duration=15, \
                       silent=False):
        self.download_video(url, max_duration=max_duration)

        for _, video in enumerate(self.mp4_files):
            self.extract_images_from_video(video, folder=self.root_dir_imgs, delay=image_delay, name=name, \
                                            max_images=max_images, silent=silent)
            if delete_video:
                os.remove(video)


if __name__ == "__main__":
    urls = ["https://youtu.be/kHPDPl3A_wM"]

    root_dir_vids = "datasets/botw_4k_60fps_vids"
    root_dir_imgs = "datasets/botw_4k_60fps_imgs"

    if not os.path.exists(root_dir_vids):
        os.mkdir(root_dir_vids)
    if not os.path.exists(root_dir_imgs):
        os.mkdir(root_dir_imgs)

    make_images = MakeImagesFromVideos(root_dir_vids, root_dir_imgs)

    for url in urls:
        make_images.extract_images(url, delete_video=True, image_delay=30, max_images=60, name="file", \
                                   max_duration=15, silent=False)