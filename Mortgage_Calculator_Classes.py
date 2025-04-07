class Applicant:
    def __init__(self, first_name, last_name, credit_score, income):
        self.first_name = first_name
        self.last_name = last_name
        self.credit_score =  credit_score
        self.income = income

class Well_Qualified(Applicant):
    def __init__(self, first_name, last_name, credit_score, income, application_id):
        super().__init__(first_name, last_name, credit_score, income)
        self.application_id = application_id

    interest_rate = 0.06
    down_payment = .1

class Adequately_Qualified(Applicant):
    def __init__(self, first_name, last_name, credit_score, income, application_id):
        super().__init__(first_name, last_name, credit_score, income)
        self.application_id = application_id

    interest_rate = 0.07
    down_payment = .15

class Minimally_Qualified(Applicant):
    def __init__(self, first_name, last_name, credit_score, income, application_id):
        super().__init__(first_name, last_name, credit_score, income)
        self.application_id = application_id

    interest_rate = 0.08
    down_payment = .2

class Mortgage_Calculator():
    def __init__(self):
        pass
        
        

