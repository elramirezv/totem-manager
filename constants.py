import wx

app = wx.App(False)
SCREEN_WIDTH, SCREEN_HEIGHT = wx.GetDisplaySize()

#SCREEN_WIDTH*=1.25
#SCREEN_HEIGHT*=1.25

row, col = (SCREEN_HEIGHT*0.1, SCREEN_WIDTH*0.1)
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = [col * x for x in range(1, 11)]
row1, row2, row3, row4, row5, row6, row7, row8, row9, row10 = [row * x for x in range(1, 11)]
