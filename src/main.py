# coding=utf-8
"""启动程序"""
if __name__ == "__main__":
    from sys import version_info
    print(f"Python {version_info.major}.{version_info.minor}.{version_info.micro}")
    if float(f"{version_info.major}.{version_info.minor}") >= 3.12:
        try:
            import game
        except ModuleNotFoundError:
            print("警告：未安装pygame，请在终端输入> pip3 install pygame <安装pygame后再次启动")
            exit()
        else:
            # 初始化游戏页面实例
            game_pages: any = game.Pages()
            # 运行
            game_pages.logo_page()
    else:
        print("警告：python版本低于要求，请在> python.org <安装python3.12后再次启动")
        exit()
