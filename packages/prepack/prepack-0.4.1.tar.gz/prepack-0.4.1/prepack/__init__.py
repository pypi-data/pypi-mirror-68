class prepack:
    """Data preparation library"""

    def __init__(self):
        pass

    # вычисляет пересечение списков
    @staticmethod
    def list_intersect(lst1, lst2):
        return set(lst1).intersection(lst2)

        # вычисляет разницу списков

    @staticmethod
    def list_diff(lst1, lst2):
        return set(lst1) - set(lst2)

    @staticmethod
    def isnan(v):
        import math as m
        if isinstance(v, float) and m.isnan(v):
            return True
        else:
            return False

    @staticmethod
    def list_concat(lst1, lst2):

        lst3 = []
        size1 = len(lst1)
        size2 = len(lst2)
        # здесь будет размер самого длинного списка
        size_max = max(size1, size2)

        # вытаскиваем и делаем строковыми значения из обоих списков
        for i in range(size_max):
            ss = ''
            if i < size1 and not prepack.isnan(lst1[i]):
                s = str(lst1[i])
                if len(s) > 0:
                    ss += s
            if i < size2 and not prepack.isnan(lst2[i]):
                s = str(lst2[i])
                if len(s) > 0:
                    if len(ss) > 0:
                        ss += ' '
                    ss += s
            # кладем все в список в виде объединенных значений
            lst3 += [ss]
        return lst3

    @staticmethod
    def p2c(lst):
        res_string = ''
        import numpy as np
        length = len(lst)
        max_len = max(len(repr(el)) for el in lst)
        # делаем кортеж со значениями из списка
        cols = tuple(lst)
        # делаем массив из кортежа названий и диапазона от 0 до length, .T транспонирует матрицу
        a = np.array([np.arange(length), cols]).T

        # смотрим форму массива, по оси 0 - это y, и по оси 1 - это x
        y, x = a.shape

        # берем половину массив, округляя в большую сторону
        col1 = a[:int(np.ceil(y / 2))].copy()
        # оставщаяся часть
        col2 = a[int(np.ceil(y / 2)):].copy()

        # определяем максимальную длину колонок, чтобы увеличить одну из колонок, если она получилась короче,
        # например, когда
        # кол-во столбцов было изначально 3, первая колонка будет длиной 2, а вторая 1
        length = max(col1.shape[0], col2.shape[0])

        # меняем размер колонок по максимальной длине
        col1.resize([length, 2])
        col2.resize([length, 2])

        # Приходится изворачиваться, у Питона нет ++/-- для инкремента/декремента. Те мелочи,
        # за которые я не люблю Питон
        i = 0
        while i < length:
            c1 = str(col1[i][0]).ljust(3)  # первая колонка
            c2 = repr(col1[i][1]).ljust(max_len + 3)
            c3 = str(col2[i][0]).ljust(3)  # вторая колонка
            c4 = repr(col2[i][1])
            res_string += c1 + c2 + c3 + c4 + '\n'
            i += 1
        return res_string

    # тут пара функций для удобного сохранения из загрузки
    @staticmethod
    def load(filepath):
        import pickle as pkl
        with open(filepath, "rb") as f:
            return pkl.load(f)

    @staticmethod
    def save(data, filepath):
        import pickle as pkl
        with open(filepath, "wb") as f:
            return pkl.dump(data, f, 2)  # 2 is protocol version

    @staticmethod
    def read_excels(filepath):
        import pandas as pd
        return pd.read_excel(filepath, sheet_name=None, header=None, na_filter=False, dtype=str)

    @staticmethod
    def read_excel(filepath):
        import pandas as pd
        return pd.read_excel(filepath, header=None, na_filter=False, dtype=str)

    @staticmethod
    def read_zip(filepath):
        import zipfile as zip_
        z = zip_.ZipFile(filepath, mode='r')
        names = tuple(z.namelist())
        lst = []
        for f in names:
            lst += [z.open(f)]
        return names, tuple(lst)

    @staticmethod
    def df_filter_and(df, fltr, iloc=False):
        import numpy as np
        lst = prepack.df_filter_parse_conditions(df, fltr, iloc)
        if len(lst) == 1:
            return lst[0]
        else:
            res = lst[0]
            for i in range(1, len(lst)):
                res = np.logical_and(res, lst[i])
            return res

    @staticmethod
    def df_filter_or(df, fltr, iloc=False):
        import numpy as np
        lst = prepack.df_filter_parse_conditions(df, fltr, iloc)
        if len(lst) == 1:
            return lst[0]
        else:
            res = lst[0]
            for i in range(1, len(lst)):
                res = np.logical_or(res, lst[i])
            return res

    # Этот метод нужен для подготовки списка масок для методов df_filter_or df_filter_and
    @staticmethod
    def df_filter_parse_conditions(df, fltr, iloc):
        lst = []
        for col in fltr:
            cond = fltr[col]
            lst += prepack.df_filter_parse_condition(df, col, cond, iloc)
        return lst

    @staticmethod
    def df_filter_parse_condition(df, col, cond, iloc):
        lst = []
        class_ = cond.__class__.__name__

        if class_ == 'str':
            mask = prepack.df_filter_prepare_mask(df, col, cond, iloc)
            lst.append(mask)
        elif class_ in ['list', 'tuple']:
            for c in cond:
                mask = prepack.df_filter_prepare_mask(df, col, c, iloc)
                lst.append(mask)
        return lst


    @staticmethod
    def df_filter_prepare_mask(df, col, cond, iloc=False):
        lst = []
        operator = str(cond)[:1]

        if operator in ['~', '>', '<']:
            cond = cond[1:]
        else:
            operator = None

        if iloc:
            s = df.iloc[:, col]
        else:
            s = df.loc[:, col]
        
        if cond == 'isnum':
            mask = s.astype(str).str.replace('.', '').str.isnumeric()
        elif cond == 'isblank':
            mask = s.astype(str).str.strip() == ''
        elif cond == 'istext':
            m1 = ~(s.astype(str).str.strip() == '')
            m2 = ~s.astype(str).str.replace('.', '').str.isnumeric()
            mask = m1 & m2
        elif cond[:9] == 'contains=':
            import re
            cond = cond[9:]
            mask = s.astype(str).str.contains(cond, flags=re.IGNORECASE, na=False, regex=True)
        else:
            if operator == '<':
                mask = s < cond
            elif operator == '>':
                mask = s > cond
            else:
                mask = s == cond

        if operator == '~':
            return ~mask
        else:
            return mask


    # делает слияние двух датафреймов через наиболее близкое расстояние Левенштейна,
    # лимит по расстоянию в % от длины длинной строки
    @staticmethod
    def levenshtein_merge(dfa, dfb, left_on, right_on, limit=90):
        import pandas as pd
        import Levenshtein as l
        a = dfa[left_on]
        b = dfb[right_on]
        klist = [None] * len(a)
        lena = len(dfa.columns)
        lenb = len(dfb.columns)
        bcols = list(range(lena, lena + lenb))  # bcols is a list with dfb columns indexes after concatenation

        res = dfa
        to_concat = pd.DataFrame([], columns=dfb.columns)
        res = pd.concat([res, to_concat], axis=1)  # this will add columns to res from dfb

        for i in a.index:
            ival = a[i]
            maxdst = 0x7FFFFFFF  # reset max distance on each cycle. #0x7FFFFFFF is a max integer
            for k in b.index:
                kval = b[k]
                dst = l.distance(ival, kval)
                if dst < maxdst:  # if current distance less than saved
                    maxdst = dst
                    max_len = max(len(ival), len(kval))  # maximum length of compared strings
                    if dst <= limit / 100 * max_len:  # if the current distance is less than or equal to a
                        # percentage of the length
                        klist[i] = k

                    if maxdst == 0:  # stop if strings are equals
                        break

            if klist[i] is not None:  # if index found than
                res.iloc[i, bcols] = list(
                    dfb.iloc[klist[i], :])  # set dfb columns values in res row to klist[i] row in dfb

        return res

    @staticmethod
    def parse_excel(filepath, columns, fltr, header=None):
        pp = prepack
        df = pp.read_excel(filepath)

        # лишние столбцы
        # данные только с 0 по 12 столбец
        df = df.iloc[:, columns[0]:columns[1]]

        if header:
            # вытащим заголовки столбцов из нужных строк в файле
            cols = []
            for i in header:
                cols = pp.list_concat(cols, list(df.iloc[i]))

            # очистка названий от переносов строк
            for i, el in enumerate(cols):
                cols[i] = cols[i].replace('\n', '')

                # устанавливаем названия
            df.columns = cols

        # фильтруем строки
        f = pp.df_filter_and(df, fltr, True)
        df = df[f].reset_index(drop=True)

        return df

    @staticmethod
    def parse_excels(filelist, columns, fltr, header=None):
        pp = prepack
        import pandas as pd

        # тут отдельно обработаем первый файл
        dff = []
        cols = []
        filepath = filelist[0]

        df = pp.parse_excel(filepath=filepath, columns=columns, fltr=fltr, header=header)

        # Если есть заголовки, сохраним их в cols
        if header:
            cols = list(df.columns)
            # тут поставим числовые заголовки
            df.columns = range(0, len(df.columns))

        # добавим столбец с именем файла источника
        df['src_filename'] = pp.get_filename(filepath)

        # запишем
        dff.append(df)

        for i in range(1, len(filelist)):
            filepath = filelist[i]
            df = pp.parse_excel(filepath=filepath, columns=columns, fltr=fltr, header=None)
            df['src_filename'] = pp.get_filename(filepath)
            dff.append(df)

        res = pd.concat(dff, axis=0).reset_index(drop=True)
        if header:
            cols.append('src_filename')
            res.columns = cols

        return res

    @staticmethod
    def get_filename(filepath):
        import os
        # Если передан file-like object, то у него будет аттрибут read
        if hasattr(filepath, 'read'):
            # тогда имя файла будет в аттрибуте name
            name = filepath.name
        else:
            name = filepath

        basename = os.path.basename(name)
        filename, ext = os.path.splitext(basename)

        return filename
