import os

scene_dir = "/home/zodnguy1/datasets/zeiss"
scenes = ["brain-transparent"]

out_dir = "output/zeiss"

for scene in scenes:
    print(f"======= Processing scene {scene} =======")
    cmd = f"python train.py -s {scene_dir}/{scene} -m {out_dir}/{scene} -r 2 --checkpoint_iterations 7000 30000  --use_decoupled_appearance --lambda_distortion 1000"
    print("[>] " + cmd)
    os.system(cmd)
    cmd = f"python render.py -m {out_dir}/{scene} -r 2 --use_decoupled_appearance"
    print("[>] " + cmd)
    os.system(cmd)
    cmd = f"python metrics.py -m {out_dir}/{scene} -r 2 --render_dir train"
    print("[>] " + cmd)
    os.system(cmd)
    print(f"======= Done with scene {scene_dir}/{scene} =======\n")
