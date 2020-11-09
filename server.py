
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, session, request,jsonify
from flask_socketio import SocketIO, emit
from flask_session import Session
from difflib import SequenceMatcher
from pathlib import Path
from api.ai import Agent
from datetime import date,datetime


import json
import apiai

'''

@author Salman Rakin

'''

count=0
stack=set()
fall_query=""
fall_response=""
async_mode = None

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
Session(app)
socketio = SocketIO(app,manage_session=False, async_mode=async_mode)

users_connected=0
#users_active=0

#path = "transcripts"
#path_fail = "Fail\\"

#CLIENT_ACCESS_TOKEN = '9624c80a372f44aeaf364eab4cc182b0'
#CLIENT_ACCESS_TOKEN = '0f46492cb7f34e1ebe5cbc31c8dbc486'
#CLIENT_ACCESS_TOKEN = 'cf8192cbf36b4dc98dc28a0eec09b42e' ## Rakin's Environment
CLIENT_ACCESS_TOKEN = '9598402294574e088f839d6f71236783' ## ERA Admin Environment


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def stat():
    global users_connected
    print("Number of User Connected to our Server:",users_connected)
    print("Number of User Actively Chatting:", len(stack))


@app.route('/')
def chat():
  return render_template('login.html')

# @app.route("/get_my_ip", methods=["GET"])
# def get_my_ip():
#     return jsonify({'ip': request.remote_addr}), 200


@app.route('/chatting')
def login():
  return render_template('chat.html')


@socketio.on('stats',namespace='/chat')
def show_stats():
    #print("Requesting the Stats of the server....")
    #print("Number of User Connected to our Server:", users_connected)
    #print("Number of User Actively Chatting:", len(stack))
    emit('server_stats',{'User_Connected': users_connected, 'User_Active': len(stack)},broadcast=False)



@socketio.on('message', namespace='/chat')
def chat_message(message):
  print("message =!! ", message)
  test_message=message

  emit('message', {'data': test_message['data']}, broadcast=False)


@socketio.on('my_conn', namespace='/chat')
def chat_message(data):
    #print("message =!! ", message)
    #emit('message', {'data': test_message['data']}, broadcast=False)
    username= data['data']['username']
    mobile_number=data['data']['mobile_number']
    session= data['data']['session']
    date= data['data']['full']
    time= data['data']['time']
    print(" A user named " +username+" with mobile number "+str(mobile_number)+" and session id "+str(session)+" has connceted to the server at "+date+" "+time )

@socketio.on('discon', namespace='/chat')
def chat_message():
    global users_connected
    print('A user disconnected for reloading...')
    # emit('disconnect',broadcast=False)
    users_connected = users_connected - 1
    # users_active=users_active-1
    if stack:
        stack.pop()
    stat()



@socketio.on('auth', namespace='/chat')
def chat_message(data):

    username=data['data']
    #print("username ---",username)
    print("Authentication blcok in the server")
    username='rakin'
    password='admin'
    emit('auth',{'username':username,'password':password},broadcast=False)


