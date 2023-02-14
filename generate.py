'''
Script which generate iceberg with given jpg and xlsx files

Labels
1,2,3,4,5,6,7,8

Parameters
--------------------------------------
x1,x2,y1,y2: int
    Coordinates of box where,
    x - width
    y - height
    x1, y1 - upper left corner
    x2, y2 - bottom right corner
'''

import pandas as pd
import cv2 as cv
import numpy as np

def test(text, font_scale=1., color=(255, 255, 255), thickness=1, font_face=cv.FONT_HERSHEY_DUPLEX):
    '''
    Attributes
    ------------------------------
    text_size: list
        (text_width, text_height)
        Because We want to have save space we add 4 pixels to text_height
    '''
    
    black_img = np.ones(shape=(256,256)) # HxWxC
    
    text_size, baseline = cv.getTextSize(text, font_face, font_scale, thickness)
    text_size = list(text_size)
    text_size[1] += 4
    cv.putText(black_img, text, (128,128), font_face, font_scale, color, thickness)
    
    cv.imwrite('black_test.jpg', black_img)
    
    
    return text_size

#text_size = test("asda")
#print(text_size)



def read_data(filepath='DANE_DO_GENERATORA.xlsx'):
    df = pd.read_excel(filepath)
    return df

df = read_data()
print(df)

def get_level_dict():
    '''
    Read jpg file and gives you coordinates of each level
    
    TRZEBA RECZNIE LEVEL HEIGHT DODAC BO JEST NIEROWNE DLA KAZDEGO XD
    
    Parameters
    ----------------------------
    
    Atributes
    ----------------------------
    
    Returns
    ----------------------------
    level_spaces: dict
        dictionary where labels are keys and heights are values
        {1: [0, 264], 2: [274, 534], 3: [544, 852], 4: [862, 1136],
        5: [1146, 1426], 6: [1436, 1684], 7: [1694, 1960], 8: [1970, 2238], "width":}
    '''
    border_height = 10
    level_height_1 = 264
    level_height_2 = 260
    level_height_3 = 308
    level_height_4 = 274
    level_height_5 = 280
    level_height_6 = 248
    level_height_7 = 266
    level_height_8 = 268
    level_tab = [level_height_1,level_height_2,level_height_3,level_height_4,level_height_5,level_height_6,level_height_7,level_height_8]
    level_spaces = {}
    
    for idx, level in enumerate(level_tab):
        if idx==0:
            level_spaces[idx+1] = [0,level]
        else:
            #num_of_borders = idx
            #previous_levels
            previous_levels = 0
            for i in range(idx):
                previous_levels += level_tab[i]
            previous_upper = 0
            for j in range(idx-1):
                previous_upper  += level_tab[j]
            level_spaces[idx+1] = [previous_upper+(level_tab[idx-1]+border_height*idx),previous_levels+level+border_height*idx]
    level_spaces["width"] = 1580
    return level_spaces
    
level_spaces = get_level_dict()
print(level_spaces)


class GenerateTextboxes:
    def __init__(self, column_name):
        '''
        column_name: str
            W tym przypadku Case kolumna ktorej bede uzywal jako dane wejsciowe
        '''
        self.column_name = column_name
        self.thickness = 1
        self.font_scale = 1.
        self.font_face = cv.FONT_HERSHEY_DUPLEX
        
    def __call__(self, row):
        '''
        Function whichc generate textboxes coordinates
        (x1,y1,x2,y2) for given string
        
        Attributes
        ------------------------------
        text_size: list
            (text_width, text_height)
            Because We want to have save space we add 4 pixels to text_height
        
        Returns
        ----------------------------
        textbox_coordinates: tuple
            (x1,y1,x2,y2)
        
        '''
        preprocessed_text = self.remove_polish_chars(row[self.column_name])
        text_size, baseline = cv.getTextSize(preprocessed_text, self.font_face, self.font_scale, self.thickness)
        text_size = list(text_size)
        text_size[1] += 4
        return (0,0, text_size[0], text_size[1])
        
    def remove_polish_chars(self, text):
        polish_to_english_map = {
        'ż': 'z', 'ź': 'z', 'ć': 'c', 'ą': 'a', 'ę': 'e',
        'ł': 'l', 'ó': 'o', 'ś': 's', 'ń': 'n',
        'Ż': 'Z', 'Ź': 'Z', 'Ć': 'C', 'Ą': 'A', 'Ę': 'E',
        'Ł': 'L', 'Ó': 'O', 'Ś': 'S', 'Ń': 'N'
        }
        for char, replacement in polish_to_english_map.items():
            text = text.replace(char, replacement)
        return text

gen = GenerateTextboxes("Case")
result = df.apply(gen, axis=1)
df["x1"], df["y1"], df["x2"], df["y2"] = zip(*result)
print(df)

