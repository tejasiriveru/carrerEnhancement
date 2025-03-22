import razorpay
from django.conf import settings

class RazorpayClient(object):
    #Generic Razorpay client class
    def __init__(self):
        #keys from razorpay
        try:
            # authorize razorpay client with API Keys.
            self.client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        except:
            print("Authentication Error")
    
    def create_order(self, amount, currency="INR"):
        
        try:
            razorpay_order = self.client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
            return razorpay_order
        except:
            print("Order error")
