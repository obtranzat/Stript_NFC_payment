This repository contains a simple Point of Sale (POS) system developed using the Kivy framework. It enables users to enter an amount and process payments using Stripe. The app also integrates NFC (Near Field Communication) support on Android devices to facilitate card payments through NFC tags.

Features
User-Friendly Interface: A grid layout is used for easy input of amounts and triggering actions like payment processing, deletion, and ending a transaction.
NFC Support (Android): Detects NFC tags for contactless payment methods.
Payment Processing: Processes payments securely using the Stripe API.
Cancel/End Transaction: Easily cancel or end a transaction.
Real-Time Feedback: Provides real-time feedback on payment status.
Prerequisites
Python 3.6+
Kivy Framework
Stripe Python Library
Requests Library
Jnius (for Android NFC integration)
dotenv (for environment variable management)
Setup
Clone the repository:

git clone https://github.com/obtranzat/stripe_NFC_payment.git
cd stripe_NFC_payment
Install the required dependencies:
pip install kivy stripe requests python-dotenv jnius
Set up your Stripe API Key:

Create a .env file in the root of the project.
Add your Stripe secret key to the .env file:
makefile

STRIPE_API_KEY=your_stripe_api_key
Ensure that the backend server for handling payments (e.g., Flask or similar) is running and accessible at the URL specified in the code (currently http://localhost:5000/charge).

Running the Application
To start the application, run the following command:


python main.py
If you're running this on an Android device, ensure NFC is enabled.

Usage
Enter Amount: Input the payment amount using the on-screen buttons. Amounts must be at least €0.50.
Process Payment: Press the Enter button to initiate the payment process using Stripe. If you're on an Android device with NFC support, tap a card to process the payment.
Cancel Transaction: Press the End button to cancel the current transaction.
Stripe Integration
The app uses Stripe's Python API to handle payment processing. Here's how the payment flow works:

The user enters an amount.
The app converts the amount to cents and sends the payment request to Stripe.
If NFC data is available, it associates the card data with the payment request.
The backend server (which must be set up separately) completes the payment processing.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contribution
Feel free to submit pull requests or open issues for bug fixes or new feature suggestions.

By using this repository, you agree to the terms of service outlined by Stripe, and to comply with all applicable laws regarding payment processing.
