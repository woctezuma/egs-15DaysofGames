from src.aggregate_utils import download_all_promos
from src.io_utils import save_promos

if __name__ == "__main__":
    all_promos = download_all_promos()
    save_promos(all_promos)
