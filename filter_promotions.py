from src.filter_utils import filter_promos
from src.io_utils import load_promos
from src.print_utils import print_promos

if __name__ == "__main__":
    all_promos = load_promos()
    filtered_promos = filter_promos(all_promos)
    print_promos(filtered_promos)
