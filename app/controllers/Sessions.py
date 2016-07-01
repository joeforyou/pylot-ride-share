from system.core.controller import *

class Sessions(Controller):
    def __init__(self, action):
        super(Sessions, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('index.html')

    def signup(self):
        return self.load_view('registration.html')

    def register(self):
        self.load_model('User')
        userArray = self.models['User'].register_new_user(request.form)
        if userArray:
            flash('Successful registration! Please log in to continue.')
            return self.load_view('index.html')

        else:
            flash('Failed to register. Name must be at least three characters. Password must be eight characters or more with at least one number and one letter.')
            return redirect ('/signup')

    def login(self):
        self.load_model('User')
        userArray = self.models['User'].login_user(request.form)
        if userArray:
            session['currentUser'] = userArray[0]
            return redirect('/main')
        else:
            flash('Failed to login. Invalid username and/or password.')
            return redirect ('/')

    def logout(self):
        session.pop('currentUser', None)
        return redirect('/')
