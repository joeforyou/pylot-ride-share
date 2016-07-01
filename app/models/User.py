
from system.core.model import Model

import re, md5

NAME_REGEX = re.compile(r'^[a-zA-Z0-9]{3,}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASS_REGEX = re.compile(r'^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{8,}$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def register_new_user(self, userData):
        hasErrors = False
        if not NAME_REGEX.match(userData['firstName']):
            hasErrors = True
        elif not NAME_REGEX.match(userData['lastName']):
            hasErrors = True
        elif not NAME_REGEX.match(userData['username']):
            hasErrors = True
        elif not userData['phoneNumber']:
            hasErrors = True
        elif not EMAIL_REGEX.match(userData['email']):
            hasErrors = True
        elif not PASS_REGEX.match(userData['password']):
            hasErrors = True
        elif userData['password'] != userData['confirmPassword']:
            hasErrors = True
        elif hasErrors == True:
            return False
        else:
            query = 'INSERT INTO user (first_name, last_name, username, email, phone_number, password, card) VALUES (:firstName, :lastName, :username, :email, :phoneNumber, :password, :creditCard)'
            hashed_pw =self.bcrypt.generate_password_hash(userData['password'])
            data = {
                'firstName': userData['firstName'],
                'lastName': userData['lastName'],
                'username': userData['username'],
                'email': userData['email'],
                'phoneNumber': userData['phoneNumber'],
                'creditCard': userData['stripeToken'],
                'password': hashed_pw
                }
            return self.db.query_db(query, data)

    def login_user(self, userData):
        hasErrors = False
        if len(userData['username']) < 3:
            hasErrors = True
        elif not NAME_REGEX.match(userData['username']):
            hasErrors = True
        elif hasErrors == False:
            password = userData['password']
            query = "SELECT * FROM user WHERE username = :username LIMIT 1"
            data = {'username': userData['username']}
            result = self.db.query_db(query, data)
            check = result[0]['password']
            if result:
                if self.bcrypt.check_password_hash(check, password):
                    return result
        else:
            return False

    def update_about_text(self, userData):
        query = 'UPDATE user SET user.about=:about WHERE user.id=:id'
        data = {'about': userData['about'], 'id': userData['id']}
        return self.db.query_db(query, data)

    def post_new_offer(self, userData):
        query = 'INSERT INTO offer (origin, destination, date, time, seats, price, about, user_id) VALUES (:origin, :destination, :date, :time, :seats, :price, :about, :id)'
        data = {
                'origin': userData['origin'], 
                'destination': userData['destination'], 
                'date': userData['date'], 
                'time': userData['time'], 
                'seats': userData['seats'], 
                'price': userData['price'], 
                'about': userData['about'], 
                'id': userData['id']
                }
        return self.db.query_db(query, data)

    def get_offers_by_id(self, id):
        query = 'SELECT * FROM offer WHERE user_id=:id'
        data = {'id': id}
        return self.db.query_db(query, data)

    def find_offers(self, userData):
        query = 'SELECT * FROM offer WHERE origin = :origin OR destination = :destination'
        data = {'origin': userData['origin'], 'destination': userData['destination']}
        return self.db.query_db(query, data)

    def get_interested(self, userData):
        query = "SELECT * FROM confirm_ride JOIN offer ON confirm_ride.offer_id = offer.id WHERE confirm_ride.user_id = :id "
        data = { 'id': userData['id'] }
        return self.db.query_db(query, data)

    def interest_ride(self, userData, offer_id):
        query = "INSERT INTO confirm_ride (user_id, offer_id) VALUES (:user, :offer)"
        data = {
                'user': userData['id']
                'offer': offer_id
               }
        self.db_query(query,data)

    def delete_request(self, userData, request_id):
        query="DELETE FROM confirm_ride WHERE confirm_ride.user_id = :user AND confirm_ride.request_id = :request"
        data = { 

                'user':userData['id']
                'request': request_id

               }
        self.db_query(query,data)
    def delete_offer(self, userData, offer_id):
        query="DELETE FROM offer_id WHERE offer.user_id= :user AND offer.id= :offer"
        data={

                'user':userData['id']
                'offer':offer_id

            }
        self.db_query(query,data)
        