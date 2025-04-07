#Potential Calculations

pp = price_of_property = int(input()) #price of desired property

i = interest_rate = float(input()) #dependent on qualification level

dp = down_payment = int(input()) #dependdent on qualification level

pt = property_tax = float(input()) #dependent on location

n = loan_term = int(input()) #desired loan term

p = mortgage_principal = (price_of_property - down_payment)

m = monthly_mortgage = p( (i(1+i)**n) / ((1+i)**(n-1)) )


