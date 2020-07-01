import joblib
from flask import Flask,render_template,request,redirect,url_for
import pandas as pd

app=Flask(__name__)
model=joblib.load(r'C:\Users\Harsha\Desktop\IPL\linear_model.pkl')

output=0
d={'OUTsurance Oval': 0,
 'De Beers Diamond Oval': 1,
 'Vidarbha Cricket Association Stadium, Jamtha': 2,
 'Buffalo Park': 3,
 'Green Park': 4,
 'Nehru Stadium': 5,
 'Holkar Cricket Stadium': 6,
 'Newlands': 7,
 'Shaheed Veer Narayan Singh International Stadium': 8,
 'Sharjah Cricket Stadium': 9,
 'Sheikh Zayed Stadium': 10,
 'JSCA International Stadium Complex': 11,
 'Barabati Stadium': 12,
 'Dubai International Cricket Stadium': 13,
 "St George's Park": 14,
 'New Wanderers Stadium': 15,
 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium': 16,
 'Himachal Pradesh Cricket Association Stadium': 17,
 'Saurashtra Cricket Association Stadium': 18,
 'Punjab Cricket Association IS Bindra Stadium, Mohali': 19,
 'SuperSport Park': 20,
 'Brabourne Stadium': 21,
 'Sardar Patel Stadium, Motera': 22,
 'Kingsmead': 23,
 'Maharashtra Cricket Association Stadium': 24,
 'Subrata Roy Sahara Stadium': 25,
 'Dr DY Patil Sports Academy': 26,
 'Sawai Mansingh Stadium': 27,
 'Punjab Cricket Association Stadium, Mohali': 28,
 'Rajiv Gandhi International Stadium, Uppal': 29,
 'MA Chidambaram Stadium, Chepauk': 30,
 'Wankhede Stadium': 31,
 'Eden Gardens': 32,
 'Feroz Shah Kotla': 33,
 'M Chinnaswamy Stadium': 34}

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        details=request.form
        bat=details['bat']
        bowl=details['bowl']
        runs=int(details['runs'])
        wickets=int(details['wickets'])
        overs=float(details['overs'])
        runs_in_last=int(details['rl5'])
        wickets_in_last=int(details['wl5'])
        venue=details['venue']
            # final=[]
            # values = [i for i in request.form.values()]
            # values[-1]=d[values[-1]]
            # final.append(values[-1])
            # values+=values[2:7])
        venue_num=d[venue]
        values=[]
        values+=[venue_num,runs,wickets,overs,runs_in_last,wickets_in_last]

        if bat == 'Chennai Super Kings':
            values+=[1,0,0,0,0,0,0,0]
        elif bat == 'Delhi Daredevils':
            values+=[0,1,0,0,0,0,0,0]
        elif bat == 'Kings XI Punjab':
            values+=[0,0,1,0,0,0,0,0]
        elif bat == 'Kolkata Knight Riders':
            values+=[0,0,0,1,0,0,0,0]
        elif bat == 'Mumbai Indians':
            values+=[0,0,0,0,1,0,0,0]
        elif bat == 'Rajasthan Royals':
            values+=[0,0,0,0,0,1,0,0]
        elif bat == 'Royal Challengers Bangalore':
            values+=[0,0,0,0,0,0,1,0]
        elif bat == 'Sunrisers Hyderabad':
            values+=[0,0,0,0,0,0,0,1]
        
        if bowl == 'Chennai Super Kings':
            values+=[1,0,0,0,0,0,0,0]
        elif bowl == 'Delhi Daredevils':
            values+=[0,1,0,0,0,0,0,0]
        elif bowl == 'Kings XI Punjab':
            values+=[0,0,1,0,0,0,0,0]
        elif bowl == 'Kolkata Knight Riders':
            values+=[0,0,0,1,0,0,0,0]
        elif bowl == 'Mumbai Indians':
            values+=[0,0,0,0,1,0,0,0]
        elif bowl == 'Rajasthan Royals':
            values+=[0,0,0,0,0,1,0,0]
        elif bowl == 'Royal Challengers Bangalore':
            values+=[0,0,0,0,0,0,1,0]
        elif bowl == 'Sunrisers Hyderabad':
            values+=[0,0,0,0,0,0,0,1]   

        
        features= pd.DataFrame(values).T
        features.columns =['venue', 'runs', 'wickets', 'overs', 'runs_last_5', 'wickets_last_5',
        'bat_team_Chennai Super Kings', 'bat_team_Delhi Daredevils',
        'bat_team_Kings XI Punjab', 'bat_team_Kolkata Knight Riders',
        'bat_team_Mumbai Indians', 'bat_team_Rajasthan Royals',
        'bat_team_Royal Challengers Bangalore', 'bat_team_Sunrisers Hyderabad',
        'bowl_team_Chennai Super Kings', 'bowl_team_Delhi Daredevils',
        'bowl_team_Kings XI Punjab', 'bowl_team_Kolkata Knight Riders',
        'bowl_team_Mumbai Indians', 'bowl_team_Rajasthan Royals',
        'bowl_team_Royal Challengers Bangalore',
        'bowl_team_Sunrisers Hyderabad']

        # print('df',features)
        prediction=model.predict(features)
        global output
        output=round(prediction[0])
        return redirect(url_for('predicted'))

    return render_template('index.html')

@app.route('/output')
def predicted():
    output1=output-7
    output2=output+8
    return render_template('output.html',out1=output1,out2=output2)    

if __name__ =='__main__':
    app.run(debug=True)    