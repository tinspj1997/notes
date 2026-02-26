
# SQL Alchemy

## Join Load

If `contains_eager` is the manual way, **`joinedload`** is the "automatic" way to load related data in one single trip to the database.


---

### Why use it? (The N+1 Problem)

Without `joinedload`, if you have 10 users and you want to print their orders, SQLAlchemy does this:

1. **1 Query** to get all 10 users.
2. **10 extra Queries** (one for each user) to get their orders.
This is called the **N+1 problem**, and it makes your app very slow.

With `joinedload`, SQLAlchemy does **1 single Query** using a `LEFT OUTER JOIN`. It gets everything at once.

---

### How it looks in code

You don't need to write the `.join()` yourself. You just add it as an "option."

```python
from sqlalchemy.orm import joinedload

# This creates the JOIN for you automatically
users = session.query(User).options(joinedload(User.orders)).all()

for u in users:
	print(u.orders) # No extra database hits here! The data is already there.

```
