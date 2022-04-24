import pathlib
import sys

import torch

work_dir = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, work_dir)

from main import Net  # noqa

model = Net().to("cpu")
state_dict = torch.load(f"{work_dir}/mnist_cnn.pt")
model.load_state_dict(state_dict)

# save state dict
torch.save(model.state_dict(), f"{work_dir}/state_dict.pt")

# save entire model
torch.save(model, f"{work_dir}/entire_model.pt")

# save torch script model
model_scripted = torch.jit.script(model)
model_scripted.save("model_scripted.pt")
