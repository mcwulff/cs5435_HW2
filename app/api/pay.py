from bottle import (
    post,
    request,
    response,
    jinja2_template as template,
)

from app.models.user import (
    get_user,
)

from app.models.session import (
    logged_in,
)


@post('/pay')
@logged_in
def do_payment(db, session):
    print("this is the session Id: " + session.get_id());
    #print("this is the id of the person making the req" + request.forms.get('csrf-id'))
    sender = get_user(db, session.get_username())
    print(session.get_id())
    recipient = db.execute(
        "SELECT * FROM users WHERE users.username='{}' LIMIT 1 OFFSET 0".format(
            request.forms.get('recipient')
        )
    ).fetchone()
    payment_amount = int(request.forms.get('amount'))
    error = None
    if (session.get_id() != request.forms.get('csrf-id')):
        response.status = 400
        error = "Seperate entity trying to make a request on behalf of user" 
    elif (sender.get_coins() < payment_amount):
        response.status = 400
        error = "Not enough funds."
    elif (payment_amount < 0):
        response.status = 400
        error = "Payment amount cannot be negative."
    elif (recipient is None):
        response.status = 400
        error = "Recipient {} does not exist.".format(request.forms.get('recipient'))
    elif (recipient['username'] == sender.username):
        response.status = 400
        error = "Cannot pay self."
    else:
        sender.debit_coins(payment_amount)
        db.execute(
            "UPDATE users SET coins={} WHERE users.username='{}'".format(
                recipient['coins'] + payment_amount, recipient['username']
            )
        )
    return template(
        "profile",
        user=sender,
        session_user=sender,
        payment_error=error,
    )

