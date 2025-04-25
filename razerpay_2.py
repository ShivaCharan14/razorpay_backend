import random
import sqlite3
from datetime import datetime

class PaymentGateway:
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self._setup_database()

        # Payment options
        self.options = {
            '1': {'name': 'Mobile Recharge', 'type': 'plan'},
            '2': {'name': 'Movie Ticket', 'type': 'movie'},
            '3': {'name': 'UPI Transfer', 'type': 'transfer'}
        }

    def _setup_database(self):
        """Create a simple database table for payments"""
        self.db.execute('''
        CREATE TABLE payments (
            id TEXT PRIMARY KEY,
            amount REAL,
            status TEXT,
            category TEXT,
            details TEXT,
            time TEXT
        )''')

    def create_payment(self, amount, category, details):
        """Create a new payment record"""
        payment_id = f"pay_{random.randint(1000,9999)}"
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.db.execute(
            "INSERT INTO payments VALUES (?,?,?,?,?,?)",
            (payment_id, amount, 'created', category, str(details), time)
        )
        return payment_id

    def process_payment(self, payment_id):
        """Process the payment (70% success rate)"""
        result = random.choices(['success', 'failed'], weights=[70, 30])[0]
        self.db.execute(
            "UPDATE payments SET status=? WHERE id=?",
            (result, payment_id))
        return result

    def get_payment(self, payment_id):
        """Get payment details"""
        data = self.db.execute(
            "SELECT * FROM payments WHERE id=?", (payment_id,)).fetchone()
        if data:
            return {
                'id': data[0],
                'amount': data[1],
                'status': data[2],
                'category': data[3],
                'details': eval(data[4]),
                'time': data[5]
            }
        return None

class PaymentApp:
    def __init__(self):
        self.gateway = PaymentGateway()

    def run(self):
        while True:
            print("\nPAYMENT APP")
            print("1. New Payment")
            print("2. Check Status")
            print("3. Exit")
            
            choice = input("Choose option: ")
            
            if choice == '1':
                self.new_payment()
            elif choice == '2':
                self.check_status()
            elif choice == '3':
                print("Thank you for using our service!")
                break
            else:
                print("Invalid choice")

    def new_payment(self):
        print("\nPAYMENT OPTIONS:")
        for num, opt in self.gateway.options.items():
            print(f"{num}. {opt['name']}")
            
        choice = input("Select payment type: ")
        
        if choice == '1':
            self.mobile_payment()
        elif choice == '2':
            self.movie_payment()
        elif choice == '3':
            self.upi_payment()
        else:
            print("Invalid choice")

    def mobile_payment(self):
        print("\nMOBILE RECHARGE")
        amount = float(input("Enter amount: ₹"))
        number = input("Enter mobile number: ")
        operator = input("Enter operator: ")
        
        details = {
            'number': number,
            'operator': operator,
            'type': 'prepaid'
        }
        
        pid = self.gateway.create_payment(amount, 'Mobile', details)
        print(f"\nPayment created! ID: {pid}")
        self.process_now(pid)

    def movie_payment(self):
        print("\nMOVIE TICKET")
        movie = input("Enter movie name: ")
        theater = input("Enter theater: ")
        amount = float(input("Enter ticket price: ₹"))
        
        details = {
            'movie': movie,
            'theater': theater,
            'seats': 'A1,A2'  # Simplified
        }
        
        pid = self.gateway.create_payment(amount, 'Movie', details)
        print(f"\nBooking created! ID: {pid}")
        self.process_now(pid)

    def upi_payment(self):
        print("\nUPI TRANSFER")
        upi_id = input("Enter UPI ID: ")
        amount = float(input("Enter amount: ₹"))
        note = input("Enter note (optional): ")
        
        details = {
            'upi_id': upi_id,
            'note': note
        }
        
        pid = self.gateway.create_payment(amount, 'UPI', details)
        print(f"\nTransfer initiated! ID: {pid}")
        self.process_now(pid)

    def process_now(self, pid):
        """Ask if user wants to process payment now"""
        choice = input("Process payment now? (y/n): ").lower()
        if choice == 'y':
            result = self.gateway.process_payment(pid)
            print(f"Payment {result}!")
            self.show_receipt(pid)

    def show_receipt(self, pid):
        """Show payment receipt"""
        payment = self.gateway.get_payment(pid)
        if payment:
            print("\nRECEIPT")
            print(f"ID: {payment['id']}")
            print(f"Amount: ₹{payment['amount']}")
            print(f"Status: {payment['status']}")
            print(f"Time: {payment['time']}")
            print("\nDetails:")
            for key, value in payment['details'].items():
                print(f"{key}: {value}")

    def check_status(self):
        pid = input("Enter payment ID: ")
        payment = self.gateway.get_payment(pid)
        
        if payment:
            self.show_receipt(pid)
        else:
            print("Payment not found")

# Start the app
if __name__ == "__main__":
    app = PaymentApp()
    app.run()
