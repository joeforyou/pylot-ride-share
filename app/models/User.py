
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
        query = 'INSERT INTO offer (origin, destination, date, departure_time, seats, price, about, user_id, arrival_time, seats_available) VALUES (:origin, :destination, :date, :departure_time, :seats, :price, :about, :id, :arrival_time, :seats_available)'
        data = {
                'origin': userData['origin'], 
                'destination': userData['destination'], 
                'date': userData['date'], 
                'departure_time': userData['departure_time'], 
                'seats': userData['seats'], 
                'price': userData['price'], 
                'about': userData['about'], 
                'id': userData['id'],
                'arrival_time': userData['arrival_time'],
                'seats_available': userData['seats']
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
                'user': userData['id'],
                'offer': offer_id
               }
        self.db.query_db(query, data)
        query = "UPDATE offer SET seats_available = seats_available - 1 WHERE offer.id = :offer"
        self.db.query_db(query, data)


    def delete_request(self, userData, confirm_id):
        query="DELETE FROM confirm_ride WHERE confirm_ride.user_id = :user AND confirm_ride.offer_id = :confirm"
        data = { 
                'user':userData['id'],
                'confirm': confirm_id
               }
        self.db.query_db(query, data)

    def delete_offer(self, userData, offer_id):
        query="DELETE FROM offer WHERE offer.id = :offer"
        data={
              'user' :userData['id'],
              'offer' :offer_id
            }
        self.db.query_db(query, data)

    def get_join(self, userData):
        query="SELECT * FROM (SELECT * FROM offer WHERE offer.user_id=:id) AS all_rides JOIN confirm_ride confirms ON all_rides.id=confirms.offer_id JOIN user ON user.id=confirms.user_id"
        data={'id': userData['id']}
        self.db.query_db(query, data)