@socketio.on('admin_train', namespace='/chat')
def chat_message(data):
    intent_name=data['data']['intent']
    training_arr=data['data']['training']
    response_arr = data['data']['response']

    print('Intent Name:- ',intent_name)
    print('Training Array:- ', training_arr)
    print('Response Array:- ', response_arr)
    #emit('auth', {'username': username, 'password': password}, broadcast=False)

    agent = Agent(  ###MAYA--LIVE
        '',
        '9624c80a372f44aeaf364eab4cc182b0',
        'a14a3b4e00b845b3b94639c11160c47b',
    )

    training_json = []

    for i in training_arr:
        training_json.append({"data": [{"text": i}]})



    res = agent.intents.create(intent_name, contexts=None,
                               userSays=training_json, responses=[
            {

                "messages": [
                    {
                        "speech": response_arr,
                        "type": 0
                    }
                ],
            }
        ])

    code = res['status']['code']
    error_type = res['status']['errorType']
    # error_detail=res['status']['errorDetails']
    #
    # print("error_code",code)
    # print("error_type",error_type)
    # print("error_detail",error_detail)

    if code == 200:
        print("Intent Created Successfully!! Now Your BOT has been trained with your training phrases!")
        message="Intent Created Successfully!! Now Your BOT has been trained with your training phrases!"
        path = "Admin_Training"
        path_check = Path('Admin_Training')

        if path_check.exists() == False:
            path_check.mkdir(parents=True, exist_ok=True)

        file_name = intent_name + ".txt"

        fo = open(path + "/" + file_name, "ab+")

        fo.write(str.encode("## Date: ") + str.encode(str(date.today())))
        fo.write(str.encode("\n## Time: ") + str.encode(str(datetime.now().time())))

        fo.write(str.encode("\n\n==============================="))
        fo.write(str.encode("\nIntent Name:--  ") + str.encode(str(intent_name)))
        fo.write(str.encode("\n==============================="))

        fo.write(str.encode("\n\n\n# Training Phrases # "))
        fo.write(str.encode("\n===============================\n\n\n"))
        for i, j in zip(training_arr, range(0, len(training_arr))):
            i = str(i)
            fo.write(str.encode(str(j + 1)) + str.encode(".  ") + str.encode(i) + str.encode("\n\n"))

        fo.write(str.encode("\n\n# BOT Responses # "))
        fo.write(str.encode("\n===============================\n\n\n"))

        for i, j in zip(response_arr, range(0, len(response_arr))):
            i = str(i)
            fo.write(str.encode(str(j + 1)) + str.encode(".  ") + str.encode(i) + str.encode("\n\n"))
    else:
        message = "Opps! Intent can't be created! \nError Code: " + str(code) + ".\nError Type: " + error_type + \
                  ".\nError Details: " + res['status']['errorDetails'] + ""
        print(message)

    fo.close()

    emit('admin_train', {'message':message }, broadcast=False)


@socketio.on('transcript', namespace='/chat')
def chat_message(data):

    username=data['data']['username']
    username=str(username).strip()
    mobile_no=data['data']['mobile_number']
    mobile_no=str(mobile_no).strip()
    session= data['data']['session']
    session=str(session).strip()
    dir_name=data['data']['full']
    dir_name=str(dir_name).strip()
    print("username ---",username.encode('utf-8'))
    print("mobile_no ---",mobile_no.encode('utf-8'))
    print("session ----",session)
    print("Dir_name ---", dir_name)


    #path="D:\Independent Frame\Realtime_New\\transcripts"
    #path = "F:\MAYA ChatBOT --- TEST\\transcripts"
    file_name=str(dir_name)+".txt"


    file_or_directory=Path("transcripts/"+mobile_no+"/"+username)

    if file_or_directory.exists():
        print(str(mobile_no.encode('utf-8'))+"/"+str(username.encode('utf-8')) + "  directory  exits---")
    else:
        print(str(mobile_no.encode('utf-8'))+"/"+str(username.encode('utf-8')) + "  --directory does not exit. --So Create it")
        file_or_directory.mkdir(parents=True, exist_ok=True)



    fo = open("transcripts/"+mobile_no+"/"+username+"/"+file_name, "ab+")

    #file_status=os.stat(file_name).st_size
    #print(file_status)

    my_file = Path("transcripts/"+mobile_no+"/"+username+"/"+ file_name)
    print("File exists:---", my_file.is_file())


    if my_file.is_file():
            fo.write(str.encode("\n\n || Session_ID:- "+str(session)+" ||\n\n"))
            stat()



    #fo.write("Python is a great language.\nYeah its great!!\n")


    fo.close()


@socketio.on('transcript_user', namespace='/chat')
def chat_message(data):
    username = data['data']['author']
    username=str(username).strip()
    mobile_no = data['data']['mobile_no']
    mobile_no=str(mobile_no).strip()
    session = data['data']['Session']
    session=str(session).strip()
    stack.add(session)
    dir_name=data['data']['full']
    dir_name=str(dir_name).strip()
    time=data['data']['time']
    time=str(time).strip()
    query=data['data']['message']
    query=str(query).strip()
    print("username ---", username.encode('utf-8'))
    print("mobile_no --", mobile_no.encode('utf-8'))
    print("session ----", session)
    print("Dir Name-", dir_name)
    print("Time", time)
    print("query----", query.encode('utf-8'))

    #path = "D:\Independent Frame\Realtime_New\\transcripts"
    #path = "F:\MAYA ChatBOT --- TEST\\transcripts"
    file_name = str(dir_name) + ".txt"

    file_or_directory = Path("transcripts/" + mobile_no + "/" + username)

    if file_or_directory.exists():
        print(str(mobile_no.encode('utf-8')) + "/" + str(username.encode('utf-8')) + "  directory  exits--")
    else:
        print(str(mobile_no.encode('utf-8')) + "/" + str(username.encode('utf-8')) + "  --directory does not exit. --So Create it")
        file_or_directory.mkdir(parents=True, exist_ok=True)

    fo = open("transcripts/" + mobile_no + "/" + username + "/" + file_name, "ab+")

    # file_status=os.stat(file_name).st_size
    # print(file_status)

    my_file = Path("transcripts/" + mobile_no + "/" + username + "/" + file_name)
    print("File exists:---", my_file.is_file())

    if my_file.is_file():
        fo.write(str.encode("\n\n       ")+username.encode('utf-8')+str.encode("  ( ")+time.encode('utf-8')+str.encode(" ) :-- ") + query.encode('utf-8') + str.encode(" \n\n"))

    fo.close()
    stat()

