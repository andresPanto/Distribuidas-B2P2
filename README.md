# Distribuidas-B2P2
Segundo proyecto del segundo bimestre


python3 gather_examples.py --input videos/fake.mp4 --output dataset/fake --detector face_detector --skip 1
python3 gather_examples.py --input videos/real.mov --output dataset/real --detector face_detector --skip 4
python3 train.py --dataset dataset --model liveness.model --le le.pickle
python3 liveness_demo.py --model liveness.model --le le.pickle --detector face_detector