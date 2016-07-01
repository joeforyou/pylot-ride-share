from system.core.controller import *

class Rides(Controller):
    def __init__(self, action):
        super(Rides, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db
   
    def index(self):
        self.load_model('User')
        offerArray = self.models['User'].get_offers_by_id(session['currentUser']['id'])
        request = self.models['User'].get_interested(session['currentUser'])
        return self.load_view('profile.html', offerArray=offerArray, request=request)

    def offer(self):
        return self.load_view('offerRide.html')

    def update(self):
        self.load_model('User')
        self.models['User'].update_about_text(request.form)
        return redirect ('/main')

    def postoffer(self):
        self.load_model('User')
        self.models['User'].post_new_offer(request.form)
        return redirect ('/main')

    def need(self):
        return self.load_view('needRide.html')

    def search(self):
        self.load_model('User')
        resultArray = self.models['User'].find_offers(request.form)
        return self.load_view('needRide.html', resultArray=resultArray)

    def interest_ride(self):
        self.load_model('User')
        self.models['User'].interest_ride(session['currentUser'], request.form['offer_id'])
        return redirect('/main')

    def delete_request(self)
        self.load_model('User')
        self.models['User'].delete_request(session['currentUser'], request.form['request_id'])
        return redirect('/main')

