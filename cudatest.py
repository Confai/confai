import torch

cuda_version = torch.version.cuda
if cuda_version is not None:
    print(f"PyTorch was compiled with CUDA {cuda_version}")
else:
    print("PyTorch does not support CUDA")

print(torch.__version__)