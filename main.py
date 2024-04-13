from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.utils import platform
import threading
import time
import requests
import stripe
import os
from jnius import autoclass
from dotenv import load_dotenv

stripe.api_key = os.getenv('STRIPE_API_KEY')

load_dotenv()

class POSApp(App):
    def __init__(self):
        super().__init__()
        self.nfc_enabled = False
        self.payment_icon = None
        self.countdown_running = False
        self.end_button_pressed = False
        self.card_data = None  # Initialize card data variable

    def build(self):
        main_layout = GridLayout(cols=1, rows=2, spacing=10, padding=(10, 10, 10, 10))

        top_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.amount_input = TextInput(hint_text='Amount must be at least €0.50 eur', input_type='number', multiline=False, size_hint=(0.8, None), height=40, font_size=16, background_color=(1, 1, 1, 1))
        top_layout.add_widget(self.amount_input)
        self.result_label = Label(text='', size_hint_x=None, width=750, font_size=16, color=(0.2, 0.6, 0.8, 1))
        top_layout.add_widget(self.result_label)
        
        bottom_layout = GridLayout(cols=4, rows=4, spacing=10)
        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'Del', '0', 'Enter',
            'End','.'
        ]

        for button_text in buttons:
            button = Button(text=button_text, on_press=self.on_button_press, font_size=16, background_normal='', background_color=(0.2, 0.6, 0.8, 1))
            bottom_layout.add_widget(button)

        main_layout.add_widget(top_layout)
        main_layout.add_widget(bottom_layout)

        if platform == 'android':
            self.init_nfc()

        return main_layout

    def init_nfc(self):
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        self.nfc_adapter = mActivity.getSystemService(mActivity.NFC_SERVICE)
        self.nfc_adapter.enableForegroundDispatch(mActivity)

    def on_button_press(self, instance):
        if instance.text == 'Enter':
            self.make_payment()
        elif instance.text == 'Del':
            current_text = self.amount_input.text
            self.amount_input.text = current_text[:-1]
        elif instance.text == 'End':
            self.end_button_pressed = True
            self.cancel_payment()
            self.stop_countdown()
        else:
            current_text = self.amount_input.text
            self.amount_input.text = current_text + instance.text

    def make_payment(self):
        amount = self.amount_input.text
        if not amount:
            self.result_label.text = 'Please enter the amount.'
            return
        
        amount_in_cents = self.convert_to_cents(amount)
        if amount_in_cents is None:
            return

        self.initiate_payment_with_tag_data()

    def convert_to_cents(self, amount):
        try:
            euros, cents = map(int, amount.split('.'))
            total_cents = euros * 100 + cents
            return total_cents
        except ValueError:
            self.result_label.text = 'Invalid amount format. Please enter the amount in euros from 0.50 (e.g., 0.50 for €0.50).'
            return None

    def initiate_payment_with_tag_data(self):
        if self.card_data:
            self.result_label.text = 'Processing payment...'
            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(float(self.amount_input.text) * 100),
                    currency='eur',
                    payment_method_types=['card'],
                    capture_method='automatic',
                    description=f"Payment for {self.card_data}"
                )
                self.handle_payment_intent(payment_intent)
                self.process_payment(payment_intent.id)
            except stripe.InvalidRequestError as e:
                self.result_label.text = f'Error: {e._message}'
            except stripe.StripeError as e:
                self.result_label.text = f'Error: {e._message}'
            except Exception as e:
                self.result_label.text = 'An error occurred. Please try again.'

    def handle_payment_intent(self, payment_intent):
        try:
            updated_payment_intent = stripe.PaymentIntent.confirm(
                payment_intent.id,
                payment_method=self.card_data.id)
            payment_method_options={'card': {'number': self.card_data}}
             

            if updated_payment_intent.status != 'requires_capture':
                self.result_label.text = 'Payment processing failed. Please try again.'
        except stripe.StripeError as e:
            self.result_label.text = f'Error: {e._message}'
        except Exception as e:
            self.result_label.text = 'An error occurred. Please try again.'

    def process_payment(self, payment_intent_id):
        amount = int(float(self.amount_input.text) * 100)
        payload = {
            'amount': amount / 100, 
            'payment_intent_id': payment_intent_id
        }

        def update_text(dt):
            self.result_label.text = f'€{amount/ 100} Successful! ORDER ID: {data["order_id"]}'
            self.amount_input.text = ''

        self.result_label.text = 'Payment is in progress. Please wait.'

        backend_url = 'http://localhost:5000/charge'  # Update backend URL
        response = requests.post(backend_url, json=payload)

        if response.status_code == 200:
            data = response.json()
            Clock.schedule_once(update_text, 0)
        else:
            Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', 'Payment failed. Please try again'), 0)

    def cancel_payment(self):
        self.amount_input.text = ''
        self.result_label.text = ''

    def stop_countdown(self):
        self.countdown_running = False

    @mainthread
    def on_new_nfc_data(self, card_data):
        self.card_data = card_data
        self.result_label.text = f'NFC Tag Data Received: {card_data}'

    def on_pause(self):
        if platform == 'android':
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            self.nfc_adapter.disableForegroundDispatch(mActivity)
        return True

    def on_resume(self):
        if platform == 'android':
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            self.nfc_adapter.enableForegroundDispatch(mActivity)

if __name__ == '__main__':
    POSApp().run()
