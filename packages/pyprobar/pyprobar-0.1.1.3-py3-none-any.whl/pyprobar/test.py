from progressbar import bar, probar
import time


def test_bar():
	N = 20
	sj = "la" * 20
	for i in range(N):
		time.sleep(0.5)
		bar(i, N, "update_random", symbol_2="o")
		print(sj, end='', flush=True)
		sj =sj[:-1]


def test_probar():
	for idx, i in probar(range(1234), symbol_2="o"):
		time.sleep(0.01)


# from colorama import Fore
# test_bar()
# test_probar()
from pyprobar.styleString import rgb_str, setRGB, rgb_dict
s2 = rgb_str("I'm green", [0, 255, 0])
# print(s1, s2)
blue1 = [115, 182, 225]
blue2 = [117, 181, 244]
green1 = [66,227,35]
color =[[204,204,204],[190, 237, 199],[140, 199, 181],[190, 231, 233]]
print(color)
for idx, i in enumerate(range(1234)):
	bar(idx, 1234, text=s2, color=color)
	time.sleep(0.005)
# from tqdm import tqdm
# for i in tqdm(range(1234)):
# 	time.sleep(0.005)