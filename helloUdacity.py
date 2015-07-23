import webapp2
import cgi

form = """
<form method ="post">
	What is your birthday??
  <br>

  <label> Month
    <input type="text" name="month" value="%(month)s">
  </label>  
  <label> Day  
    <input type="text" name="day" value="%(day)s">
	</label>
  <label> Year 
    <input type="text" name="year" value="%(year)s">
  </label>

  <div style="color: red">%(error)s </div>
  <br>
  <br>
  <input type="submit">
</form>
"""


class MainPage(webapp2.RequestHandler):

    months = ['January', #python list called a Dictionary
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

    months_abbvs = dict( (m[:3].lower(), m) for m in months)

    def write_form(self, error="", month="", day="", year=""):
      self.response.out.write(form % {"error": error,
                                      "month": self.escape_html(month),
                                      "day": self.escape_html(day),
                                      "year": self.escape_html(year)})

    def escape_html(self,s):
      return cgi.escape(s, quote = True)  

    def valid_month(self, month):
      if month:  #if user input exists, if non empty string
        short_month = month[:3].lower()
        return self.months_abbvs.get(short_month)

    def valid_day(self, day):
      if day and day.isdigit():
        num = int(day)
        if (num <32 and num>0):
            return day

    def valid_year(self, year):
      if year and year.isdigit():
        year = int(year)
        if year >1900 and year <2020:
          return year        

    def get(self):
        self.write_form()
        #by default he response type is HTML, so its not specified. 

    def post(self):
      user_month = self.request.get('month')
      user_day = self.request.get('day')
      user_year = self.request.get('year')

      month = self.valid_month(user_month)
      day = self.valid_day(user_day)
      year = self.valid_year(user_year)

      if not(month and day and year):
        self.write_form("That doesn't look valid to me buddy",
                        user_month,
                        user_day,
                        user_year)
      else:
        #redirect from this current handler to another url
        #and this /thanks url is already mapped to another handler
        #:-)
        self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler): 
  def get(self):
    self.response.out.write("Thanks, thats a totally valid date!")       
   
                

app = webapp2.WSGIApplication([('/', MainPage),
                                ('/thanks',ThanksHandler)], debug=True)







