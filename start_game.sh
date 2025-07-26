#!/bin/bash

# 坦克大战游戏启动脚本

echo "正在启动坦克大战游戏..."
echo "=========================================="
echo "游戏控制说明:"
echo "玩家1（蓝色坦克）:"
echo "  W - 前进"
echo "  S - 后退"
echo "  A - 左转"
echo "  D - 右转"
echo "  空格键 - 射击"
echo ""
echo "玩家2（红色坦克）:"
echo "  ↑ - 前进"
echo "  ↓ - 后退"
echo "  ← - 左转"
echo "  → - 右转"
echo "  回车键 - 射击"
echo ""
echo "其他控制:"
echo "  ESC - 退出游戏"
echo "  R - 游戏结束后重新开始"
echo "=========================================="
echo ""

# 运行游戏
python3 tank_game.py