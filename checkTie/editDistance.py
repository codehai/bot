#coding=utf-8

import numpy as np


class LevenshteinDistance:
    def leDistance(self, input_x, input_y):
        xlen = len(input_x) + 1  # 此处需要多开辟一个元素存储最后一轮的计算结果
        ylen = len(input_y) + 1

        dp = np.zeros(shape=(xlen, ylen), dtype=int)
        for i in range(0, xlen):
            dp[i][0] = i
        for j in range(0, ylen):
            dp[0][j] = j

        for i in range(1, xlen):
            for j in range(1, ylen):
                if input_x[i - 1] == input_y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[xlen - 1][ylen - 1]

def getEditDistance(strl, strr):
	ld = LevenshteinDistance()
	return ld.leDistance(strl, strr)
