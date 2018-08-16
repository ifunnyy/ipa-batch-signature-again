# 脚本使用
1. 先把描述文件放在脚本目录下
2. 把需要打包的ipa放在ipas里
3. 打开终端，cd到脚本文件夹下
4. 调用python signature.py

# ipa重签
ipa 重签的操作主要分为以下几步：

1. 先将ipa包进行解压
2. 删除Payload/xxx.app/_CodeSignature里面的文件
3. 替换embedded.mobileprovision
4. 生成entitlements.plist
4. 进行重新签名
5. 重新打包

假设证书和ipa包都在同个目录下

## 先将ipa包进行解压

````
unzip xxx.ipa 
````

## 删除Payload/xxx.app/_CodeSignature里面的文件

````
rm -fr Payload/xxx.app/_CodeSignature/
````

## 替换embedded.mobileprovision

````
cp embedded.mobileprovision Payload/xxx.app/embedded.mobileprovision
````

## 生成entitlements.plist

````
security cms -D -i embedded.mobileprovision > entitlements_full.plist

/usr/libexec/PlistBuddy -x -c 'Print:Entitlements' entitlements_full.plist > entitlements.plist 
````

## 进行重新签名

````
/usr/bin/codesign -f -s "证书名称" --entitlements entitlements.plist Payload/xxx.app/ 
````

## 重新打包

````
zip -r xxx.ipa Payload/
````
