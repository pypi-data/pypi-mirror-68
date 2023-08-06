#zhangwei_helper
zhangwei_helper is a package include all common part,like function,enum,written \
by zhang wei(zwzw911)    
## install    
`pip install zhangwei-helper`    
## content    
### enum    
SelfEnum    
***description***: a module include self defined enum   
***usage***:     
import zhangwei_helper.SelfEnum as self_enum  
1. CpuBits: bits64/bits32    
2. OsType: Windows/Linux    
3. WindowsVersion: Windows7/Windows8/Windows10/Unknown    
4. WindowsBits: Win32/Win64    
5. PythonVersion: Python2/Python3/Unknown    
6. ProxyType: Transparent/Anonymous/High_anonymous    
7. BrowserType: FireFox/Chrome/All    
   
### function     
**os**     
***description***: a module include some functions about os   
***usage***:   
import zhangwei_helper.function.Os as zw_os     
1. get_cpu_bits(): 枚举(CpuBits)：cpu的位数    
2. get_os_type(): 枚举(OsType)：os的类型：windows或者linux    
3. get_windows_ver(): 枚举(WindowsVersion)：windows的版本（7/8/10）    
4. get_windows_bits(): 枚举(WindowsBits)：windows的位数：32或者64    
5. windows_login_as_admin(): Boolean：当前是否以admin登录    
6. get_python_major_version():枚举(PythonVersion)：返回python的大版本号：2或者3或者unknown 

**WindowsService**     
***description***: a module include some functions about os     
***usage***:    
import zhangwei_helper.function.WindowsServices as zw_winser   
1. if_service_exists(): Boolean：服务是否存在    
2. if_service_running(): Booleans:服务是否运行    
 
**Network**     
***description***: a module include some functions about network         
***usage***:   
import zhangwei_helper.function.Network as zw_network    
1. extract_protocol_from_url(url)：获得协议http或者https
2. extract_host_from_url(url)：获得host
3. extract_base_url_from_url(url)：获得基础url  https://github.com
4. gen_proxies_from_ip(ip): 根据IP生成request/request_html需要的代理
5. detect_if_need_proxy(url): Boolean:是否需要代理
6. detect_if_proxy_usable(proxies, timeout=5, url='https://www.baidu.com'）：Boolean：代理是否有效
7. detect_url_exist(url, proxies, headers): url是否存在（返回404）
8. send_request_get_response(**args): request_html或者error。同步获得页面html
9. async_send_request_get_response(**args): request_html或者error。异步获得页面html
10. download_file(url,save_path): Error(下载失败）；None（下载成功）
11. download_unzip_chrome_driver     
12. download_unzip_firefox_driver      
 
**Software**     
***description***: a module include some functions about software             
***usage***:   
1. check_minimum_python_version(ver=str): Error（python版本不匹配或者未安装）；python安装路径
2. check_firefox_version(): None（未安装FF）；FF版本（自动补齐.0）
3. check_chrome_version(): None（未安装）：chrome版本
4. check_driver_exist(python_dir, browser_type): 检查对应的driver在python目录下是否存在
5. unzip_file():解压zip文件到指定目录
6. is_valid_zip_file():是否为合格的zip文件

**Regedit**     
***description***: a module include some functions to operate windows reg              
***usage***:  
1. _open_item: 返回item
2. _read_key_value：读取item下一个key的值和类型
3. _save_key_value：以某种类型的方式，把值保存到某个key中
4. read_PATH_value：读取环境变量PATH的值
5. append_value_in_PATH：为PATH添加一个值
6. del_value_in_PATH：从PATH中删除一个值
7. check_key_value_exists(key,value_name)：检查某个key小，value_name是否存在
8. create_value(key,value_name,value_type,value): 直接调用_save_key_value
9. delete_value(key,value_name): 删除key下的value

### change history
0.0.1  add SelfEnum/Os/WindowsServices  
0.0.2  add const/Const.py, function/Network.py, function/Software  
0.0.3  add function/TypeCheck, add new enum VariantType, add test case for function/TypeCheck
0.0.4  fix issue of network/gen_proxies_from_ip & download_file & download_unzip_firefox_driver
0.0.5  add new function/Regedit.py, to operate windows reg
0.0.6  add create/delete_value/check_key_value_exists in function/Regedit.py