#!/bin/bash
# $1 需要监测的文件
# $2 存放文件md5值，用于判断文件是否更改
# $3 可选文件更新后，需要执行的命令（用'service nginx restart' 用单引号包起来）
# 适用场景，修改某配置文件或更新某文件以后自动处理某些事物
if [ ! $1 ] || [ ! $2 ] || [ ! -e $1 ] ; then
    echo "\$1 or \$2 is file"
    exit
fi
# 生成md5验证文件
function creatMd5file()
{
    md5sum -b $1 > $2
}

# 判断文件是否存在
if [ ! -e $2 ] ; then
    creatMd5file $1 $2
fi

while true
do
    # 检测文件是否修改，$?返回1 表示修改, 0表示未修改
    creatMd5file $1 $2
    md5sum -c $2 --status

    if [ $? -gt 0 ] ; then
        sh old_info_v1.sh > log/hy.log
        creatMd5file $1 $2

    fi
    # 每过3秒检测一次
    sleep 3
done
