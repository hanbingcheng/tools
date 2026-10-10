import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def draw_pinyin_tianzige(filename):
    # 将 A4 纸旋转 90 度改为横向（Landscape）
    # 此时 width = 841.89, height = 595.27
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # 设置页边距（单位：磅）
    margin_left = 40
    margin_right = 40
    top_margin = 40
    bottom_margin = 40
    
    # 垂直对折线的中央空白区宽度（左右对折留白）
    center_gap = 40
    
    # 计算左半页和右半页各自可用的最大宽度
    half_page_width = (width - margin_left - margin_right - center_gap) / 2
    
    # 设定每一行包含 6 个格子（左半页 6 个，右半页 6 个，对折后刚好重合）
    cols_per_half = 6
    cell_size = half_page_width / cols_per_half  # 自动计算每个田字格的尺寸
    pinyin_height = cell_size * 0.45             # 拼音格高度约为田字格的 45%
    
    row_height = cell_size + pinyin_height
    row_gap = 12  # 每行之间的间距
    
    # 计算一页横向 A4 纸在垂直方向能容纳的行数
    usable_height = height - top_margin - bottom_margin
    num_rows = int(usable_height / (row_height + row_gap))
    
    # --- 【新增】在正中间绘制垂直折叠辅助虚线 ---
    center_x = width / 2.0
    c.setStrokeColor(colors.HexColor("#cccccc"))  # 使用更淡的灰色
    c.setLineWidth(0.6)                           # 较细的线宽
    c.setDash(4, 4)                               # 虚线样式（长4点，空4点）
    c.line(center_x, bottom_margin, center_x, height - top_margin)
    
    # 开始绘制字帖格子
    start_y = height - top_margin
    
    for r in range(num_rows):
        current_y = start_y - r * (row_height + row_gap)
        
        pinyin_top = current_y
        pinyin_bottom = pinyin_top - pinyin_height
        
        tianzige_top = pinyin_bottom
        tianzige_bottom = tianzige_top - cell_size
        
        # 针对左半页 and 右半页分别绘制这一行的格子
        for side in ['left', 'right']:
            # 计算当前半页的起始 X 坐标
            if side == 'left':
                page_start_x = margin_left
            else:
                page_start_x = margin_left + half_page_width + center_gap
                
            # 绘制当前行的具体格子
            for c_idx in range(cols_per_half):
                x_left = page_start_x + c_idx * cell_size
                x_right = x_left + cell_size
                
                # --- 1. 绘制拼音格 (带有外框以及内部两条虚线) ---
                c.setStrokeColor(colors.HexColor("#555555"))
                c.setLineWidth(0.8)
                c.setDash()  # 恢复实线
                c.rect(x_left, pinyin_bottom, cell_size, pinyin_height, fill=0, stroke=1)
                
                c.setStrokeColor(colors.HexColor("#aaaaaa"))
                c.setLineWidth(0.5)
                c.setDash(2, 2)  # 设置虚线
                pinyin_space = pinyin_height / 3.0
                c.line(x_left, pinyin_bottom + pinyin_space, x_right, pinyin_bottom + pinyin_space)
                c.line(x_left, pinyin_bottom + 2 * pinyin_space, x_right, pinyin_bottom + 2 * pinyin_space)
                
                # --- 2. 绘制田字格 ---
                c.setStrokeColor(colors.HexColor("#555555"))
                c.setLineWidth(0.8)
                c.setDash()  # 恢复实线
                c.rect(x_left, tianzige_bottom, cell_size, cell_size, fill=0, stroke=1)
                
                c.setStrokeColor(colors.HexColor("#aaaaaa"))
                c.setLineWidth(0.5)
                c.setDash(2, 2)  # 设置虚线
                # 水平中心线
                c.line(x_left, tianzige_bottom + cell_size/2.0, x_right, tianzige_bottom + cell_size/2.0)
                # 垂直中心线
                c.line(x_left + cell_size/2.0, tianzige_bottom, x_left + cell_size/2.0, tianzige_top)
                
    c.showPage()
    c.save()
    print(f"成功生成带有折叠虚线的字帖：{filename}")

if __name__ == "__main__":
    draw_pinyin_tianzige("my_blank_pinyin_tianzige.pdf")
