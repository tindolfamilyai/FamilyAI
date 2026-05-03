# Data Contracts

These headers and conventions are the shared contract for all agents.

## Global Conventions

- Dates use ISO format: `YYYY-MM-DD`.
- Annual recurring dates use `MM-DD`.
- Times use readable local time such as `9 AM`, `2:30 PM`, or `5-6:30 PM`.
- Calendar prefixes: `B:` Blake, `M:` Melina, `Be:` Bella, `Mi:` Mila. No prefix means the whole family.
- Do not change CSV headers unless the user asks for a schema change and the related README is updated too.
- Append new factual rows when logging events. Do not silently rewrite past records.

## CSV Schemas

### `00_Calendar/YYYY-MM.csv`

`Date,Day,6 AM,7 AM,8 AM,9 AM,10 AM,11 AM,12 PM,1 PM,2 PM,3 PM,4 PM,5 PM,6 PM,7 PM,8 PM,9 PM,10 PM,11 PM`

### `02_Health_Fitness/Meal_Plans/grocery_list.csv`

`Item,Category,Quantity,Need By,Status`

### `02_Health_Fitness/Meal_Plans/meal_plan.csv`

`Date,Breakfast,Lunch,Dinner,Snacks,Notes`

### `02_Health_Fitness/Meal_Plans/food_log.csv`

`Date,Person,Meal,Food/Description,Calories,Protein (g),Carbs (g),Fat (g),Fiber (g),Notes`

### `02_Health_Fitness/Meal_Plans/body_metrics_log.csv`

`Date,Person,Weight (lb),Waist,Calories Target,Protein Target (g),Energy (1-5),Hunger (1-5),Training Performance,Notes,Adjustment`

### `_Archive/02_Health_Fitness/Workouts/Blake/blake_workouts_2026-05-04_to_2026-07-26.csv`

`Date,Week,Day,Session,Exercise,Sets,Reps/Sec,Load (lb),RPE,Time/Dist,Notes`

### `02_Health_Fitness/Workouts/Blake/blake_workouts_performed.csv`

`Date,Session,Exercise,Sets,Reps/Sec,Load (lb),RPE,Time/Dist,Notes,Source`

### `02_Health_Fitness/Workouts/Melina/melina_workouts.csv`

`Date,Workout Type,Duration (min),Exercises,Sets x Reps / Distance,Intensity (1-10),Calories,Notes`

### `03_Kids/<Child>/growth_log.csv`

`Date,Age,Height,Weight,Clothing Size,Shoe Size,Notes`

### `03_Kids/<Child>/medical_log.csv`

`Date,Type,Provider,Reason,Notes,Follow-up Needed`

### `04_Pets/<Dog>/vet_log.csv`

`Date,Reason,Vet,Weight (lbs),Vaccines/Treatments,Cost,Next Visit Due,Notes`

### `04_Pets/walks_log.csv`

`Date,Time,Dog,Walker,Duration (min),Notes`

### `05_Home/inventory.csv`

`Item,Room,Brand/Model,Purchase Date,Cost,Warranty Expires,Serial #,Notes`

### `05_Home/maintenance_log.csv`

`Date,Task,Category,Done By,Cost,Next Due,Notes`

### `05_Home/repairs_log.csv`

`Date,Issue,Room,Resolved By,Cost,Status,Notes`

### `06_Finances/expenses.csv`

`Date,Category,Description,Amount,Payment Method,Notes`

### `06_Finances/monthly_budget.csv`

`Category,Subcategory,Budgeted,Actual,Variance,Notes`

### `06_Finances/subscriptions.csv`

`Service,Cost,Frequency,Renewal Date,Payment Method,Used By,Keep?,Notes`

### `07_Travel/travel_budget_template.csv`

`Category,Estimated,Actual,Notes`

### `08_Social_Media_Orlando_Theme_Park_Family/analytics_log.csv`

`Date,Platform,Followers,Reach (28d),Engagement Rate,Top Post,Notes`

### `08_Social_Media_Orlando_Theme_Park_Family/brand_partnerships.csv`

`Brand,Status,Contact,Deal Type,Compensation,Deliverables,Due Date,Posted Date,Notes`

### `08_Social_Media_Orlando_Theme_Park_Family/content_calendar.csv`

`Date,Platform,Content Type,Caption/Concept,Status,Post Time,Hashtags,Collab/Brand,Notes`

### `09_Holidays_Birthdays/annual_events.csv`

`Date (MM-DD),Event,Person/Type,Recurring,Gift Ideas,Notes`
