Database schema and endpoint structure for a simple To-Do List project using FastAPI. 

### Database Schema (SQL)

```sql
-- Simple table for todo tasks
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER REFERENCES categories(id)
);

-- Optional table for task categories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
```

### API Endpoints

**Tasks Endpoints:**
1. **Create Task**
   - POST `/tasks/`
   - Request Body:
     ```json
     {
         "title": "string",
         "description": "string",
         "due_date": "datetime (optional)",
         "completed": "boolean (default: false)",
         "category_name": "string (optional)"
     }
     ```

2. **Get All Tasks**
   - GET `/tasks/`
   - Query Parameters:
     - `completed`: boolean (filter by completion status)
     - `category_name`: string (filter by category)
     - `due_date_from`: date (filter tasks due after this date)
     - `due_date_to`: date (filter tasks due before this date)

3. **Get Single Task**
   - GET `/tasks/{task_id}`

4. **Update Task**
   - PUT `/tasks/{task_id}`
   - Request Body (all fields optional):
     ```json
     {
         "title": "string",
         "description": "string",
         "due_date": "datetime",
         "completed": "boolean",
         "category_name": "string"
     }
     ```

5. **Delete Task**
   - DELETE `/tasks/{task_id}`

**Categories Endpoints:**
1. **Create Category**
   - POST `/categories/`
   - Request Body:
     ```json
     {
         "name": "string"
     }
     ```

2. **Get All Categories**
   - GET `/categories/`

3. **Delete Category**
   - DELETE `/categories/{category_id}`
   - (Only if no tasks are associated with it)

### Relations Explanation
- **One-to-Many Relationship**: 
  - A category can have many tasks (through `category_id` foreign key)
  - A task belongs to 0 or 1 category


This structure gives a good foundation to practice:
- CRUD operations
- Database relationships
- API endpoint design
- Query parameter handling
- Error handling
- Data validation

### Final
![image](https://github.com/user-attachments/assets/65435669-6e9f-43b5-9051-1a3584c76a87)

