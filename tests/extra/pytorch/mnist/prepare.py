import torch
from main import Net

model = Net().to("cpu")
state_dict = torch.load("mnist_cnn.pt")
model.load_state_dict(state_dict)

# save state dict
torch.save(model.state_dict(), "state_dict.pt")

# save entire model
torch.save(model, "entire_model.pt")

# save torch script model
model_scripted = torch.jit.script(model)
model_scripted.save("model_scripted.pt")
