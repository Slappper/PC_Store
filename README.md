# PC_Store

# PC Component Store Inventory System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pytest](https://img.shields.io/badge/Pytest-Tested-green.svg)
![OOP](https://img.shields.io/badge/OOP-Implemented-yellowgreen.svg)

A complete inventory management system for PC component stores, built with Python using object-oriented principles.

## Features

- **Inventory Management**: Track CPUs, GPUs, and other components
- **Validation System**: Enforces proper naming conventions for components
- **Sales Processing**: Record component sales with stock reduction
- **Reporting**: View current stock levels and available products
- **Data Persistence**: Automatically saves inventory to file
- **Testing Suite**: Comprehensive pytest coverage

## How It Works

### Core Components

1. **FileHandler Class**
   - Base class for file operations
   - Uses generators for memory-efficient file reading
   - Implements `__add__` for file concatenation

2. **InventoryFileHandler Class** (inherits from FileHandler)
   - Specialized for inventory management
   - Overrides `__add__` to merge inventory quantities
   - Handles loading/saving inventory data

3. **PCStore Class**
   - Main application logic
   - Handles user interactions through a console menu
   - Implements strict validation for component names:
     - CPUs: `Ryzen 5600X` or `Core i5-12400K`
     - GPUs: `RTX 3060` or `RX 6800 XT`

### Data Flow

```mermaid
graph TD
    A[User Menu] --> B[View Inventory]
    A --> C[Add Components]
    A --> D[Sell Components]
    A --> E[Check Quantities]
    B --> F[Display CPUs/GPUs]
    C --> G[Validate Input]
    D --> H[Update Inventory]
    E --> I[Query Stock]
    H --> J[Save to File]
    I --> J