def add_random_positions(df, width=1250, height_0=274, height_1=534):
    # Obliczenie szerokości i wysokości każdego prostokąta
    df['w'] = df['x2'] - df['x1']
    df['h'] = df['y2'] - df['y1']
    
    # Generowanie losowych pozycji punktów dla każdego prostokąta
    df['XL'] = np.random.randint(0, width - df['w'])
    df['YL'] = np.random.randint(height_0, height_1 - df['h'])
    
    # Uwzględnienie pozycji punktów wraz z rozmiarami prostokątów
    df['XL'] += df['x1']
    df['YL'] += df['y1']
    
    # Zabezpieczenie przed kolizją prostokątów
    for i in range(len(df)):
        while any((df['XL'][i]+df['w'][i] > df['XL'][:i]) & (df['XL'][i] < df['XL'][:i]+df['w'][:i]) &
                  (df['YL'][i]+df['h'][i] > df['YL'][:i]) & (df['YL'][i] < df['YL'][:i]+df['h'][:i])):
            df.at[i, 'XL'] = np.random.randint(0, width - df['w'][i]) + df['x1'][i]
            df.at[i, 'YL'] = np.random.randint(height_0, height_1 - df['h'][i]) + df['y1'][i]
    # Usunięcie niepotrzebnych kolumn
    df.drop(['w', 'h'], axis=1, inplace=True)
    
    return df

def generate_image(img_path, df, font_scale=1.0, color=(255, 255, 255), thickness=1, font_face=cv.FONT_HERSHEY_DUPLEX):
    '''
    ASSUMPTION
    Nieintuicyjne ale img musi istniec juz przed wywolaniem funkcji!
    bo nadpisuje sie caly czas w tym samym miejscu
    '''
    img = cv.imread(img_path)
    def remove_polish_chars(text):
        polish_to_english_map = {
        'ż': 'z', 'ź': 'z', 'ć': 'c', 'ą': 'a', 'ę': 'e',
        'ł': 'l', 'ó': 'o', 'ś': 's', 'ń': 'n',
        'Ż': 'Z', 'Ź': 'Z', 'Ć': 'C', 'Ą': 'A', 'Ę': 'E',
        'Ł': 'L', 'Ó': 'O', 'Ś': 'S', 'Ń': 'N'
        }
        for char, replacement in polish_to_english_map.items():
            text = text.replace(char, replacement)
        return text
    for index, row in df.iterrows():
        x_pos = row['XL']
        y_pos = row['YL']
        text = remove_polish_chars(row["Case"])
        
        cv.putText(img, text, (x_pos,y_pos), font_face, font_scale, color, thickness)
    cv.imwrite(img_path, img)
   


def generate_all_levels(df):
    for i in range(1,9):
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {i}")
        h0,h1 = level_spaces[i]
        h0+=10
        minidf = df[df["Label"]==i].copy()
        minidf = minidf.reset_index(drop=True)
        print(minidf)
        test_df = add_random_positions(minidf, width=1250, height_0=h0, height_1=h1)
        generate_image("INOUTIMAGE.jpg",test_df)
        
        
generate_all_levels(df)



'''
# BEDE ITEROWAL PO DF ROW xd
for index, row in df.iterrows():
   
import random

def main():
    pro_width = 1800
    pro_height = 450
    n = 10 # liczba prostokatów ze zbioru N
    min_rect_width = 10
    max_rect_width = 500
    rect_height = 30
    rects = []

    for i in range(n):
        rect_width = random.randint(min_rect_width, max_rect_width)
        rect_x = random.randint(0, pro_width - rect_width)
        rect_y = random.randint(0, pro_height - rect_height)
        rect = (rect_x, rect_y, rect_width, rect_height)
        while overlap(rect, rects):
            rect_x = random.randint(0, pro_width - rect_width)
            rect_y = random.randint(0, pro_height - rect_height)
            rect = (rect_x, rect_y, rect_width, rect_height)
        rects.append(rect)

def overlap(rect, rects):
    for r in rects:
        if (rect[0] < r[0] + r[2] and rect[0] + rect[2] > r[0] and
            rect[1] < r[1] + r[3] and rect[1] + rect[3] > r[1]):
            return True
    return False

if __name__ == "__main__":
    main()


max_iterations = 1000
iterations = 0
while overlap(rect, rects) and iterations < max_iterations:
            rect_x = random.randint(0, pro_width - rect_width)
            rect_y = random.randint(0, pro_height - rect_height)
            rect = (rect_x, rect_y, rect_width, rect_height)
            iterations += 1

if iterations == max_iterations:
    print("Nie można znaleźć wolnego miejsca na kolejny prostokąt.")
   
'''
