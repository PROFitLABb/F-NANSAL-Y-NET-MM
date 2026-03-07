from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from backend.agent import FinancialAgent
from backend.database import Database

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Personal Finance Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the financial agent and database
agent = FinancialAgent()
db = Database()

class ExpenseText(BaseModel):
    text: str
    provider: str = "gemini"

class ExpenseAnalysis(BaseModel):
    category: str
    amount: float
    description: str
    date: Optional[str] = None
    tags: List[str] = []

class AnalysisResponse(BaseModel):
    expenses: List[ExpenseAnalysis]
    summary: str
    suggestions: List[str]

@app.get("/")
def read_root():
    return {"message": "AI Personal Finance Assistant API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze")
def analyze_expense(expense: ExpenseText):
    try:
        if not expense.text.strip():
            raise HTTPException(status_code=400, detail="Expense text cannot be empty")
        
        print(f"Analyzing expense: {expense.text}")
        
        result = agent.analyze_expense(
            expense_text=expense.text,
            provider=expense.provider
        )
        
        print(f"Analysis result: {result}")
        
        return result
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# New Models
class IncomeData(BaseModel):
    source: str
    amount: float
    description: str = ""
    date: str

class BudgetData(BaseModel):
    category: Optional[str] = None
    amount: float
    period: str = "monthly"
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class GoalData(BaseModel):
    title: str
    target_amount: float
    deadline: Optional[str] = None

class RecurringPaymentData(BaseModel):
    category: str
    amount: float
    description: str
    frequency: str
    next_due_date: str

# Income endpoints
@app.post("/income")
def add_income(income: IncomeData):
    try:
        income_id = db.add_income(
            source=income.source,
            amount=income.amount,
            description=income.description,
            date=income.date
        )
        return {"id": income_id, "message": "Income added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/income")
def get_income(start_date: str = None, end_date: str = None):
    try:
        income_list = db.get_income(start_date=start_date, end_date=end_date)
        return {"income": income_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Expense history endpoints
@app.get("/expenses")
def get_expenses(start_date: str = None, end_date: str = None, category: str = None):
    try:
        expenses = db.get_expenses(start_date=start_date, end_date=end_date, category=category)
        return {"expenses": expenses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/expenses/save")
def save_expenses(expenses: List[ExpenseAnalysis]):
    try:
        saved_ids = []
        for expense in expenses:
            expense_id = db.add_expense(
                category=expense.category,
                amount=expense.amount,
                description=expense.description,
                date=expense.date or datetime.now().strftime("%Y-%m-%d"),
                tags=expense.tags
            )
            saved_ids.append(expense_id)
        return {"message": "Expenses saved successfully", "ids": saved_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Budget endpoints
@app.post("/budget")
def set_budget(budget: BudgetData):
    try:
        budget_id = db.set_budget(
            category=budget.category,
            amount=budget.amount,
            period=budget.period,
            start_date=budget.start_date,
            end_date=budget.end_date
        )
        return {"id": budget_id, "message": "Budget set successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/budget")
def get_budgets():
    try:
        budgets = db.get_budgets()
        return {"budgets": budgets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/budget/check")
def check_budget(category: str = None):
    try:
        # Get current month expenses
        today = datetime.now()
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        
        expenses = db.get_expenses(start_date=start_date, end_date=end_date, category=category)
        budgets = db.get_budgets()
        
        total_spent = sum(e['amount'] for e in expenses)
        
        warnings = []
        for budget in budgets:
            if category and budget['category'] != category:
                continue
            
            cat_expenses = [e for e in expenses if e['category'] == budget['category']]
            cat_spent = sum(e['amount'] for e in cat_expenses)
            
            percentage = (cat_spent / budget['amount'] * 100) if budget['amount'] > 0 else 0
            
            if percentage >= 100:
                warnings.append({
                    'category': budget['category'],
                    'budget': budget['amount'],
                    'spent': cat_spent,
                    'percentage': percentage,
                    'status': 'exceeded',
                    'message': f"{budget['category']} bütçesi aşıldı!"
                })
            elif percentage >= 80:
                warnings.append({
                    'category': budget['category'],
                    'budget': budget['amount'],
                    'spent': cat_spent,
                    'percentage': percentage,
                    'status': 'warning',
                    'message': f"{budget['category']} bütçesinin %{percentage:.0f}'i kullanıldı"
                })
        
        return {
            'total_spent': total_spent,
            'warnings': warnings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Goals endpoints
@app.post("/goals")
def add_goal(goal: GoalData):
    try:
        goal_id = db.add_goal(
            title=goal.title,
            target_amount=goal.target_amount,
            deadline=goal.deadline
        )
        return {"id": goal_id, "message": "Goal added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/goals")
def get_goals():
    try:
        goals = db.get_goals()
        return {"goals": goals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Recurring payments endpoints
@app.post("/recurring")
def add_recurring_payment(payment: RecurringPaymentData):
    try:
        payment_id = db.add_recurring_payment(
            category=payment.category,
            amount=payment.amount,
            description=payment.description,
            frequency=payment.frequency,
            next_due_date=payment.next_due_date
        )
        return {"id": payment_id, "message": "Recurring payment added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recurring")
def get_recurring_payments():
    try:
        payments = db.get_recurring_payments()
        
        # Check for upcoming payments
        today = datetime.now().date()
        upcoming = []
        
        for payment in payments:
            due_date = datetime.strptime(payment['next_due_date'], "%Y-%m-%d").date()
            days_until = (due_date - today).days
            
            if days_until <= 7:
                upcoming.append({
                    **payment,
                    'days_until': days_until,
                    'is_overdue': days_until < 0
                })
        
        return {
            'payments': payments,
            'upcoming': upcoming
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Statistics endpoint
@app.get("/statistics")
def get_statistics(start_date: str = None, end_date: str = None):
    try:
        stats = db.get_statistics(start_date=start_date, end_date=end_date)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Dashboard endpoint
@app.get("/dashboard")
def get_dashboard():
    try:
        today = datetime.now()
        
        # Current month
        month_start = today.replace(day=1).strftime("%Y-%m-%d")
        month_end = today.strftime("%Y-%m-%d")
        
        # Last month
        last_month_end = (today.replace(day=1) - timedelta(days=1))
        last_month_start = last_month_end.replace(day=1).strftime("%Y-%m-%d")
        last_month_end_str = last_month_end.strftime("%Y-%m-%d")
        
        current_stats = db.get_statistics(start_date=month_start, end_date=month_end)
        last_month_stats = db.get_statistics(start_date=last_month_start, end_date=last_month_end_str)
        
        # Budget check
        budget_check = check_budget()
        
        # Upcoming payments
        recurring = get_recurring_payments()
        
        # Goals
        goals = db.get_goals()
        
        return {
            'current_month': current_stats,
            'last_month': last_month_stats,
            'budget_warnings': budget_check['warnings'],
            'upcoming_payments': recurring['upcoming'],
            'goals': goals
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
