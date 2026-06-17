import os
import json
import numpy as np
import cv2
import torch
import gradio as gr
from PIL import Image

EXECUTORCH_AVAILABLE = True
try:
    from executorch.runtime import Runtime
except ImportError:
    EXECUTORCH_AVAILABLE = False

with open("experiment_summary.json", "r") as f:
    SUMMARY = json.load(f)

IMG_H, IMG_W = SUMMARY["config"]["img_size"]
PALETTE = np.array(SUMMARY["class_colors"], dtype=np.uint8)
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

class ExecuTorchRunner:
    def __init__(self, pte_path="unet_camvid.pte"):
        self.active = EXECUTORCH_AVAILABLE and os.path.exists(pte_path)
        if self.active:
            self.runtime = Runtime.get()
            self.program = self.runtime.load_program(pte_path)
            self.method = self.program.load_method("forward")
        else:
            raise RuntimeError("Fatal: ExecuTorch backend missing or corrupted .pte file.")

    def run(self, input_tensor):
        return self.method.execute((input_tensor,))[0]

def preprocess_image(img_pil):
    img_resized = img_pil.convert("RGB").resize((IMG_W, IMG_H), resample=Image.Resampling.BILINEAR)
    img_np = (np.array(img_resized, dtype=np.float32) / 255.0 - MEAN) / STD
    return torch.from_numpy(img_np.transpose(2, 0, 1)).unsqueeze(0).contiguous()

def decode_segmentation(output_tensor, orig_img):
    mask_idx = torch.argmax(output_tensor[0], dim=0).numpy().astype(np.uint8)
    mask_color = PALETTE[mask_idx]
    orig_w, orig_h = orig_img.size
    mask_resized = cv2.resize(mask_color, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)
    return Image.fromarray(cv2.addWeighted(np.array(orig_img), 0.6, mask_resized, 0.4, 0))

try:
    runner = ExecuTorchRunner()
except Exception as e:
    runner = None
    print(f"Runner initialization failed: {e}")

def segment_scene(image):
    if image is None or runner is None: return image
    tensor = preprocess_image(image)
    out_tensor = runner.run(tensor)
    if isinstance(out_tensor, np.ndarray):
         out_tensor = torch.from_numpy(out_tensor)
    return decode_segmentation(out_tensor, image)

with gr.Blocks(title="Urban Scene Segmentation") as interface:
    gr.Markdown("# CamVid Urban Segmentation (U-Net FP32)")
    gr.Markdown("Interactive inference via ExecuTorch runtime.")

    with gr.Row():
        img_in = gr.Image(type="pil", label="Input Scene")
        img_out = gr.Image(type="pil", label="Predicted Segmentation")

    btn = gr.Button("Segment Scene", variant="primary")
    btn.click(segment_scene, inputs=img_in, outputs=img_out)

if __name__ == "__main__":
    interface.launch()
