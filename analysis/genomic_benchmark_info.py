import argparse
from genomic_benchmarks.data_check import list_datasets
from genomic_benchmarks.data_check import info

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        default="human_enhancers_cohn"
    )
    args = parser.parse_args()

    dataset_info = info(args.dataset, version=0)
    print(dataset_info)