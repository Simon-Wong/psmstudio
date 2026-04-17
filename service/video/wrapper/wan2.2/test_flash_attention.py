import torch
import flash_attn

# 打印成功信息
print("FlashAttention 安装成功！")
print(f"显卡: {torch.cuda.get_device_name(0)}")
print(f"CUDA版本: {torch.version.cuda}")

# 直接测试核心算子（RTX5080 Blackwell 专属优化）
q = torch.randn(2, 1024, 32, 128, dtype=torch.bfloat16, device="cuda")
k = torch.randn(2, 1024, 32, 128, dtype=torch.bfloat16, device="cuda")
v = torch.randn(2, 1024, 32, 128, dtype=torch.bfloat16, device="cuda")

out = flash_attn.flash_attn_func(q, k, v, causal=True)
print(f"测试运行成功！输出形状: {out.shape}")

# FlashAttention 安装成功！
# 显卡: NVIDIA GeForce RTX 5080
# CUDA版本: 13.0
# 测试运行成功！输出形状: torch.Size([2, 1024, 32, 128])


#虽然如此，Windows上还是没法用，因为triton看起来也是要自己编译的。
#这个Wan2.2还是要wsl或者docker来跑的。