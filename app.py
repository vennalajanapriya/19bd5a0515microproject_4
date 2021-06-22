import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests
import requests_cache

account_sid = 'AC418ef24f46773abf96c1aa0a09c17847'
auth_token = '1f548809678e1b208096e1282e5927ac'
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    print("test")
    return render_template('loginpage.html')


@app.route('/loginpage', methods=['POST', 'GET'])
def user_registration():
    print("register")
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email_id']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['id_card']
    date = request.form['trip']
    full_name = first_name + "." + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt / pop) * 100)
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to="whatsapp:+918977524503",
                               from_="whatsapp:+14155238886",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " " + " To " + " " + destination_dt + " " +
                                 "Has" + " " + status + " On " + " " + date + " ")

        return render_template('user_registration.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)

    else:
        status = 'Not Confirmed'
        client.messages.create(to="whatsapp:+918977524503",
                               from_="whatsapp:+14155238886",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " " + "To" + " " + destination_dt + " " +
                                    "Has" + " " + status + "On" + " " + date + " " + ", Apply later")

        return render_template('user_registration.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)


if __name__ == "__main__":
    app.run(port=9002, debug=True)
