import pandas as pd
from IPython.display import display
from os.path import abspath, split, join, dirname

def multi_columns(data_frame):
	"""
	:param dataframe (Pandasのread_excelで読込んだMultiIndexのあるDataFlames):
	:return Excelに近い構成のMultiIndexに直して返す:
	"""

	df = data_frame.copy()
	if type(df.columns) is not pd.MultiIndex:
		return df

	# 列にUnnamedという文字の入った内容を削除しインデックスを振り直す
	df = df.rename(columns=lambda x: x if not 'Unnamed' in str(x) else '')
	df = df.reset_index()

	cols = df.columns
	copy_col = list(cols)

	# column.namesを新しいcolumnの一番上(インデックスセルの一番左)に持ってくる
	name_col = tuple([(name if name is not None else '') for name in cols.names])
	copy_col[0] = name_col

	# 無効セルは上に詰める
	for i, col in enumerate(copy_col):
		pack = [content for content in col if content != ""]
		copy_col[i] = tuple(pack + ([""] * (len(col)  - len(pack))))

	df.columns = pd.MultiIndex.from_tuples(copy_col)
	cols.names = tuple([None for x in cols.names])
	return df

if __name__ == '__main__':
	pjc_folder = abspath(dirname(__file__))

	xl_file = 'test_col3.xlsx'
	xi_path = join(pjc_folder, 'file', xl_file)

	df = pd.read_excel(xi_path, skiprows=2, header=[0, 1, 2])
	df = multi_columns(df)
	print(df)