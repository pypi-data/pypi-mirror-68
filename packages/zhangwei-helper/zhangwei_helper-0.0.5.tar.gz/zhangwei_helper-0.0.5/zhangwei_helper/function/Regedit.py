'''
对windows的注册表进行操作
_open_item: 返回item
_read_key_value：读取item下一个key的值和类型
_save_key_value：以某种类型的方式，把值保存到某个key中

read_PATH_value：读取环境变量PATH的值
append_value_in_PATH：为PATH添加一个值
del_value_in_PATH：从PATH中删除一个值
'''

import winreg


def _open_item(root_item_name,sub_item_name):
    try:
        sub_item = winreg.OpenKey(root_item_name, sub_item_name,0 ,winreg.KEY_ALL_ACCESS)
    except Exception as e:
        if root_item_name == winreg.HKEY_CURRENT_USER:
            root_item_name = 'HKEY_CURRENT_USER'
        elif root_item_name == winreg.HKEY_CLASSES_ROOT:
            root_item_name = 'HKEY_CLASSES_ROOT'
        elif root_item_name == winreg.HKEY_CURRENT_CONFIG:
            root_item_name = 'HKEY_CURRENT_CONFIG'
        elif root_item_name == winreg.HKEY_DYN_DATA:
            root_item_name = 'HKEY_DYN_DATA'
        elif root_item_name == winreg.HKEY_LOCAL_MACHINE:
            root_item_name = 'HKEY_LOCAL_MACHINE'
        elif root_item_name == winreg.HKEY_PERFORMANCE_DATA:
            root_item_name = 'HKEY_PERFORMANCE_DATA'
        elif root_item_name == winreg.HKEY_USERS:
            root_item_name = 'HKEY_USERS'
        raise EnvironmentError('注册表的项%s\%s不存在' % (root_item_name,sub_item_name))
    return sub_item
    # val, tpe = winreg.QueryValueEx(sub_item, key_name)


def _read_key_value(sub_item,key_name):
    val, tpe = winreg.QueryValueEx(sub_item, key_name)
    return val,tpe

def _save_key_value(sub_item,key_name,value_type,value):
    # key = winreg.OpenKey(sub_item,key_name)
    # v,t = _read_key_value(sub_item,key_name)
    winreg.SetValueEx(sub_item,key_name, 0, value_type, value)


def read_PATH_value():
    '''
    读取windown环境变量PATH的内容
    :return:
    '''
    root_item = winreg.HKEY_CURRENT_USER
    sub_item_name = r'Environment'
    key_name = r'PATH'
    sub_item = _open_item(root_item, sub_item_name)
    val, tpe = _read_key_value(sub_item, key_name)
    return val,tpe
    # print(val)

def append_value_in_PATH(v):
    '''
    把v添加到系统变量PATH中去
    :param v:
    :return:
    '''
    root_item = winreg.HKEY_CURRENT_USER
    sub_item_name = r'Environment'
    key_name = r'PATH'
    sub_item = _open_item(root_item, sub_item_name)
    val, tpe = _read_key_value(sub_item,key_name)
    #检测是否包含
    tmp = val.split(';')
    if v not in tmp:
        _save_key_value(sub_item, key_name, tpe,val+';'+v)

    winreg.CloseKey(sub_item)

def del_value_in_PATH(v):
    '''
    把v添加到系统变量PATH中去
    :param v:
    :return:
    '''
    root_item = winreg.HKEY_CURRENT_USER
    sub_item_name = r'Environment'
    key_name = r'PATH'
    sub_item = _open_item(root_item, sub_item_name)
    val, tpe = _read_key_value(sub_item,key_name)

    tmp = val.split(';')
    tmp.remove(v)
    _save_key_value(sub_item, key_name, tpe,';'.join(tmp))

    winreg.CloseKey(sub_item)
