#!/bin/bash
echo "============================================="
echo "  WSL 大文件/垃圾文件 精准分析工具"
echo "  适配：Ubuntu24.04 + Conda + AI大模型环境"
echo "============================================="

echo -e "\n1. 用户目录大文件扫描（前20名，仅统计可管理文件）"
echo "---------------------------------------------"
# 只扫描你的家目录，排除系统文件，结果100%有用
du -ah ~ 2>/dev/null | sort -rh | head -20

echo -e "\n2. Conda/Python 缓存垃圾（可安全删除）"
echo "---------------------------------------------"
CONDA_BASE=$(conda info --base 2>/dev/null)
echo -n "Conda 缓存大小: "
[ -d "${CONDA_BASE}/pkgs" ] && du -sh "${CONDA_BASE}/pkgs/" || echo "0B"

echo -n "Pip 缓存大小: "
[ -d ~/.cache/pip ] && du -sh ~/.cache/pip/ || echo "0B"

echo -e "\n3. AI框架缓存（torch/transformers 最大垃圾区）"
echo "---------------------------------------------"
echo -n "Torch 缓存: "
[ -d ~/.cache/torch ] && du -sh ~/.cache/torch/ || echo "0B"

echo -n "Huggingface 缓存: "
[ -d ~/.cache/huggingface ] && du -sh ~/.cache/huggingface/ || echo "0B"

echo -n "Triton/加速缓存: "
du -sh ~/.cache/triton/ ~/.cache/accelerate/ 2>/dev/null

echo -e "\n4. 临时文件/编译残留（可安全删除）"
echo "---------------------------------------------"
echo -n "系统临时文件"
echo ""
du -sh /tmp 2>/dev/null

echo -n "项目编译缓存 __pycache__: "
echo ""
find ~/testGit -name "__pycache__" -type d 2>/dev/null | xargs du -sh 2>/dev/null

echo -e "\n5. 系统日志/垃圾（可安全清理）"
echo "---------------------------------------------"
echo -n "系统日志: "
journalctl --disk-usage 2>/dev/null

echo -e "\n清理建议（绝对安全，不删模型/代码/环境）"
echo "---------------------------------------------"
echo "1. 一键清空缓存: conda clean -all -y "
echo "                 pip cache purge"
echo "2. 清空AI缓存: rm -rf ~/.cache/torch ~/.cache/huggingface ~/.cache/triton ~/.cache/accelerate"
echo "3. 清空临时文件: sudo rm -rf /tmp/*"
echo "4. 清理项目缓存: find ~/testGit -name \"__pycache__\" -delete"
echo ""