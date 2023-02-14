# -*- coding: utf-8 -*-
"""
@Author: DFGANDP

Dzialanie algorytmu:
    1. wpisywanie w cmd CO + Level  (+ oraz -)
    2. otworz plik wpisz i show, po wpisaniu nastepnej rzeczy zamknij otworz + show

"""

import cv2
import pandas as pd
import numpy as np

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


def draw_text_on_image(img, text, x, y, font_scale=1.0, color=(255, 255, 255), thickness=1, font_face=cv2.FONT_HERSHEY_DUPLEX):
    '''
    wpisz cos w losowym miejscu i zwroc koordynaty gdzie to wpisales (NA zdjeciu nie nad lub pod)
    # wysokosc tekstu 24
    
    X - width
    Y - Height
    
    
    --------------------------
    Returns:
        text_rexc : list
            (x,y,x_1+3,y_1+3)
    '''
    
    text = remove_polish_chars(text)
    text_size, baseline = cv2.getTextSize(text, font_face, font_scale, thickness)
    y_text=y+24 # wysokosc tekstu
    text_width, text_height = text_size
    text_rect = (x, y, x + text_width+3, y+text_height+3)
    cv2.putText(img, text, (x,y_text), font_face, font_scale, color, thickness)
    return text_rect

def read_data(img_pth='sheets_test.jpg',data_pth='Iceberg_Preprocess_v2.xlsx',save=False):
    # Wczytanie danych z pliku excel
    df = pd.read_excel(data_pth)
    
    # Wczytanie zdjęcia
    img = cv2.imread(img_pth)
    
    # Ustawienie wymiarów sekcji
    section_height = int(img.shape[0] / 8)
    occupied_coords = {} # dodac klucz jako Case i Value jako koordynaty sprawdzic czy sie nie przecina!
    
    # Petla przetwarzająca każdy label
    
    # LINIA ZAJMUJE 10 pixeli
    for label in range(1, 9):
        # Wyszukanie wszystkich tekstów z danego labela
        texts = df[df['Level'] == label]['Case'].tolist()
        print(label)
        print(texts)
        
        # Get segment coordinates
        print(section_height)
        for text in texts:
            print(text)
            text_rect = draw_text_on_image(img, text, 0, 0)
            print(text_rect)
            text_rect = draw_text_on_image(img, text, 0, text_rect[3])
            print(text_rect)
            break
        break
        '''
        # Przygotowanie pustej macierzy do przechowywania współrzędnych istniejących tekstów
        occupied_coords = np.zeros((section_height, section_width), dtype=np.int32)
        
        # Petla przetwarzająca każdy tekst z danego labela
        for text in texts:
            # Losowanie pozycji tekstu
            position_found = False
            while not position_found:
                y = np.random.randint(0, section_height)
                x = np.random.randint(0, section_width)
                
                # Sprawdzenie, czy pozycja nie jest juz zajeta
                if occupied_coords[y][x] == 0:
                    position_found = True
                    occupied_coords[y][x] = 1
                    
                    # Wpisanie tekstu na zdjęcie
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 1
                    thickness = 2
                    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
                    text_start_x = x - text_width // 2
                    text_start_y = y - text_height // 2
                    text_end_x = x + text_width // 2
                    text_end_y = y + text_height // 2
                    cv2.putText(img, text, (text_start_x, text_start_y), font, font_scale, (0, 0, 0), thickness)
        '''
    #cv2.imshow('haha',img)
    if save is True:
        # Zapisanie zdjęcia
        cv2.imwrite('output.jpg', img)
read_data(save=True)