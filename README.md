Please read the [Document](https://github.com/Sciuromorpha/Documents/blob/main/README.md) in [Documents Repo](https://github.com/Sciuromorpha/Documents) .

项目的详细信息请查阅[项目文档库](https://github.com/Sciuromorpha/Documents)

## 项目配置

1. 克隆本代码仓库，使用 `poetry install` 进行引用包安装；
2. 使用 `poetry shell` 进入项目虚拟环境；
3. 编辑 `config.ini` 配置运行模式、数据库、MQ 等必要信息；
4. 在 `src` 目录下执行 `alembic upgrade head` 来合并数据库架构；
5. 使用 `faststream run sciuromorpha_core:app` 来启动服务；