from celery import task

import sendgrid
from sendgrid.helpers.mail import *
from myshop.settings import ADMIN_EMAIL, SENDGRID_API_KEY

from .models import Order


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    subject1 = 'Замовлення з магазину Меблі-Лем'
    message = 'Ваше замовлення оформлено. Номер вашого замовлення № {}'.format(order.id)
    message += '\n З Вами зв\'яжеться менеджер \n\n З повагою, магазин "Меблі-Лем"'
    content = Content("text/plain", message)
    from_email = Email(ADMIN_EMAIL)
    to_email = Email(order.email)

    # subject2 = 'Поступило Замовлення (Меблі-Лем)'
    # message_admin = 'Замовник {0} {1} з {2} \n оформив замовлення № {3}'.format(order.first_name,
    #                                                                            order.last_name, order.address,
    #                                                                            order.id)
    # message_admin += '\n Телефон замовника {}'.format(order.phone)
    # content_admin = Content("text/plain", message_admin)
    mail = Mail(from_email, subject1, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    return response


"""
    mail_admin = Mail(from_email, subject2, from_email, content_admin)
    response = sg.client.mail.send.post(request_body=mail_admin.get())

    return
"""
