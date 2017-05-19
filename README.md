＃UITesting_Log_Analyse
一，使用方法
使用时，直接调用：sh localPath/UI_Testing_Analyse.sh 
其中：
working_path='localPath'
//cd 到脚本目录下
cd ${working_path}

#用来区分具体的工程
python Log_HTML_Show.py '工程在 /Users/userName/Library/Developer/Xcode/DerivedData/ 的目录下的名称'

二、第三方库pyH安装后由于权限问题，import到本地文件后报错，所以直接下载，并复制到脚本的相同目录下
