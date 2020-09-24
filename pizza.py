from flask import Flask,request,jsonify,render_template
import MysqlConnection as connect
import Mysqlresponse as response
import Mysqlerror as er
app = Flask(__name__)
@app.route("/")
def index():
     return render_template("index.html") #to send context to html

@app.route("/webhook", methods=['POST','GET'])
def webhook():
    req = request.get_json(silent=True, force=True)
    temp = insert(req)
    return temp
@app.route("/insert",methods = ['get','post'])
def insert(req):
    con = connect.connect_mysql()
    if con is False:
        speech = "Sorry some error has occurred while connecting to database try again later!"
        return {
            "fulfillmentText": speech,
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                        "simpleResponses": [{
                            "textToSpeech": speech
                        }]
                    }
                }]

        }
    else:
        try:
            pizza_name = req.get('queryResult').get('parameters').get('pizza_name')
            pizza_size = req.get('queryResult').get('parameters').get('pizza_size')
            crust_pizza = req.get('queryResult').get('parameters').get("crust_pizza")
            topping = req.get('queryResult').get('parameters').get("topping")
            count_pizza = req.get('queryResult').get('parameters').get("count_pizza")
            cust_name  = req.get('queryResult').get('parameters').get("cust_name")['name']
            phone_no = req.get('queryResult').get('parameters').get("phone_no")
            mail_id = req.get('queryResult').get('parameters').get("mail_id")
            address =req.get('queryResult').get('parameters').get("address")
            status = req.get('queryResult').get('parameters').get("confirmation")
            payment = req.get('queryResult').get('parameters').get("payment")
            amt = int(int(req.get('queryResult').get('parameters').get("count_pizza"))*230)
            cur_con = con.cursor()
            print(amt)
            print(phone_no)
            print(topping)
            query = "insert into testing15(pizza_name,pizza_size,crust_pizza,pizza_toppings,pizza_count,cust_name,phone_no,mail_id,address,status,payment,amt) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            val = (pizza_name, pizza_size, crust_pizza, topping, count_pizza, cust_name, phone_no, mail_id, address, status,payment, amt)
            cur_con.execute(query, val)
            con.commit()
            order_id = cur_con.lastrowid
            speech = "Your order has been recorded successfully! <br/> Order_id : " + str(order_id) + "<br/> Name : " + cust_name + "<br/> Ordered Pizza : " + str(pizza_name) + " " + pizza_size + " " + "<br/> Amount : " + str(amt) + "<br/> status : ordered."
            return {
                "fulfillmentText": speech,
                "fulfillmentMessages": [
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "simpleResponses": {
                            "simpleResponses": [{
                                "textToSpeech": speech
                            }]
                        }
                    }]
            }
        except Exception as e:
            speech = "Some error has occurred!"
            return {
                "fulfillmentText": speech,
                "fulfillmentMessages": [
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "simpleResponses": {
                            "simpleResponses": [{
                                "textToSpeech": speech
                            }]
                        }
                    }]

            }




if __name__ == "__main__":
    app.run(debug=True,port = 80)