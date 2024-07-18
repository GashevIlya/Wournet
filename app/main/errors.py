from app.manage import app
from flask import render_template


@app.errorhandler(404)
def error_404(error):
    return render_template('errors.html', title='Страница не найдена',
                           message='К сожалению, запрашиваемая страница не найдена...')


@app.errorhandler(403)
def error_403(error):
    return render_template('errors.html', title='Доступ запрещен',
                           message='Возможно, вы не зарегистрировались на сайте. Повторите попытку...')


@app.errorhandler(505)
def error_505(error):
    return render_template('errors.html', title='Неполадки с сервером',
                           message='На сайте происходят технические неполадки. Повторите попытку позже...')

