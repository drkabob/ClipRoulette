import video_code
import multiprocessing

pool = multiprocessing.Pool()
while True:
    try:
        pool.apply_async(video_code.everything())
    except Exception as e:
        print(e)