@socketio.on('transcript_bot', namespace='/chat')
def chat_message(data):
    username = data['data']['author']
    username=str(username).strip()
    mobile_no = data['data']['mobile_no']
    mobile_no=str(mobile_no).strip()
    session = data['data']['Session']
    session=str(session).strip()
    dir_name=data['data']['full']
    dir_name=str(dir_name).strip()
    time=data['data']['time']
    time=str(time).strip()
    query=data['data']['message']
    query=str(query).strip()
    #username="MAYA"
    print("username ---", username.encode('utf-8'))
    print("mobile_no --", mobile_no.encode('utf-8'))
    print("session ----", session)
    print("Dir Name-", dir_name)
    print("Time", time)
    print("query", query.encode('utf-8'))

    #path = "D:\Independent Frame\Realtime_New\\transcripts"
    #path = "F:\MAYA ChatBOT --- TEST\\transcripts"
    file_name = str(dir_name) + ".txt"

    file_or_directory = Path("transcripts/" + mobile_no + "/" + username)

    if file_or_directory.exists():
        print(str(mobile_no.encode('utf-8')) + "/" + str(username.encode('utf-8')) + "  directory  exits--")
    else:
        print(str(mobile_no.encode('utf-8')) + "/" + str(username.encode('utf-8')) + "  --directory does not exit. --So Create it")
        file_or_directory.mkdir(parents=True, exist_ok=True)

    fo = open("transcripts/" + mobile_no + "/" + username + "/" + file_name, "ab+")

    # file_status=os.stat(file_name).st_size
    # print(file_status)

    my_file = Path("transcripts/" + mobile_no + "/" + username + "/" + file_name)
    print("File exists:----", my_file.is_file())

    username="AVA"
    if my_file.is_file():
        fo.write(str.encode("\n\n       ")+username.encode('utf-8')+str.encode("  ( ")+time.encode('utf-8')+str.encode(" ) :-- ") + query.encode('utf-8') + str.encode(" \n\n"))

    fo.close()
    stat()

