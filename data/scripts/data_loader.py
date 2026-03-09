import kagglehub
# This downloads the 6GB to a cache folder on your Mac automatically
path = kagglehub.dataset_download("frankcaoyun/stocktwits-2020-2022-raw")
print(f"Dataset downloaded to: {path}")
