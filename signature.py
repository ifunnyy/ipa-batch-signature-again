# -*- coding: utf-8 -*-

__author__ = 'Johnny'
__describe__ = 'cd到脚本目录下，描述文件也放在脚本目录下，需要签名的包放在ipas里面'

import os
import commands

def run():
    #重签文件夹
    iDir = 'ipas'

    #成果文件夹
    rDir = 'results'

    #描述文件名称 (描述文件放在ipa目录下)
    mobileprovision = 'xxxx.mobileprovision'

    #证书
    certificate = 'iPhone Distribution: xxxx'

    ipaPaths = []

    results = {}

    if not os.path.exists(mobileprovision):
        print '找不到证书'
        return

    if not os.path.isdir(iDir):
        os.mkdir(iDir)

    os.system('rm -fr %s' %(rDir))
    os.mkdir(rDir)

    for (_, _, files) in os.walk(iDir):
        for file in files:
            if file.endswith('.ipa'):
                ipaPaths.append(iDir + '/' + file)

    if len(ipaPaths) == 0:
        print '没有需要签名的ipa'
        return

    print '需要重签的文件(%s个):' %(len(ipaPaths))
    for ipaPath in ipaPaths:
        print "   " + ipaPath.split('/')[-1]
        results[ipaPath.split('/')[-1].replace('.ipa', '')] = 'none'

    raw_input('\n输入任意字符继续,或者control+c退出:')

    os.system('security cms -D -i %s > t_entitlements_full.plist' %(mobileprovision))
    os.system('/usr/libexec/PlistBuddy -x -c \'Print:Entitlements\' t_entitlements_full.plist > entitlements.plist')

    if not os.path.exists('entitlements.plist'):
        print 'entitlements.plist 生成错误'
        return

    os.chdir(rDir)
    i = 0
    for ipaPath in ipaPaths:
        fileName = ipaPath.replace('.ipa', '').split('/')[-1]

        os.system('unzip ../%s -x __MACOSX/*' %(ipaPath))

        os.system('rm -rf Payload/%s.app/_CodeSignature/' %(fileName))

        os.system('cp ../%s Payload/%s.app/embedded.mobileprovision' %(mobileprovision, fileName))

        (status, output) = commands.getstatusoutput('/usr/bin/codesign -f -s "%s" --entitlements ../entitlements.plist Payload/%s.app/' %(certificate, fileName))

        if 'replacing existing signature' in output:
            os.system('rm -fr %s.ipa' %(fileName))
            os.system('zip -r %s.ipa Payload/' %(fileName))
            results[fileName] = 'yes'
        else:
            print 'error:'
            print output
            print '-----------------------------'

            results[fileName] = 'error: %s' %(output)

        os.system('rm -fr Payload')

    print '\n结果为：\n'
    for key in results:
        print '%s 结果为:%s' %(key, results[key])

    print ''

    os.chdir('..')
    os.system('rm -fr entitlements.plist')
    os.system('rm -fr t_entitlements_full.plist')


if __name__ == '__main__':
    run()