@socketio.on('matching', namespace='/chat')
def chat_message(data):

    #test_data=data
    global path_fail
    flag=data['data']['flag']
    user_text=data['data']['message']
    user_text=user_text.strip()
    rad_arr=data['data']['arr']
    length=len(rad_arr)
    score=[]
    mismatch_flag=0
    match_flag=0
    match_intent=""
    #score= similar(user_text,rad_arr[0])


    for i in range(length):
        rad_arr[i]=rad_arr[i].strip()
        if rad_arr[i].upper() in user_text.upper():
            match_flag=1
            match_intent=rad_arr[i]
            #print("Matched intent:- ",match_intent)


    if match_flag==1:
        message=data
        query = match_intent
        # print("Username:-", message['data']['author'])
        print("\n************* Query-", query.encode('utf-8'), " ---- Username:- ",
              message['data']['author'].encode('utf-8'), " ----- Session ID:- ", message['data']['Session'],
              "  ********")

        #CLIENT_ACCESS_TOKEN='9624c80a372f44aeaf364eab4cc182b0'

        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

        request = ai.text_request()

        request.lang = 'en'  # optional, default value equal 'en'

        request.session_id = str(message['data']['Session'])
        # print("session_id:- "+str(message['data']['Session']))
        # print(query.encode('utf-8'))
        request.query = query
        response = request.getresponse()

        result = response.read().decode('utf-8')

        json_obj = json.loads(result)

        res = json_obj['result']['fulfillment']['speech']
        # print("response_code",res.encode('utf-8'))
        response = {'data': {'message': res, 'author': 'OCAS'}}
        response = json.dumps(response)
        response = json.loads(response)

        # print(response['data'])

        # print("response: = ",response)

        emit('response', {'data': response['data']}, broadcast=False)

        if "I am sorry" in res:
            print("Yes....................", "session: ", message['data']['Session'])
            today = str(date.today())
            print(str(date.today()))
            #global path_fail

            path = Path('Fail')

            if path.exists() == False:
                path.mkdir(parents=True, exist_ok=True)

            path_fail = "Fail/"+ today + ".txt"
            username = message['data']['author']
            time = message['data']['time']
            mobile_no = message['data']['mobile_no']

            fo = open(path_fail, "ab+")

            myfile = Path(path_fail)

            if myfile.is_file():
                fo.write(str.encode("\n\n       ") + username.encode('utf-8') + str.encode(" -- ") + mobile_no.encode(
                    'utf-8') + str.encode("  ( ") + time.encode('utf-8') + str.encode(" ) :-- ") + query.encode(
                    'utf-8') + str.encode(" \n\n"))
                username = "AVA"
                fo.write(str.encode("\n\n       ") + username.encode('utf-8') + str.encode("  ( ") + time.encode(
                    'utf-8') + str.encode(" ) :-- ") + res.encode('utf-8') + str.encode(" \n\n"))


            fo.close()

        else:
            print("No....................", "session: ", message['data']['Session'])



    else:


        #print("######## User Text ######## ",user_text)
        #print("######## Array for matching content ######## ", rad_arr)
        print("Array length:----- ", length)
        print("Matching Score:----", score)



        for i in rad_arr:
            #print("i== ", i)
            score.append(similar(user_text.upper(),i.upper()))
            print("Matching Score:---- ", score)


        for i in score:

            if(i >= 0.40):
                mismatch_flag=0
                break
            else:
                mismatch_flag=1

        print(" Maximum Score:---", max(score))

        max_index = score.index(max(score))

        print("Max Index== ", max_index)

        if(max(score)>0.80):
            mismatch_flag=1
            data['data']['message']=rad_arr[max_index]




        if mismatch_flag==0:


            if flag==0:
                res=" Did you mean " + rad_arr[max_index]+", "+data['data']['author']+ " ?"
            else:
                res = " আপনি কি " + rad_arr[max_index] + " বোঝাতে চেয়েছেন, " + data['data']['author'] + " ?"


            response={'data':{'message':res,'match':rad_arr[max_index]}}
            emit('response', {'data': response['data']}, broadcast=False)

        else:
            message=data
            query = message['data']['message']
            # print("Username:-", message['data']['author'])
            print("\n*************** Query-", query.encode('utf-8'), " ---- Username:- ",
                  message['data']['author'].encode('utf-8'), " ----- Session ID:- ", message['data']['Session'],
                  "  ********")
            # query="একটি অ্যাকাউন্ট খুলতে আমাকে কি করতে হবে"
            # print("query!=!",query.encode('utf-8'))


            #CLIENT_ACCESS_TOKEN = '9624c80a372f44aeaf364eab4cc182b0'

            ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

            request = ai.text_request()

            request.lang = 'en'  # optional, default value equal 'en'

            request.session_id = str(message['data']['Session'])
            # print("session_id:- "+str(message['data']['Session']))
            # print(query.encode('utf-8'))
            request.query = query
            response = request.getresponse()

            result = response.read().decode('utf-8')

            json_obj = json.loads(result)

            res = json_obj['result']['fulfillment']['speech']
            # print("response_code",res.encode('utf-8'))
            response = {'data': {'message': res, 'author': 'OCAS'}}
            response = json.dumps(response)
            response = json.loads(response)

            # print(response['data'])

            # print("response: = ",response)

            emit('response', {'data': response['data']}, broadcast=False)

            if "I am sorry" in res:
                print("Yes....................", "session: ", message['data']['Session'])
                today = str(date.today())
                print(str(date.today()))
                #global path_fail

                path=Path('Fail')

                if path.exists()==False:
                    path.mkdir(parents=True,exist_ok=True)


                path_fail = "Fail/"+ today + ".txt"
                username = message['data']['author']
                time = message['data']['time']
                mobile_no = message['data']['mobile_no']

                fo = open(path_fail, "ab+")

                myfile = Path(path_fail)

                if myfile.is_file():
                    fo.write(
                        str.encode("\n\n       ") + username.encode('utf-8') + str.encode(" -- ") + mobile_no.encode(
                            'utf-8') + str.encode("  ( ") + time.encode('utf-8') + str.encode(" ) :-- ") + query.encode(
                            'utf-8') + str.encode(" \n\n"))
                    username = "AVA"
                    fo.write(str.encode("\n\n       ") + username.encode('utf-8') + str.encode("  ( ") + time.encode(
                        'utf-8') + str.encode(" ) :-- ") + res.encode('utf-8') + str.encode(" \n\n"))


                fo.close()

            else:
                print("No....................", "session: ", message['data']['Session'])
            stat()



