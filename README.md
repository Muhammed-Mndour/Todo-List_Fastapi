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

### Suggested Features to Implement
1. Input validation (e.g., title cannot be empty)
2. Proper error handling (404 for missing resources)
3. Sorting options for GET /tasks/ endpoint
4. Database constraints (e.g., unique category names)

### Tips for Implementation
1. Use SQL model for database interactions
2. Implement proper Pydantic models for request/response validation
3. Consider using Alembic for database migrations
4. Add created_at/updated_at timestamps for better tracking
5. Test your API endpoints with different scenarios:
   - Creating tasks with/without categories
   - Updating completion status
   - Filtering by multiple criteria

This structure gives you a good foundation to practice:
- CRUD operations
- Database relationships
- API endpoint design
- Query parameter handling
- Error handling
- Data validation

