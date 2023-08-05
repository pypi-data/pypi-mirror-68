import random
from colorama import Fore
from pyprobar.styleString import setRGB, rgb_str

class A:
    @staticmethod
    def get_color(N_color, update=True, COLOR=[0]):
        """Choice random n colors"""
        if update == True or COLOR[0] == 0:
            rgb_dict = {"浅绿":(66, 227, 35), "深绿":(28, 97, 15), "紫色":(146, 52, 247)}
            rgb_list = [setRGB(rgb_dict["浅绿"])]

            for i in range(N_color - 2):
                rgb = rgb_dict[(random.choice(list(rgb_dict)))]
                rgb_list.append(setRGB(rgb))

            rgb_list.append(setRGB(rgb_dict["紫色"]))
            COLOR[0] = rgb_list
            return COLOR[0]
        else:
            return COLOR[0]

    def test(self):
        return self.get_color(4)

a = A()
print(a.test())
rgb_dict = {"浅绿":(66, 227, 35), "深绿":(28, 97, 15), "紫色":(146, 52, 247)}
# print(get_color(4)[2], "lalalksjdflaksjdf;kj")
