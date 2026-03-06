import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json

class Database:
    def __init__(self, db_path: str = "finance.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date DATE NOT NULL,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Income table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                source TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Budget table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                category TEXT,
                amount REAL NOT NULL,
                period TEXT DEFAULT 'monthly',
                start_date DATE,
                end_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Goals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                title TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                deadline DATE,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Recurring payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recurring_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                frequency TEXT DEFAULT 'monthly',
                next_due_date DATE,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Create default user
        cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (1, 'default')")
        
        conn.commit()
        conn.close()
    
    def add_expense(self, category: str, amount: float, description: str, 
                   date: str, tags: List[str], user_id: int = 1) -> int:
        """Add a new expense"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tags_str = json.dumps(tags) if tags else "[]"
        
        cursor.execute("""
            INSERT INTO expenses (user_id, category, amount, description, date, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, category, amount, description, date, tags_str))
        
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return expense_id
    
    def get_expenses(self, user_id: int = 1, start_date: str = None, 
                    end_date: str = None, category: str = None) -> List[Dict]:
        """Get expenses with optional filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM expenses WHERE user_id = ?"
        params = [user_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY date DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        expenses = []
        for row in rows:
            expenses.append({
                'id': row[0],
                'user_id': row[1],
                'category': row[2],
                'amount': row[3],
                'description': row[4],
                'date': row[5],
                'tags': json.loads(row[6]) if row[6] else [],
                'created_at': row[7]
            })
        
        return expenses
    
    def add_income(self, source: str, amount: float, description: str,
                  date: str, user_id: int = 1) -> int:
        """Add income"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO income (user_id, source, amount, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, source, amount, description, date))
        
        income_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return income_id
    
    def get_income(self, user_id: int = 1, start_date: str = None,
                  end_date: str = None) -> List[Dict]:
        """Get income records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM income WHERE user_id = ?"
        params = [user_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        income_list = []
        for row in rows:
            income_list.append({
                'id': row[0],
                'user_id': row[1],
                'source': row[2],
                'amount': row[3],
                'description': row[4],
                'date': row[5],
                'created_at': row[6]
            })
        
        return income_list
    
    def set_budget(self, category: str, amount: float, period: str = 'monthly',
                  start_date: str = None, end_date: str = None, user_id: int = 1) -> int:
        """Set budget for a category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO budgets (user_id, category, amount, period, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, category, amount, period, start_date, end_date))
        
        budget_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return budget_id
    
    def get_budgets(self, user_id: int = 1) -> List[Dict]:
        """Get all budgets"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM budgets WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        budgets = []
        for row in rows:
            budgets.append({
                'id': row[0],
                'user_id': row[1],
                'category': row[2],
                'amount': row[3],
                'period': row[4],
                'start_date': row[5],
                'end_date': row[6],
                'created_at': row[7]
            })
        
        return budgets
    
    def add_goal(self, title: str, target_amount: float, deadline: str = None,
                user_id: int = 1) -> int:
        """Add a savings goal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO goals (user_id, title, target_amount, deadline)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, target_amount, deadline))
        
        goal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return goal_id
    
    def get_goals(self, user_id: int = 1) -> List[Dict]:
        """Get all goals"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM goals WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        goals = []
        for row in rows:
            goals.append({
                'id': row[0],
                'user_id': row[1],
                'title': row[2],
                'target_amount': row[3],
                'current_amount': row[4],
                'deadline': row[5],
                'status': row[6],
                'created_at': row[7]
            })
        
        return goals
    
    def add_recurring_payment(self, category: str, amount: float, description: str,
                            frequency: str, next_due_date: str, user_id: int = 1) -> int:
        """Add recurring payment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO recurring_payments 
            (user_id, category, amount, description, frequency, next_due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, category, amount, description, frequency, next_due_date))
        
        payment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return payment_id
    
    def get_recurring_payments(self, user_id: int = 1) -> List[Dict]:
        """Get all recurring payments"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM recurring_payments 
            WHERE user_id = ? AND is_active = 1
            ORDER BY next_due_date
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        payments = []
        for row in rows:
            payments.append({
                'id': row[0],
                'user_id': row[1],
                'category': row[2],
                'amount': row[3],
                'description': row[4],
                'frequency': row[5],
                'next_due_date': row[6],
                'is_active': row[7],
                'created_at': row[8]
            })
        
        return payments
    
    def get_statistics(self, user_id: int = 1, start_date: str = None,
                      end_date: str = None) -> Dict:
        """Get financial statistics"""
        expenses = self.get_expenses(user_id, start_date, end_date)
        income = self.get_income(user_id, start_date, end_date)
        
        total_expenses = sum(e['amount'] for e in expenses)
        total_income = sum(i['amount'] for i in income)
        
        # Category breakdown
        category_totals = {}
        for expense in expenses:
            cat = expense['category']
            category_totals[cat] = category_totals.get(cat, 0) + expense['amount']
        
        return {
            'total_expenses': total_expenses,
            'total_income': total_income,
            'balance': total_income - total_expenses,
            'expense_count': len(expenses),
            'income_count': len(income),
            'category_breakdown': category_totals,
            'average_expense': total_expenses / len(expenses) if expenses else 0
        }
