import os
import re
from file_handler import InventoryFileHandler, color_deco, COLORS

#A program that helps manage a computer store's stock of CPUs and GPUs. Let's do functions (1-6)

# Main class for the PC Store Inventory System
class PCStore:
    def __init__(self, inventory_file="inventory.txt"):
        # Initialize with inventory file handler
        self.file_handler = InventoryFileHandler(inventory_file)
        self.inventory = self.file_handler.inventory

    @staticmethod
    def validate_cpu(cpu: str):
        # Validattion rules CPU name format (Ryzen or Core)
        ryzen_pattern = r"^Ryzen \d{4}X$"
        intel_pattern = r"^Core i[3579]-\d{4,5}([kfst])?$"  # Accepts 4 or 5 digits, [kfst] optional
        return re.match(ryzen_pattern, cpu) or re.match(intel_pattern, cpu)

    @staticmethod
    def validate_gpu(gpu: str):                 
        # Same Validation for GPU name format (Nvidia or AMD)
        nvidia_pattern = r"^(RTX|GTX) \d{4}$"
        amd_pattern = r"^RX \d{4} XT$"
        return re.match(nvidia_pattern, gpu) or re.match(amd_pattern, gpu)

    def display_cpus(self):                   #1
        # Return list of CPUs in inventory
        return [cpu for cpu in self.inventory if cpu.startswith("Ryzen") or cpu.startswith("Core")]

    def display_gpus(self):                   #2
        # Return list of GPUs in inventory
        return [gpu for gpu in self.inventory if gpu.startswith("RTX") or gpu.startswith("RX")]

    def add_component(self, component_type: str):       #3
        # Add a new CPU or GPU component with user input for name and amount
        if component_type.lower() == "cpu":
            while True:
                cpu = input("Enter CPU name (Ryzen XXXX or Core iX-XXXX): ")
                # Convert trailing letters to lowercase
                cpu = re.sub(r"([A-Za-z]+)$", lambda m: m.group(1).lower(), cpu)
                if self.validate_cpu(cpu):
                    amount = input("Enter amount to add: ")
                    try:
                        amount = int(amount)
                        return cpu, amount
                    except ValueError:
                        print("Amount must be an integer.")
                else:
                    print("Invalid CPU format. Examples: 'Ryzen 5600X', 'Core i5-12400K'")
        elif component_type.lower() == "gpu":
            while True:
                gpu = input("Enter GPU name (RTX/GTX XXXX or RX XXXX XT): ")
                # Convert trailing letters to lowercase
                gpu = re.sub(r"([A-Za-z]+)$", lambda m: m.group(1).lower(), gpu)
                if self.validate_gpu(gpu):
                    amount = input("Enter amount to add: ")
                    try:
                        amount = int(amount)
                        return gpu, amount
                    except ValueError:
                        print("Amount must be an integer.")
                else:
                    print("Invalid GPU format. Examples: 'RTX 3060', 'RX 6800 XT'")

    def sell_component(self, component: str):             #4
        # Sell one or more units of a component if available
        if component in self.inventory:
            while True:
                try:
                    amount = int(input(f"How many units of {component} do you want to sell? "))
                    if amount <= 0:
                        print("Amount must be positive.")
                        continue
                    if self.inventory[component] >= amount:
                        self.inventory[component] -= amount
                        return f"Sold {amount} {component}"
                    else:
                        return f"Not enough stock for {component}. Available: {self.inventory[component]}"
                except ValueError:
                    print("Amount must be an integer.")
        else:
            print(f"{component} not found in inventory. Available components:")
            for item in self.inventory:
                print(f"- {item} (Stock: {self.inventory[item]})")
            return "Component not found. Please check the list above."

    @color_deco("yellow")            #color coding for unkown component
    def check_quantity(self, component: str):
        # Return the quantity of a component, colored output
        return self.inventory.get(component, "Component not found")

    def save_inventory(self):
        # Save inventory back to file
        self.file_handler.save()

    def run(self):           #The actual loop you get when you run
        # Main loop for user interaction 
        while True:
            print("\n" + "="*40)
            print(COLORS['green'] + "PC Component Store Inventory System" + COLORS['reset'])
            print("="*40)
            print("1. CPU Components")
            print("2. GPU Components")
            print("3. Add New Component")
            print("4. Sell Component")
            print("5. Check Component Quantity")
            print("6. Exit Store")

            choice = input("\nEnter your choice (1-6): ")

            if choice == "1":
                # Show all CPUs and their stock
                print("\nAvailable CPUs:")
                for cpu in self.display_cpus():
                    print(f"- {cpu} (Stock: {self.inventory[cpu]})")

            elif choice == "2":
                # Show all GPUs and their stock
                print("\nAvailable GPUs:")
                for gpu in self.display_gpus():
                    print(f"- {gpu} (Stock: {self.inventory[gpu]})")

            elif choice == "3":
                # Add a new component (CPU or GPU)
                comp_type = input("Add CPU or GPU? ").lower()
                if comp_type in ["cpu", "gpu"]:
                    new_component, amount = self.add_component(comp_type)
                    self.inventory[new_component] = self.inventory.get(new_component, 0) + amount
                    print(f"Added {amount} units of {new_component}")
                else:
                    print("Invalid component type. Please enter 'CPU' or 'GPU'")

            elif choice == "4":
                # Sell a component
                component = input("Enter component to sell: ")
                print(self.sell_component(component))

            elif choice == "5":
                # Check quantity of a component
                component = input("Enter component name: ")
                quantity = self.check_quantity(component)
                print(f"Available quantity: {quantity}")

            elif choice == "6":
                # Save and exit
                self.save_inventory()
                print("Inventory saved. Exiting store.")
                break

            else:
                print("Invalid choice. Please enter a number between 1-6.")

# Entry point for the application
if __name__ == "__main__":
    # Create sample inventory file if it doesn't exist
    if not os.path.exists("inventory.txt"):
        with open("inventory.txt", "w") as f:
            f.write("""Ryzen 5600X:10
Ryzen 5800X:8
Ryzen 5950X:5
Core i5-12400:12
Core i7-12700K:7
Core i9-12900KS:3
RTX 3060:15
RTX 3070:9
RTX 3080:6
RX 6600 XT:11
RX 6800 XT:8
RX 6900 XT:4""")
    store = PCStore()
    store.run()
