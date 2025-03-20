from argparse import ArgumentParser
from pathlib import Path

import json

def calculate_average_chamfer(dataset_dir: Path, method, split):
    avg_d2s = 0.0
    avg_s2d = 0.0
    avg_chamfer = 0.0
    
    count = 0

    for scene in dataset_dir.iterdir():
        if not scene.is_dir():
            continue

        result_file = scene / split / "ours_30000" / method / "results.json"
        if not result_file.exists():
            print(f"Error: {result_file} not found for scene {scene}.")
            continue

        with open(result_file, "r") as f:
            result = json.load(f)
            print(f"{scene}:\t {result['overall']:0.2f}")
            avg_d2s += result["mean_d2s"]
            avg_s2d += result["mean_s2d"]
            avg_chamfer += result["overall"]
            count += 1
    
    if count == 0:
        print("No scene to evaluate")
        return

    avg_chamfer /= count
    avg_d2s /= count
    avg_s2d /= count
    print(f"Average chamfer: {avg_chamfer:0.2f}")

    chamfer_file = dataset_dir / "chamfer.json"
    if chamfer_file.exists():
        with open(chamfer_file, "r") as f:
            chamfer = json.load(f)
    else:
        chamfer = {}

    if method not in chamfer:
        chamfer[method] = {}
    if split not in chamfer[method]:
        chamfer[method][split] = {}
    chamfer[method][split]["ours_30000"] = {
        "mean_d2s": avg_d2s,
        "mean_s2d": avg_s2d,
        "overall": avg_chamfer
    }
    print(f"Writing chamfer to {chamfer_file}")
    with open(chamfer_file, "w") as f:
        json.dump(chamfer, f, indent=4)

if __name__ == "__main__":

    parser = ArgumentParser(description="Calculate average Chamfer metrics.")
    parser.add_argument("--dataset_dir", "-d", type=str, required=True, help="Path to the model parent directory")
    parser.add_argument("--method", "-m", type=str, default="tsdf", help="Method name (tsdf/fusion)")
    parser.add_argument("--split", "-s", type=str, default="test", help="Split name (train/test)")
    args = parser.parse_args()

    dataset_dir = Path(args.dataset_dir)
    if not dataset_dir.is_dir():
        print(f"Error: {dataset_dir} is not a valid directory.")
        exit(1)

    child_dirs = [child for child in dataset_dir.iterdir() if child.is_dir()]
    print(f"Number of child directories: {len(child_dirs)}")

    calculate_average_chamfer(dataset_dir, method=args.method, split=args.split)