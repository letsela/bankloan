# save this as app.py
from flask import Flask, escape, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("prediction.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        self_employed = request.form['self_employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        if (gender == "Male"):
            gender=1
        else:
            gender=0
        
        # married
        if(married=="Yes"):
            married = 1
        else:
            married=0

        # dependents
        if(dependents=='1'):
            dependents=1
        elif(dependents == '2'):
            dependents=2
        elif(dependents=='4'):
            dependents=4
        else:
            dependents=0

        # education
        if (education=="Not Graduate"):
            education=0
        else:
            education=1

        # self_employed
        if (self_employed == "Yes"):
            self_employed=1
        else:
            self_employed=0

        # property area

        if(area=="Semiurban"):
           area=1
        elif(area=="Urban"):
          area=2
        else:
          area=0


        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Term_Log = np.log(Loan_Amount_Term)

        prediction = model.predict([[gender, married, dependents, education, self_employed, credit, area, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Term_Log, totalincomelog]])


        # print(prediction)

        if(prediction== 0):
            prediction="No"
        else:
            prediction="Yes"


        return render_template("prediction.html", prediction_text="loan status is {}".format(prediction))




    else:
        return render_template("prediction.html")



if __name__ == "__main__":
    app.run(debug=True)