@socketio.on('response', namespace='/chat')
def chat_message(message):
      #print("message !!== ", message)
      #message="একটি অ্যাকাউন্ট খুলতে আমাকে কি করতে হবে"
      #test_message=message
      #test_message['data']['message']= "Server side"
      #reply= str(message['data']['message'])+ " sultan...."

      #Session(app)

      #emit('message', {'data': test_message['data']}, broadcast=True)

      global path_fail

      test_message=message

      query=message['data']['message']
      #print("Username:-", message['data']['author'])
      print("\n*************** Query-", query.encode('utf-8')," ---- Username:- ", message['data']['author'].encode('utf-8'), " ----- Session ID:- ", message['data']['Session'],"  ********")
      #query="একটি অ্যাকাউন্ট খুলতে আমাকে কি করতে হবে"
      #print("query!=!",query.encode('utf-8'))


      #CLIENT_ACCESS_TOKEN='9624c80a372f44aeaf364eab4cc182b0'

      ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

      request = ai.text_request()

      request.lang = 'en'  # optional, default value equal 'en'



      request.session_id =str(message['data']['Session'])
      #print("session_id:- "+str(message['data']['Session']))
      #print(query.encode('utf-8'))
      request.query = query
      response = request.getresponse()

      result=response.read().decode('utf-8')

      json_obj=json.loads(result)


      res= json_obj['result']['fulfillment']['speech']
      #print("response_code",res.encode('utf-8'))
      response={'data':{'message':res,'author':'OCAS'}}
      response=json.dumps(response)
      response=json.loads(response)

      #print(response['data'])

      print("query:-",query," response: = ",res,"session: ",message['data']['Session'])
      emit('response', {'data': response['data']}, broadcast=False)

      if "I am sorry" in res:
          print("Yes....................","session: ",message['data']['Session'])
          today=str(date.today())
          print(str(date.today()))

          path = Path('Fail')

          if path.exists() == False:
              path.mkdir(parents=True, exist_ok=True)

          path_fail = "Fail/"+today+".txt"
          username=message['data']['author']
          time=message['data']['time']
          mobile_no=message['data']['mobile_no']

          fo = open(path_fail, "ab+")

          myfile=Path(path_fail)

          if myfile.is_file():
              fo.write(str.encode("\n\n       ") + username.encode('utf-8')+str.encode(" -- ")+mobile_no.encode('utf-8') + str.encode("  ( ") + time.encode('utf-8') + str.encode(" ) :-- ") + query.encode('utf-8') + str.encode(" \n\n"))
              username="AVA"
              fo.write(str.encode("\n\n       ") + username.encode('utf-8') + str.encode("  ( ") + time.encode('utf-8') + str.encode(" ) :-- ") + res.encode('utf-8') + str.encode(" \n\n"))

          fo.close()
      else:
          print("No....................","session: ",message['data']['Session'])

      stat()

@socketio.on('connect', namespace='/chat')
def test_connect():
    global users_connected
    users_connected = users_connected + 1
    #emit('my response', {'data': 'Connected', 'count': 0})
    print("A user connected to the server with IP Address: ",request.remote_addr,".....")
    print(request.remote_addr)
    stat()

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    global users_connected
    print('A user disconnected from our server with IP Address: ',request.remote_addr,".....")
    #emit('disconnect',broadcast=False)
    users_connected= users_connected -1
    #users_active=users_active-1
    if stack:
        stack.pop()
    stat()



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5003, debug=True)
    # socketio.run(app,debug=True)