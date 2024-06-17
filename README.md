# Calorie Counter in Django

## Intial Setup

* Project Name - `mysite`, App name - `myapp`

* Make a model `Food` in `myapp/models.py`:

```python
from django.db import models

class Food(models.Model):
    
    def __str__(self):
        return self.name
        
    name = models.CharField(max_length=100)
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    calories = models.IntegerField()
```

* After making necessary migrations, define a view to render a template. In `myapp/views.py`:-

```python
from django.shortcuts import render
from .models import Food

def index(request):
    food = Food.objects.all()
    return render(request, "myapp/index.html", {"foods": food})
```

* Now create a template in `myapp/templates/myapp/index.html`. We will create a template where all the name of foods will appear in a select box.

```html
<form method="POST">
    {% csrf_token %}
    <select name="food_consumed" id="food_consumed">
        {% for food in foods %}
            <option value="{{ food.id }}">{{ food.name }}</option>
        {% endfor %}
    </select>
    
    <button type="submit">Add</button>
</form>
```

**Challenge** - Now, in this project, we want user to select a food item and the macronutrient will be added to the consumption list of a user. Now the challenge is to have different consumptions for different users.

## User & Consume Model

First lets import Django pre-built `User` model. In `myapp/models.py`, 

```python
from django.contrib.auth.models import User
```

Now we will make a consume model which will contain which user ate which food. Now, we can link two tables using `ForeignKey`. In `myapp/models.py`, add the new model:-

```python
class Consume(models.Model):
    # Foreign key will link User Model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Foreign key will link Food Model
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
```

Make necessary migrations and register the model to admin page.

## Add functionality to Consume Model

Now when user clicks `Add`, the value from select box `food_consumed` will be obtained. Next the current user is to be extracted. Then, in a object of `Consume` model, both values will be passed and saved. We will have to do all this in the view `index`. Update `index` in `myapp/views.py`:-

```python
from django.shortcuts import render
# Import Consume Model
from .models import Food, Consume

def index(request):
    food = Food.objects.all()
    
    # If Add button is clicked
    if request.method == "POST":
        food_consumed = request.POST.get("food_consumed")
        # Get the food object using the ID from food_consumed
        food_object = Food.objects.get(pk=food_consumed)
        # Current User Object
        user = request.user
        
        # Pass these values to consume object
        consume = Consume(user=user, food_consumed=food_object)
        
        # Save the object
        consume.save()
        
    return render(request, "myapp/index.html", {"foods": food})
```

## Listing Consumed Food Items

Now, we want to show the list of items consumed. We can do so easily in `myapp/views.py`:-

```python
def index(request):
    food = Food.objects.all()
    # Filter consume model by user
    consumed_food_by_user = Consume.objects.filter(user=request.user)

    ...
    ...
    
    context = {"foods": food,
               "consumed_foods": consumed_food_by_user}

    # Return the consumed_food_by_user as a context
    return render(request, "myapp/index.html", context)
```

Update the template to show a list of foods consumed by the user:-

```html
<h2>Consumed Foods</h2>
{% for consumed_food in consumed_foods %}
    <p>{{ consumed_food.food_consumed }} Carbs: {{ consumed_food.food_consumed.carbs }}gms</p>
{% endfor %}
```

**Imp** - As `food_consumed` is a foreign key of `Food` model, we can access the associated `carbs`, `protein`, `fat` and `calories` as `food_consumed.carbs` etc.

## Add Bootstrap

To improve how the page looks, lets add some Bootstrap. The updated template file:-

```html
<div class="container">
    <h2 class="mt-5 mb-3">Calorie Tracker</h2>
    <div class="row">
        <form method="POST">
            {% csrf_token %}
            <div class="row">
                <div class="col-11">
                    <select name="food_consumed" id="food_consumed" class="form-select">
                        {% for food in foods %}
                            <option value="{{ food.id }}">{{ food.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-1">
                    <button type="submit" class="btn btn-warning">Add</button>
                </div>
            </div>
        </form>
    </div>
    
    <div class="row">
        <div class="col-12 mt-5 mb-2"><h3>Consumed Foods</h3></div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <table class="table table-striped" id="table">
                <thead>
                    <tr>
                        <th scope="col">Food</th>
                        <th scope="col">Carbs (gms)</th>
                        <th scope="col">Protein (gms)</th>
                        <th scope="col">Fat (gms)</th>
                        <th scope="col">Calories (KCal)</th>
                    </tr>
                </thead>
                
                <tbody>
                    {% for consumed_food in consumed_foods %}
                        <tr>
                            <td>{{ consumed_food.food_consumed }}</td>
                            <td>{{ consumed_food.food_consumed.carbs }}</td>
                            <td>{{ consumed_food.food_consumed.protein }}</td>
                            <td>{{ consumed_food.food_consumed.fats }}</td>
                            <td>{{ consumed_food.food_consumed.calories }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
```

## Calculating Total Macros

### Using Javascript

First create four divs with IDs `carbs-count`, `protein-count`, `fats-count` and `calories-count` which will contain the total values. In `<script></script>` after `</body>` add:-

```javascript
var table = document.getElementById("table");
var carbs = 0;
var protein = 0;
var fats = 0;
var calories = 0;

for(var i=1; i<table.rows.length; i++){
    carbs += parseFloat(table.rows[i].cells[1].innerHTML)
    protein += parseFloat(table.rows[i].cells[2].innerHTML)
    fats += parseFloat(table.rows[i].cells[3].innerHTML)
    calories += parseFloat(table.rows[i].cells[4].innerHTML)
}

// Update the elements. Here .to fixed(2) means round till two decimal points
document.getElementById("carbs-count").innerHTML = `${carbs.toFixed(2)}gms`
document.getElementById("protein-count").innerHTML = `${protein.toFixed(2)}gms`
document.getElementById("fats-count").innerHTML = `${fats.toFixed(2)}gms`
document.getElementById("calories-count").innerHTML = `${calories}KCal`
```

## Adding Calorie Progress Bar

Add BootStrap Progress in HTML:-

```html
<div class="progress" style="height: 4px;">
    <div id="pgbar" class="progress-bar bg-warning" role="progressbar" style="width: 0%;"></div>
</div>
```

ID of the progress bar is `pgbar` and the attribute we need to change is `style` for e.g. `width: 20%`. So in `<script></script>` at the end:-

```javascript
var prog = (calories/2500) * 100;
document.getElementById("pgbar").setAttribute("style", `width: ${prog}%`);
```

## Integrating ChartJS

Add ChartJS CDN to `<head></head>`:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

Add a `canvas` element where you want to put the chart:

```html
<canvas id="myChart"></canvas>
```

Now add the script for chart in `<script></script>`:- (Taken from documentation)

```javascript
const ctx = document.getElementById('myChart');

new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Carbohydrate', 'Protein', 'Fats'],
        datasets: [{
            label: 'Macronutrient Breakdown',
            data: [carbs, protein, fats],
            borderWidth: 1
        }]
    },
    
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
```

## Designing Delete Functionality

Add delete button in the table:

```html
<td><a href="/delete/{{ consumed_food.id }}" class="btn btn-danger">X</a></td>
```

Now, we will create a view to delete item. In `myapp/views.py`:-

```python
# import redirect
from django.shortcuts import render, redirect
from .models import Food, Consume

def delete_item(request,id):
    # Filter record to delete by ID
    selected_item = Consume.objects.get(id=id)
    # Delete the object
    selected_item.delete()
    # Redirect to home page
    return redirect('/')
```

Add the following line to `urlpatterns` in `myapp/urls.py`:-

```python
path('delete/<int:id>', views.delete_item, name="delete")
```
