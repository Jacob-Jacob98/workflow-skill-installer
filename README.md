# 两个 Codex 技能的安装器

安装图片提示词复刻（image-prompt-replication）和婚礼音乐工作流（wedding-music-workflow）。需要 Codex、Python 3.8 或更高版本，以及发布者提供的安装码。

## Windows 安装

在 PowerShell 运行以下命令。它会下载指定版本的安装脚本并启动它。

```powershell
$p = Join-Path $env:TEMP 'workflow-skill-install.py'; Invoke-WebRequest -UseBasicParsing -ErrorAction Stop 'https://raw.githubusercontent.com/Jacob-Jacob98/workflow-skill-installer/2d3e7529732f7b89b3261de786f9b79eaa496ae9/install.py' -OutFile $p; python $p
```

按提示输入安装码，输入时字符隐藏。显示安装成功后重启 Codex。安装器使用 CODEX_HOME 指定的技能目录，默认安装到用户目录下的 .codex/skills。已存在的同名目录会保留。

## macOS 或 Linux 安装

```sh
p=$(mktemp) && curl -fsSL 'https://raw.githubusercontent.com/Jacob-Jacob98/workflow-skill-installer/2d3e7529732f7b89b3261de786f9b79eaa496ae9/install.py' -o "$p" && python3 "$p"
```

安装码自激活起 24 小时有效，每码可兑换一份包含两个技能的安装包。下载遇到临时网络错误时，安装器会用同一兑换凭证重试。使用技能时所需的外部工具和账号请按各技能的说明配置。
