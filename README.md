#### 环境配置
推荐使用[uv工具](https://github.com/astral-sh/uv)或者venv虚拟环境
1. uv管理环境
```shell
uv venv
uv sync
uv run python Qt-Tools.py
```
2. venv管理环境
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
**注意**，如果使用venv管理环境，python版本需指定为3.12.*
3. conda管理环境
```shell
conda create -n qt-tools python=3.12.*
conda activate qt-tools
pip install -r requirements.txt
```
#### 打包
如果使用uv管理环境，可以直接运行
```shell
uv run python deploy.py
```
如果使用其他管理环境，需要先安装`nuitka`包