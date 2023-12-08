#! /usr/bin/env python3
import os
import sys

from base import Base

current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

class Csmpreinstaller:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger

    # 修改配置文件参数
    def modify_fstab_file(self):  
        # 执行命令
        command = "swapoff -a"
        self.base.com(command)

        try:
            file_path = '/etc/fstab'
            self.logger.log(f"修改配置文件参数：{file_path}")
            new_content = ""

            # 打开文件并读取内容
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # 遍历文件的每一行，查找并替换目标参数
            for line in lines:
                if "/swap.img      none    swap    sw      0       0" in line:
                    new_content += '#/swap.img      none    swap    sw      0       0'
                else:
                    new_content += line

            # 打开文件并写入修改后的内容
            with open(file_path, 'w') as file:
                file.write(new_content)

            return True
        except Exception as e:
            print(f"修改配置文件参数发生错误：{e}")
            self.logger.log(f"修改配置文件参数发生错误：{e}")  # debug
            return False
        
    # 添加密钥
    def add_key(self):
        print("添加密钥")
        command = "mkdir -m 0755 -p /etc/apt/keyrings"
        result = self.base.com(command)
        if result.returncode != 0:
            print("添加密钥失败")
            exit()

        command = "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
        result = self.base.com(command)
        if result.returncode != 0:
            print("添加密钥失败")
            exit()

        command = 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
        result = self.base.com(command)
        if result.returncode != 0:
            print("添加密钥失败")
            exit()
        print("添加密钥成功")

    # 执行安装
    def install_(self):
        print("执行安装docker")
        command = "apt-get update"
        result = self.base.com(command)
        if result.returncode != 0:
            self.base.logger.log(f"{command}, 执行失败")

        command = "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
        result = self.base.com(command)
        if result.returncode != 0:
            self.base.logger.log(f"{command}, 执行失败")
            
        command = 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
        result = self.base.com(command)
        if result.returncode != 0:
            self.base.logger.log(f"{command}, 执行失败")
            
        print("安装docker完成")

    def start_docker(self):
        command = "systemctl start docker"
        result = self.base.com(command)

        command = "systemctl enable docker"
        result = self.base.com(command)

        try:
            # 检查 Docker 服务状态
            command = "systemctl is-active docker"
            result = self.base.com(command)
            if result.stdout == "active":
                return "Docker 已启动"
            else:
                return "Docker 未启动"
        
        except Exception as e:
            self.logger.log(f"发生错误：{str(e)}")
            return f"发生错误：{str(e)}"

    def install_kubernetes(self):

        # 添加 Kubernetes 的 GPG 密钥
        command = "curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -"
        result = self.base.com(command)
        if result.returncode != 0:
            self.base.logger.log(f"执行失败")
            print("添加 Kubernetes 的 GPG 密钥失败")
        else:
            print("添加 Kubernetes 的 GPG 密钥成功")

        # 将 Kubernetes 源加入源列表
        kubernetes_source = '''echo "deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main" >/etc/apt/sources.list.d/kubernetes.list'''
        result = self.base.com(kubernetes_source)
        if result.returncode != 0:
            self.base.logger.log(f"执行失败")
            print("Kubernetes 源加入源列表失败")
        else:
            print("Kubernetes 源加入源列表成功")    

        # 更新源
        command = "apt-get update"
        result = self.base.com(command)
        if result.returncode != 0:
            self.base.logger.log(f"执行失败")
            print("更新源失败")
        else:
            print("更新源成功")

        # 安装指定版本的 Kubernetes 相关软件
        command = "apt-get install kubeadm=1.20.5-00 kubectl=1.20.5-00 kubelet=1.20.5-00 -y"
        result = self.base.com(command)
        if result.returncode != 0:
            self.base.logger.log(f"执行失败")
            print("安装 Kubernetes 相关软件失败")
        else:
            print("安装 Kubernetes 相关软件成功")