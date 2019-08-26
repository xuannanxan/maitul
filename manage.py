# -*- coding: utf-8 -*-
# Created by xuannan on 2019-01-01.
import os
from app import create_app

# 生成app
app = create_app()

if __name__ == '__main__':
    app.run()
