from src.aggregate_utils import download_all_promos
from src.io_utils import save_promos

if __name__ == "__main__":
    include_dlc = True
    all_promos = download_all_promos(include_dlc=include_dlc)
    save_promos(all_promos)
