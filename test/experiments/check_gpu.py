import torch
if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    x = torch.ones(1, device=mps_device)
    print(x)
else:
    print("MPS device not found.")

# check best torch_device
if torch.backends.mps.is_available():
    torch_device = torch.device('mps')
elif torch.cuda.is_available():
    torch_device = 'cuda'
else:
    torch_device = 'cpu'
print(torch_device)