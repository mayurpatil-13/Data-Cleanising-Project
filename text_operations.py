import pandas as pd

def text_split(excel, column:str):
    max_width = 39
    specific_column = excel[column]
    index = excel.columns.get_loc(column)

    # specific_column.fillna('')
    specific_column = specific_column.str.wrap(max_width)
    specific_column.str.split(pat='\n', expand=True)
    split_df = pd.DataFrame(specific_column.str.split('\n').values.tolist())
    
    
    split_df.columns = ['delivery adress ' + str(i) for i in range(1, split_df.shape[1]+1)]
    # split_df = split_df.add_prefix('Delivery adress_')
    
    new_sheet = pd.concat([excel.iloc[:, :index], split_df, excel.iloc[:,index+1:]], axis=1)
    
    return new_sheet



def text_split2(excel, column:str):
    max_width = 39
    specific_column = excel[column]
    index = excel.columns.get_loc(column)

    # specific_column.fillna('')
    specific_column = specific_column.str.wrap(max_width)
    specific_column.str.split(pat='\n', expand=True)
    split_df = pd.DataFrame(specific_column.str.split('\n').values.tolist())
    
    
    split_df.columns = ['gift message ' + str(i) for i in range(1, split_df.shape[1]+1)]
    # split_df = split_df.add_prefix('Delivery adress_')
    
    new_sheet = pd.concat([excel.iloc[:, :index], split_df, excel.iloc[:,index+1:]], axis=1)
    
    return new_sheet