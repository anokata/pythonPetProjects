from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

arguments = {"keywords":"Cat,pussy,beatch","limit":1,"print_urls":False}
paths = response.download(arguments)
print(paths) 
